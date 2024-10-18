from typing import Set
import re

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
