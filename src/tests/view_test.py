import sys

from PySide6.QtGui import QColor, QLinearGradient
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsLineItem

from src.view.custom_widget import ColorLabel


class View(QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 160)
        self.layout = QHBoxLayout()
        view = QGraphicsView()
        self.layout.addWidget(view)
        scene = QGraphicsScene(view)
        line_item = QGraphicsLineItem()
        gradient = QLinearGradient(0, 0, 100, 100)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
