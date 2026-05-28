from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VerifAI")
        self.setMinimumSize(800, 600)
        self._build_menu()
        self._build_ui()
        self._build_statusbar()

    def _build_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = menu.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        label = QLabel("Welcome to VerifAI")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)

        subtitle = QLabel("Your AI-powered verification tool")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(subtitle)

        btn = QPushButton("Get Started")
        btn.setFixedWidth(160)
        btn.clicked.connect(self._on_get_started)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _build_statusbar(self) -> None:
        bar = QStatusBar()
        self.setStatusBar(bar)
        bar.showMessage("Ready")

    def _on_get_started(self) -> None:
        self.statusBar().showMessage("Starting…")

    def _on_about(self) -> None:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(self, "About VerifAI", "VerifAI v0.1.0\n\nAI-powered verification tool.")
