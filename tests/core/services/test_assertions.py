import pytest

from verifai.core.services.assertions import AssertionWriter


class FakeAgent:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def run(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def test_write_strips_code_fence() -> None:
    agent = FakeAgent("```systemverilog\nassert property (@(posedge clk) req |-> ##[1:4] ack);\n```")
    writer = AssertionWriter(agent=agent)

    result = writer.write("req must be followed by ack within 4 cycles")

    assert result.code == "assert property (@(posedge clk) req |-> ##[1:4] ack);"


def test_write_includes_signal_hint() -> None:
    agent = FakeAgent("assert property (...);")
    writer = AssertionWriter(agent=agent)

    writer.write("req/ack handshake", signals=["req", "ack"])

    assert "req, ack" in agent.prompts[0]


def test_write_rejects_empty_description() -> None:
    writer = AssertionWriter(agent=FakeAgent(""))

    with pytest.raises(ValueError):
        writer.write("")
