import pytest

from verifai.core.services.coverage import CoverageAnalyzer
from verifai.utils.json_extract import JsonExtractionError


class FakeAgent:
    def __init__(self, response: str) -> None:
        self.response = response

    def run(self, prompt: str) -> str:
        return self.response


def test_analyze_parses_gaps() -> None:
    response = """
    {
        "summary": "Reset corner cases are undertested.",
        "gaps": [
            {"bin": "cp_reset.mid_txn", "description": "Never hit reset mid-transaction.",
             "suggested_test": "Assert reset while a burst is in flight."}
        ]
    }
    """
    analyzer = CoverageAnalyzer(agent=FakeAgent(response))

    result = analyzer.analyze("=== coverage report ===")

    assert result.summary == "Reset corner cases are undertested."
    assert len(result.gaps) == 1
    assert result.gaps[0].bin == "cp_reset.mid_txn"
    assert result.gaps[0].suggested_test == "Assert reset while a burst is in flight."


def test_analyze_handles_fenced_json() -> None:
    response = '```json\n{"summary": "ok", "gaps": []}\n```'
    analyzer = CoverageAnalyzer(agent=FakeAgent(response))

    result = analyzer.analyze("report")

    assert result.summary == "ok"
    assert result.gaps == []


def test_analyze_raises_on_unparseable_response() -> None:
    analyzer = CoverageAnalyzer(agent=FakeAgent("not json at all"))

    with pytest.raises(JsonExtractionError):
        analyzer.analyze("report")


def test_analyze_rejects_empty_report() -> None:
    analyzer = CoverageAnalyzer(agent=FakeAgent(""))

    with pytest.raises(ValueError):
        analyzer.analyze("   ")
