from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QStatusBar, QTabWidget

from verifai.core.services.assertions import AssertionWriter
from verifai.core.services.coverage import CoverageAnalyzer
from verifai.core.services.log_triage import LogTriage
from verifai.core.services.testbench import TestbenchGenerator
from verifai.core.config import get_api_key
from verifai.ui.api_connector import ApiKeyDialog
from verifai.ui.tabs import AssertionsTab, CoverageTab, LogTriageTab, TestbenchTab


class MainWindow(QMainWindow):
    def __init__(self, api_key: str | None = None) -> None:
        super().__init__()
        self.api_key = api_key
        self.setWindowTitle("VerifAI")
        self.setMinimumSize(800, 600)
        self._build_menu()
        self._build_tabs()
        self._build_statusbar()

    def _build_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")

        api_key_action = QAction("&API Key…", self)
        api_key_action.triggered.connect(self._on_api_key)
        file_menu.addAction(api_key_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = menu.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _build_tabs(self) -> None:
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self._populate_tabs()

    def _populate_tabs(self) -> None:
        self.tabs.clear()
        self.tabs.addTab(TestbenchTab(TestbenchGenerator(api_key=self.api_key)), "Testbench Generation")
        self.tabs.addTab(AssertionsTab(AssertionWriter(api_key=self.api_key)), "SVA Assertion Writing")
        self.tabs.addTab(CoverageTab(CoverageAnalyzer(api_key=self.api_key)), "Coverage Gap Analysis")
        self.tabs.addTab(LogTriageTab(LogTriage(api_key=self.api_key)), "Simulation Log Triage")

    def _build_statusbar(self) -> None:
        bar = QStatusBar()
        self.setStatusBar(bar)
        if self.api_key:
            bar.showMessage("Ready")
        else:
            bar.showMessage("No API key configured — set one under File > API Key…")

    def _on_api_key(self) -> None:
        dialog = ApiKeyDialog(self)
        if dialog.exec():
            self.api_key = get_api_key()
            self._populate_tabs()
            self.statusBar().showMessage("Ready" if self.api_key else "No API key configured")

    def _on_about(self) -> None:
        QMessageBox.about(self, "About VerifAI", "VerifAI v0.1.0\n\nAI-powered verification tool.")
