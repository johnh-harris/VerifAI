import sys
from PyQt6.QtWidgets import QApplication
from verifai.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("VerifAI")
    app.setOrganizationName("VerifAI")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
