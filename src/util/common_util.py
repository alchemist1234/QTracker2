from PySide6.QtGui import QColor
from PySide6.QtCore import QRandomGenerator


def random_color():
    return QColor.fromHsl(int(QRandomGenerator.global_().bounded(360) % 360),
                          int(QRandomGenerator.global_().bounded(256) % 256),
                          int(QRandomGenerator.global_().bounded(200) % 200))
