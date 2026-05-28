import pytest
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
