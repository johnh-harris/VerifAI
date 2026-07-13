from verifai.core.services.testbench import TestbenchResult
from verifai.ui.tabs.testbench_tab import TestbenchTab


class FakeTestbenchGenerator:
    def generate(self, module_source: str, module_name: str | None = None) -> TestbenchResult:
        return TestbenchResult(code=f"// testbench for: {module_source}")


class FailingTestbenchGenerator:
    def generate(self, module_source: str, module_name: str | None = None) -> TestbenchResult:
        raise RuntimeError("boom")


def test_run_populates_output(qtbot):
    tab = TestbenchTab(FakeTestbenchGenerator())
    qtbot.addWidget(tab)

    tab.input_edit.setPlainText("module dut; endmodule")
    tab.run_btn.click()

    qtbot.waitUntil(lambda: tab.status_label.text() == "Done.", timeout=2000)
    assert tab.output_edit.toPlainText() == "// testbench for: module dut; endmodule"
    assert tab.run_btn.isEnabled()


def test_run_with_empty_input_shows_message_without_calling_service(qtbot):
    tab = TestbenchTab(FakeTestbenchGenerator())
    qtbot.addWidget(tab)

    tab.run_btn.click()

    assert tab.status_label.text() == "Input is empty."
    assert tab.output_edit.toPlainText() == ""


def test_run_surfaces_service_errors(qtbot):
    tab = TestbenchTab(FailingTestbenchGenerator())
    qtbot.addWidget(tab)

    tab.input_edit.setPlainText("module dut; endmodule")
    tab.run_btn.click()

    qtbot.waitUntil(lambda: tab.status_label.text() == "Error.", timeout=2000)
    assert "boom" in tab.output_edit.toPlainText()
    assert tab.run_btn.isEnabled()
