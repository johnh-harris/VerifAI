from __future__ import annotations

from verifai.core.agent.agent import Agent


class AgentService:
    """Base class for services that wrap a single-purpose Agent.

    Subclasses set `system_prompt` and add a domain method that calls
    `self._ask(prompt)`. An `agent` can be injected (e.g. in tests) to
    bypass constructing a real `anthropic.Anthropic` client.
    """

    system_prompt: str = "You are a helpful assistant."

    def __init__(self, api_key: str | None = None, agent: Agent | None = None) -> None:
        self._agent = agent if agent is not None else Agent(system=self.system_prompt, api_key=api_key)

    def _ask(self, prompt: str) -> str:
        return self._agent.run(prompt)
