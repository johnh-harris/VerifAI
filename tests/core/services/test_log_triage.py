import pytest

from verifai.core.services.log_triage import LogTriage


class FakeAgent:
    def __init__(self, response: str) -> None:
        self.response = response

    def run(self, prompt: str) -> str:
        return self.response


def test_triage_parses_failures() -> None:
    response = """
    {
        "summary": "One protocol violation found.",
        "failures": [
            {"signal": "ack", "category": "protocol violation",
             "description": "ack asserted without a pending req.",
             "suggested_probe": "Probe req/ack handshake around t=1200ns."}
        ]
    }
    """
    triage = LogTriage(agent=FakeAgent(response))

    result = triage.triage("UVM_ERROR ... ack asserted unexpectedly")

    assert result.summary == "One protocol violation found."
    assert len(result.failures) == 1
    assert result.failures[0].category == "protocol violation"
    assert result.failures[0].signal == "ack"


def test_triage_rejects_empty_log() -> None:
    triage = LogTriage(agent=FakeAgent(""))

    with pytest.raises(ValueError):
        triage.triage("")
