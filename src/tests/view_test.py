import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsView
from PySide6.QtCore import QThread, Qt

from src.util.widget_util import ColorLabel


class View(QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 160)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        color_label = ColorLabel(self)
        color_label.set_color([QColor("#00FF00"), QColor("#FFFF00")])
        self.layout.addWidget(color_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
