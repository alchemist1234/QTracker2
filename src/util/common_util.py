from typing import Set, Sequence
import re
import math

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


def split_indexes_text(text: str) -> Set[int]:
    """
    将索引字符串分割成索引集合
    ','和' '为分隔符
    索引支持'-'连续选择
    :param text: 索引字符串
    :return: 索引集合
    """
    arr = re.split('[, ]', text)
    indexes = set()
    for i in arr:
        pos = i.find('-')
        if pos > 0:
            left = i[:pos]
            right = i[pos + 1:]
            if left.isdecimal() and right.isdecimal():
                min_index = min(int(left), int(right))
                max_index = max(int(left), int(right))
                indexes.update(range(min_index, max_index + 1))
        else:
            if i.isdecimal():
                indexes.add(int(i))
    return indexes


def angle_to_y(x1, y1, x2, y2) -> float:
    """
    计算 A(x1, y1) -> B(x2, y2)向量与y轴的夹角，y轴正方向为0
    :return: a，b两点连线与y轴正方向夹角[0,360)
    """
    dx = x2 - x1
    dy = y2 - y1
    if dy == 0:
        return 0 if dx == 0 else 90 if dx > 0 else 270
    arc = math.atan(dx / dy)
    angle = math.degrees(arc)
    if dy < 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle


def distance(x1, y1, x2, y2) -> float:
    """
    计算两点直线距离
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
