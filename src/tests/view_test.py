import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsView
from PySide6.QtCore import QThread, Qt


class View(QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 160)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.view = View()
        self.layout.addWidget(self.view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
