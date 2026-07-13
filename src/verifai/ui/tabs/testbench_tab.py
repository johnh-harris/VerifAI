from __future__ import annotations

from verifai.core.services.testbench import TestbenchGenerator, TestbenchResult
from verifai.ui.tabs.base_tab import ServiceTab


class TestbenchTab(ServiceTab):
    def __init__(self, service: TestbenchGenerator) -> None:
        self._service = service
        super().__init__(
            title="Testbench Generation",
            instructions=(
                "Paste a Verilog/SystemVerilog module and generate a UVM-compatible "
                "testbench scaffold, including stimulus, checkers, and coverage groups."
            ),
            run_label="Generate Testbench",
            input_placeholder="module my_module (\n  input  logic clk,\n  ...\n);\n  ...\nendmodule",
        )

    def _call_service(self, text: str) -> TestbenchResult:
        return self._service.generate(text)

    def _format_result(self, result: TestbenchResult) -> str:
        return result.code
