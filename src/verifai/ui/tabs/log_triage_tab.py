from __future__ import annotations

from verifai.core.services.log_triage import LogTriage, LogTriageResult
from verifai.ui.tabs.base_tab import ServiceTab


class LogTriageTab(ServiceTab):
    def __init__(self, service: LogTriage) -> None:
        self._service = service
        super().__init__(
            title="Simulation Log Triage",
            instructions=(
                "Paste simulation output to flag failures, categorize likely causes, "
                "and see which signals to probe next."
            ),
            run_label="Triage Log",
            input_placeholder="Paste simulation log output here…",
        )

    def _call_service(self, text: str) -> LogTriageResult:
        return self._service.triage(text)

    def _format_result(self, result: LogTriageResult) -> str:
        lines = [result.summary, ""]
        for i, failure in enumerate(result.failures, start=1):
            signal = f" ({failure.signal})" if failure.signal else ""
            lines.append(f"{i}. [{failure.category}]{signal}")
            lines.append(f"   {failure.description}")
            lines.append(f"   Probe: {failure.suggested_probe}")
            lines.append("")
        return "\n".join(lines).strip()
