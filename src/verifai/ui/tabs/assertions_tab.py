from __future__ import annotations

from verifai.core.services.assertions import AssertionResult, AssertionWriter
from verifai.ui.tabs.base_tab import ServiceTab


class AssertionsTab(ServiceTab):
    def __init__(self, service: AssertionWriter) -> None:
        self._service = service
        super().__init__(
            title="SVA Assertion Writing",
            instructions=(
                "Describe a protocol or design behavior in plain English and receive "
                "synthesizable SystemVerilog Assertions."
            ),
            run_label="Write Assertions",
            input_placeholder="e.g. \"req must be followed by ack within 4 cycles, and req must stay high until ack.\"",
        )

    def _call_service(self, text: str) -> AssertionResult:
        return self._service.write(text)

    def _format_result(self, result: AssertionResult) -> str:
        return result.code
