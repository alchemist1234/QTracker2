import sys

from PySide6.QtWidgets import QApplication
import PySide6.QtAsyncio as QtAsyncio

from src.view.main import MainWindow, Settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = Settings("config.ini")
    window = MainWindow(settings)
    window.show()
    QtAsyncio.run()
    # sys.exit(app.exec())
