import sys

from PySide6.QtWidgets import QApplication

from src.view.main import MainWindow, Settings
# from src.settings.settings import Settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = Settings("config.ini")
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())
