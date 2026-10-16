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
    # 饱和度与亮度限制在中间范围, 排除掉一些过深或过浅的颜色
    hue = int(QRandomGenerator.global_().bounded(360))
    saturation = 128 + int(QRandomGenerator.global_().bounded(128))
    lightness = 80 + int(QRandomGenerator.global_().bounded(120))
    return QColor.fromHsl(hue, saturation, lightness)


def split_indexes_text(text: str) -> Set[int]:
    """
    将索引字符串分割成索引集合
    ','、空白字符(空格/制表符/换行)为分隔符
    索引支持'-'连续选择
    :param text: 索引字符串
    :return: 索引集合
    """
    arr = re.split(r'[, \t\r\n]+', text)
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
    # atan2覆盖全部象限与零向量, 免去逐象限特判
    return math.degrees(math.atan2(dx, dy)) % 360


def distance(x1, y1, x2, y2) -> float:
    """
    计算两点直线距离
    """
    return math.hypot(x2 - x1, y2 - y1)
