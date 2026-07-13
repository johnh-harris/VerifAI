import pytest

from verifai.core.services.testbench import TestbenchGenerator


class FakeAgent:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def run(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def test_generate_strips_code_fence() -> None:
    agent = FakeAgent("```systemverilog\nmodule tb; endmodule\n```")
    generator = TestbenchGenerator(agent=agent)

    result = generator.generate("module dut; endmodule")

    assert result.code == "module tb; endmodule"


def test_generate_includes_module_name_hint() -> None:
    agent = FakeAgent("module tb; endmodule")
    generator = TestbenchGenerator(agent=agent)

    generator.generate("module dut; endmodule", module_name="dut")

    assert "dut" in agent.prompts[0]


def test_generate_rejects_empty_input() -> None:
    generator = TestbenchGenerator(agent=FakeAgent(""))

    with pytest.raises(ValueError):
        generator.generate("   ")
