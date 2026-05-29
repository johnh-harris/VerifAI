from __future__ import annotations

from typing import Any, Callable

import anthropic

_MODEL = "claude-opus-4-8"
_MAX_TOKENS = 16_000


class Agent:
    """
    Minimal agentic loop: send a prompt, run tools until Claude is done,
    return the final text response.

    Usage:
        agent = Agent(system="You are a helpful assistant.")

        @agent.tool(
            name="add",
            description="Add two numbers.",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        )
        def add(a: float, b: float) -> float:
            return a + b

        result = agent.run("What is 3 + 4?")
    """

    def __init__(self, system: str = "You are a helpful assistant.") -> None:
        self._client = anthropic.Anthropic()
        self._system = system
        self._tools: list[dict[str, Any]] = []
        self._handlers: dict[str, Callable[..., Any]] = {}

    # ------------------------------------------------------------------
    # Tool registration
    # ------------------------------------------------------------------

    def tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
    ) -> Callable:
        """Decorator that registers a function as a callable tool."""
        def decorator(fn: Callable) -> Callable:
            self._register(name, description, input_schema, fn)
            return fn
        return decorator

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Any],
    ) -> None:
        """Register a tool imperatively (alternative to the decorator)."""
        self._register(name, description, input_schema, handler)

    def _register(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Any],
    ) -> None:
        self._tools.append(
            {"name": name, "description": description, "input_schema": input_schema}
        )
        self._handlers[name] = handler

    # ------------------------------------------------------------------
    # Run loop
    # ------------------------------------------------------------------

    def run(self, prompt: str) -> str:
        """Run the agentic loop and return the final text response."""
        messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]

        # System prompt is cached so repeated calls with the same system text
        # only pay the full token cost once per cache TTL (~5 min).
        system: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": self._system,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        tool_kwargs: dict[str, Any] = {"tools": self._tools} if self._tools else {}

        while True:
            with self._client.messages.stream(
                model=_MODEL,
                max_tokens=_MAX_TOKENS,
                thinking={"type": "adaptive"},
                system=system,
                messages=messages,
                **tool_kwargs,
            ) as stream:
                response = stream.get_final_message()

            if response.stop_reason == "end_turn":
                return next(
                    (b.text for b in response.content if b.type == "text"), ""
                )

            if response.stop_reason != "tool_use":
                break

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": self._execute_tools(response)})

        return ""

    def _execute_tools(self, response: anthropic.types.Message) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for block in response.content:
            if block.type != "tool_use":
                continue

            handler = self._handlers.get(block.name)
            if handler is None:
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Unknown tool: {block.name}",
                    "is_error": True,
                })
                continue

            try:
                output = str(handler(**block.input))
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
            except Exception as exc:
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(exc),
                    "is_error": True,
                })

        return results
