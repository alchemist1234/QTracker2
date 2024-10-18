import math
from typing import Union, List

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QBrush, QPainter, QPixmap, QMouseEvent
from PySide6.QtWidgets import (QLabel, QWidget, QHBoxLayout, QListView, QSizePolicy, QSpacerItem, QGraphicsEllipseItem,
                               QGraphicsItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsItemGroup)

from src.settings.default_settings import *
from src.settings.settings import Settings
from src.util.graphic_util import SettingWidgetHelper
from src.ui.view_btn_grp_ui import Ui_wid_button_group


class ViewButtonGroup(QWidget):
    def __init__(self, parent=None):
        """
        VideoView容器中的固定按钮组
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui = Ui_wid_button_group()
        self.ui.setupUi(self)
        self.resize(36, 260)


class ColorLabel(QLabel):
    """
    色块标签
    """
    clicked = Signal(QMouseEvent)

    def __init__(self, parent=None):
        super(ColorLabel, self).__init__(parent=parent)
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.painter = QPainter()
        self._colors = []

    @property
    def colors(self) -> List[QColor]:
        """
        当前颜色
        :return: 颜色列表
        """
        return self._colors

    def set_color(self, colors: Union[List[QColor], QColor]) -> None:
        """
        设置颜色并更新显示
        :param colors: 需要更新的颜色
        """
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
        """
        标签点击事件
        :param ev: QMouseEvent
        """
        self.clicked.emit(ev)
        super(ColorLabel, self).mousePressEvent(ev)


class Ui_ColorItem(object):
    def __init__(self, parent: QWidget, color: QColor, height: int):
        """
        ListWidget中用来显示颜色的Item UI
        :param parent: 父对象
        :param color: 颜色
        :param height: 色块高度
        """
        margin = 4
        self.layout = QHBoxLayout(parent)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(margin)
        self.color_name = QColor(color).name()
        self.lb_color = ColorLabel(parent)
        self.lb_color.setFixedSize(64, height - 2 * margin)
        self.lb_color.set_color([color])
        self.lb_color_name = QLabel(parent)
        self.lb_color_name.setText(self.color_name)
        self.layout.addWidget(self.lb_color)
        self.layout.addWidget(self.lb_color_name)
        self.layout.addItem(QSpacerItem(20, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


class ColorItem(QWidget):
    def __init__(self, parent: QListView, color: QColor, height: int):
        """
        ListWidget中用来显示颜色的Item
        :param parent: ListWidget父对象
        :param color: 颜色
        :param height: 色块高度
        """
        super().__init__(parent)
        self.ui = Ui_ColorItem(self, color, height)
        self.color = color
        self.color_name = QColor(color).name()

    def update_color(self, color: QColor) -> None:
        """
        更新颜色
        :param color: 颜色
        """
        self.color = color
        self.color_name = QColor(color).name()
        self.ui.lb_color.set_color(color)
        self.ui.lb_color_name.setText(self.color_name)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """
        双击事件
        :param event: QMouseEvent
        """
        self.parent().mouseDoubleClickEvent(event)


class ParticleItem(QGraphicsEllipseItem):
    def __init__(self, settings: Settings, index: int, x, y):
        """
        粒子Item
        :param settings: 配置信息
        :param index: 粒子序号
        :param x: x坐标
        :param y: y坐标
        """
        radius = settings.int_value(particle_size)
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.settings = settings
        self.settings_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setToolTip(str(index))
        self.setBrush(self.settings_helper.particle_brush(index))
        self.setPen(self.settings_helper.particle_pen(index))
        self.mark = None

    def center(self) -> QPoint:
        rect = self.rect()
        return QPoint(int(rect.x() + rect.width() / 2), int(rect.y() + rect.height() / 2))


class MarkItem(QGraphicsSimpleTextItem):
    def __init__(self, settings: Settings, index: int, center_x, center_y, prefix: str = '', suffix: str = ''):
        """
        标记Item
        :param settings: 设置信息
        :param index: 粒子序号
        :param center_x: 粒子中心位置x坐标
        :param center_y: 粒子中心位置y坐标
        :param prefix: 标记前缀
        :param suffix: 标记后缀
        """
        super().__init__(prefix + str(index) + suffix)
        self.settings = settings
        self.settings_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        font = QFont(self.settings.value(mark_font))
        font.setPixelSize(self.settings.int_value(mark_size))
        self.setFont(font)
        self.setBrush(self.settings_helper.mark_brush(index))
        radius = self.settings.int_value(particle_size)
        x = center_x - radius - self.boundingRect().width()
        y = center_y - radius - self.boundingRect().height()
        if x < 0:
            x = center_x + radius
        if y < 0:
            y = center_y + radius
        self.setX(x)
        self.setY(y)


class ParticleGroup(QGraphicsItemGroup):
    def __init__(self, settings: Settings, index: int, x, y):
        """
        粒子组，将粒子与标记组合在一起，方便同时移动
        :param settings: 配置信息
        :param index: 粒子序号
        :param x: x坐标
        :param y: y坐标
        """
        super().__init__()
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setX(x)
        self.setY(y)
        self.particle = ParticleItem(settings, index, x, y)
        self.addToGroup(self.particle)
        self.mark = MarkItem(settings, index, x, y)
        self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

    def set_particle_visible(self, visible: bool):
        self.particle.setVisible(visible)

    def set_mark_visible(self, visible: bool):
        self.mark.setVisible(visible)


class TrajectoryItem(QGraphicsLineItem):
    def __init__(self, settings: Settings, index: int, x1, y1, x2, y2):
        """
        轨迹Item（一段）
        :param settings: 配置信息
        :param index: 粒子序号
        :param x1: 起点x坐标
        :param y1: 起点y坐标
        :param x2: 终点x坐标
        :param y2: 终点y坐标
        """
        super().__init__(x1, y1, x2, y2)
        self.settings = settings
        self.index = index
        self.settings_helper = SettingWidgetHelper(settings)
        self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.setPen(self.settings_helper.trajectory_pen(index))

    def update_pen(self):
        self.setPen(self.settings_helper.trajectory_pen(self.index))
