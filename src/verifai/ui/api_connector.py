from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from verifai.core.config import get_api_key, set_api_key


class ApiKeyDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("API Key")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui()
        self._load_existing()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        heading = QLabel("Anthropic API Key")
        heading.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(heading)

        hint = QLabel(
            "Your key is stored securely in the system keychain and never written to disk."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(hint)

        self._key_input = QLineEdit()
        self._key_input.setPlaceholderText("sk-ant-…")
        self._key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self._key_input)

        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        self._toggle_btn = QPushButton("Show")
        self._toggle_btn.setFixedWidth(60)
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.toggled.connect(self._toggle_visibility)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self._toggle_btn)
        layout.addLayout(toggle_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self._clear_btn = QPushButton("Clear saved key")
        self._clear_btn.clicked.connect(self._clear_key)

        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._save)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self._clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _load_existing(self) -> None:
        existing = get_api_key()
        if existing:
            self._key_input.setText(existing)

    def _toggle_visibility(self, checked: bool) -> None:
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self._key_input.setEchoMode(mode)
        self._toggle_btn.setText("Hide" if checked else "Show")

    def _save(self) -> None:
        key = self._key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Empty key", "Please enter an API key before saving.")
            return
        if not key.startswith("sk-"):
            QMessageBox.warning(
                self,
                "Invalid key",
                'Anthropic API keys start with "sk-". Please check and try again.',
            )
            return
        set_api_key(key)
        QMessageBox.information(self, "Saved", "API key saved to keychain.")
        self.accept()

    def _clear_key(self) -> None:
        confirm = QMessageBox.question(
            self,
            "Clear key",
            "Remove the saved API key from the keychain?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            import keyring
            keyring.delete_password("verifai", "anthropic_api_key")
            self._key_input.clear()
            QMessageBox.information(self, "Cleared", "API key removed from keychain.")
