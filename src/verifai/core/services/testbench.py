from __future__ import annotations

from dataclasses import dataclass

from verifai.core.services.base import AgentService
from verifai.utils.text import strip_code_fence


@dataclass(frozen=True)
class TestbenchResult:
    code: str


class TestbenchGenerator(AgentService):
    """Generates a UVM-compatible testbench scaffold for a Verilog/SystemVerilog module."""

    system_prompt = (
        "You are a senior hardware verification engineer. Given a Verilog or "
        "SystemVerilog module, generate a UVM-compatible testbench scaffold for it: "
        "an interface, a driver, a monitor, a sequencer, a scoreboard, coverage groups, "
        "an environment class, and a base test class. Respond with SystemVerilog code "
        "only, no prose, wrapped in a single ```systemverilog code block."
    )

    def generate(self, module_source: str, module_name: str | None = None) -> TestbenchResult:
        if not module_source.strip():
            raise ValueError("module_source must not be empty")

        hint = f"The module under test is named `{module_name}`.\n\n" if module_name else ""
        prompt = f"{hint}Generate a UVM testbench scaffold for the following module:\n\n{module_source}"
        response = self._ask(prompt)
        return TestbenchResult(code=strip_code_fence(response))
