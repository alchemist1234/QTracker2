import sys

from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtWidgets import QGraphicsSimpleTextItem, QApplication
from src.view.custom_widget import MarkItem
from src.settings.settings import Settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = Settings("config.ini")
    item = MarkItem(settings, 1, 100, 100)
    # item = QGraphicsSimpleTextItem('123')
    # item.
    # item.setFont(QFont('Arial', 10))
    # item.setText('123')
