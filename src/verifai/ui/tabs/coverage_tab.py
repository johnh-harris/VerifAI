from __future__ import annotations

from verifai.core.services.coverage import CoverageAnalysisResult, CoverageAnalyzer
from verifai.ui.tabs.base_tab import ServiceTab


class CoverageTab(ServiceTab):
    def __init__(self, service: CoverageAnalyzer) -> None:
        self._service = service
        super().__init__(
            title="Coverage Gap Analysis",
            instructions=(
                "Paste a functional coverage report to find underrepresented corner "
                "cases and get suggested directed tests to close them."
            ),
            run_label="Analyze Coverage",
            input_placeholder="Paste coverage report output here…",
        )

    def _call_service(self, text: str) -> CoverageAnalysisResult:
        return self._service.analyze(text)

    def _format_result(self, result: CoverageAnalysisResult) -> str:
        lines = [result.summary, ""]
        for i, gap in enumerate(result.gaps, start=1):
            lines.append(f"{i}. {gap.bin}")
            lines.append(f"   Gap: {gap.description}")
            lines.append(f"   Suggested test: {gap.suggested_test}")
            lines.append("")
        return "\n".join(lines).strip()
