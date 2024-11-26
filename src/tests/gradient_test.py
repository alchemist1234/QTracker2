import sys

from PySide6.QtGui import QColor, QLinearGradient, QBrush, QPainter, QPixmap, QColorConstants
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QGraphicsView, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation


class GradientLabel(QLabel):
    def __init__(self, parent=None):
        super(GradientLabel, self).__init__(parent)
        self.painter = QPainter()
        self._colors = []

    def set_gradient(self, gradient: QLinearGradient):
        # gradient = QLinearGradient(0,  0, self.width(), 0)
        # gradient.setColorAt(0.0, QColorConstants.Blue)
        # gradient.setColorAt(0.5, QColorConstants.Green)
        # gradient.setColorAt(1.0, QColorConstants.Red)
        brush = QBrush(gradient)

        # brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.painter = QPainter()
        # self.gradient = gradient
        pixmap = QPixmap(self.width(), self.height())
        self.painter.begin(pixmap)
        self.painter.setBrush(brush)
        self.painter.drawRect(0, 0, self.width(), self.height())
        self.painter.end()
        self.setPixmap(pixmap)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 160)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        interpolator = QPropertyAnimation()
        duration = 1000
        interpolator.setDuration(duration)
        interpolator.setKeyValueAt(0, QColorConstants.Blue)
        interpolator.setKeyValueAt(0.5, QColorConstants.Green)
        interpolator.setKeyValueAt(1.0, QColorConstants.Red)
        pos = 0.8
        interpolator.setCurrentTime(int(pos * duration))
        print(interpolator.keyValues())
        print(interpolator.currentValue())
        label = GradientLabel(self)
        gradient = QLinearGradient(0, 0, label.width(), 0)
        gradient.setColorAt(0.0, QColorConstants.Blue)
        gradient.setColorAt(0.5, QColorConstants.Green)
        gradient.setColorAt(1.0, QColorConstants.Red)
        label.set_gradient(gradient)


        self.layout.addWidget(label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
