from verifai.ui.main_window import MainWindow


def test_window_title(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "VerifAI"


def test_window_minimum_size(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.minimumWidth() == 800
    assert window.minimumHeight() == 600


def test_window_has_a_tab_per_feature(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    labels = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert labels == [
        "Testbench Generation",
        "SVA Assertion Writing",
        "Coverage Gap Analysis",
        "Simulation Log Triage",
    ]


def test_statusbar_flags_missing_api_key(qtbot, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    window = MainWindow(api_key=None)
    qtbot.addWidget(window)
    assert "No API key" in window.statusBar().currentMessage()
