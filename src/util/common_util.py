from PySide6.QtGui import QColor
from PySide6.QtCore import QRandomGenerator


def random_color() -> QColor:
    """
    随机颜色
    使用HSL可以通过参数调节颜色的明度范围，排除掉一些过深或过浅的颜色
    :return: QColor
    """
    return QColor.fromHsl(int(QRandomGenerator.global_().bounded(360) % 360),
                          int(QRandomGenerator.global_().bounded(256) % 256),
                          int(QRandomGenerator.global_().bounded(256) % 256))
