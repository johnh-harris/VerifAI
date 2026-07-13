from __future__ import annotations

from dataclasses import dataclass

from verifai.core.services.base import AgentService
from verifai.utils.text import strip_code_fence


@dataclass(frozen=True)
class AssertionResult:
    code: str


class AssertionWriter(AgentService):
    """Writes synthesizable SystemVerilog Assertions from a plain-English description."""

    system_prompt = (
        "You are a senior hardware verification engineer specializing in SystemVerilog "
        "Assertions (SVA). Given a plain-English description of a protocol or design "
        "behavior, and optionally a list of relevant signals, write synthesizable SVA "
        "properties and assertions that check it. Respond with SystemVerilog code only, "
        "no prose, wrapped in a single ```systemverilog code block."
    )

    def write(self, description: str, signals: list[str] | None = None) -> AssertionResult:
        if not description.strip():
            raise ValueError("description must not be empty")

        signal_hint = f"\n\nRelevant signals: {', '.join(signals)}" if signals else ""
        prompt = f"Behavior to assert:\n{description}{signal_hint}"
        response = self._ask(prompt)
        return AssertionResult(code=strip_code_fence(response))
