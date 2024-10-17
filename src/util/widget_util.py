from typing import Union, List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap, QMouseEvent
from PySide6.QtWidgets import QLabel


class ColorLabel(QLabel):
    clicked = Signal(QMouseEvent)

    def __init__(self, parent=None):
        super(ColorLabel, self).__init__(parent=parent)
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.painter = QPainter()
        self._colors = []

    @property
    def colors(self):
        return self._colors

    def set_color(self, colors: Union[List[QColor], QColor]):
        if not isinstance(colors, list):
            colors = [colors]
        self._colors = colors
        size = len(colors)
        base_color_width = int(self.width() / size)
        base_color_width = 1 if base_color_width < 1 else base_color_width
        unfilled_width = self.width() - base_color_width * size
        pixmap = QPixmap(self.width(), self.height())
        filled_width = 0
        self.painter.begin(pixmap)
        for color in colors:
            color_width = base_color_width
            if unfilled_width > 0:
                color_width += 1
                unfilled_width -= 1
            self.brush.setColor(color)
            self.painter.fillRect(filled_width, 0, color_width, self.height(), self.brush)
            filled_width += color_width
        self.painter.end()
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(ev)
        super(ColorLabel, self).mousePressEvent(ev)
