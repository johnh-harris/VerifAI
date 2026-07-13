from __future__ import annotations

from dataclasses import dataclass, field

from verifai.core.services.base import AgentService
from verifai.utils.json_extract import extract_json_object


@dataclass(frozen=True)
class CoverageGap:
    bin: str
    description: str
    suggested_test: str


@dataclass(frozen=True)
class CoverageAnalysisResult:
    summary: str
    gaps: list[CoverageGap] = field(default_factory=list)
    raw_response: str = ""


class CoverageAnalyzer(AgentService):
    """Analyzes a functional coverage report and suggests directed tests for the gaps."""

    system_prompt = (
        "You are a senior hardware verification engineer analyzing functional coverage "
        "reports. Given a coverage report, identify which coverage bins or cross points "
        "are underrepresented or missing, and suggest a directed test that would close "
        "each gap. Respond with ONLY a JSON object matching this schema, no prose, no "
        "code fences:\n"
        '{"summary": "<one paragraph summary>", "gaps": ['
        '{"bin": "<bin or coverpoint name>", "description": "<why it is a gap>", '
        '"suggested_test": "<directed test that would close it>"}]}'
    )

    def analyze(self, coverage_report: str) -> CoverageAnalysisResult:
        if not coverage_report.strip():
            raise ValueError("coverage_report must not be empty")

        response = self._ask(f"Coverage report:\n\n{coverage_report}")
        data = extract_json_object(response)
        gaps = [
            CoverageGap(
                bin=item.get("bin", "unknown"),
                description=item.get("description", ""),
                suggested_test=item.get("suggested_test", ""),
            )
            for item in data.get("gaps", [])
        ]
        return CoverageAnalysisResult(summary=data.get("summary", ""), gaps=gaps, raw_response=response)
