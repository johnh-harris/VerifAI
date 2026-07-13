from __future__ import annotations

from pathlib import Path
from typing import Any

from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from verifai.ui.workers import Worker


class ServiceTab(QWidget):
    """Base tab: an input editor, a run button, and a read-only output editor.

    Subclasses implement `_call_service` (runs on a background thread) and
    `_format_result` (turns the service's result into display text).
    """

    def __init__(
        self,
        title: str,
        instructions: str,
        run_label: str,
        input_placeholder: str = "",
    ) -> None:
        super().__init__()
        self._worker: Worker | None = None
        self._build_ui(title, instructions, run_label, input_placeholder)

    def _build_ui(self, title: str, instructions: str, run_label: str, input_placeholder: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(heading)

        desc = QLabel(instructions)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)

        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlaceholderText(input_placeholder)
        layout.addWidget(self.input_edit, stretch=1)

        controls = QHBoxLayout()

        load_btn = QPushButton("Load File…")
        load_btn.clicked.connect(self._load_file)
        controls.addWidget(load_btn)

        controls.addStretch()

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666;")
        controls.addWidget(self.status_label)

        self.run_btn = QPushButton(run_label)
        self.run_btn.setDefault(True)
        self.run_btn.clicked.connect(self._on_run_clicked)
        controls.addWidget(self.run_btn)
        layout.addLayout(controls)

        self.output_edit = QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("Output will appear here.")
        layout.addWidget(self.output_edit, stretch=1)

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Load File")
        if not path:
            return
        try:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self.status_label.setText(f"Could not read file: {exc}")
            return
        self.input_edit.setPlainText(text)

    def _on_run_clicked(self) -> None:
        text = self.input_edit.toPlainText()
        if not text.strip():
            self.status_label.setText("Input is empty.")
            return

        self.run_btn.setEnabled(False)
        self.status_label.setText("Working…")

        self._worker = Worker(self._call_service, text)
        self._worker.succeeded.connect(self._on_success)
        self._worker.failed.connect(self._on_failure)
        self._worker.finished.connect(lambda: self.run_btn.setEnabled(True))
        self._worker.start()

    def _call_service(self, text: str) -> Any:
        raise NotImplementedError

    def _format_result(self, result: Any) -> str:
        raise NotImplementedError

    def _on_success(self, result: Any) -> None:
        self.status_label.setText("Done.")
        self.output_edit.setPlainText(self._format_result(result))

    def _on_failure(self, message: str) -> None:
        self.status_label.setText("Error.")
        self.output_edit.setPlainText(message)
