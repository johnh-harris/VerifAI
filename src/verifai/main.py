import sys
from PyQt6.QtWidgets import QApplication
from verifai.ui.main_window import MainWindow
from verifai.ui.api_connector import ApiKeyDialog
from verifai.core.config import get_api_key


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("VerifAI")
    app.setOrganizationName("VerifAI")

    if not get_api_key():
        dialog = ApiKeyDialog()
        dialog.exec()

    window = MainWindow(api_key=get_api_key())
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
