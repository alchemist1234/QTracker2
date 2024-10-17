import math

from PySide6.QtWidgets import (QGraphicsEllipseItem, QGraphicsSimpleTextItem,
                               QGraphicsItemGroup, QGraphicsLineItem, QGraphicsItem)
from PySide6.QtGui import QBrush, QColor, QPen, QFont
from PySide6.QtCore import Qt, QPoint

from src.settings.settings import Settings
from src.settings import default_settings


class SettingWidgetHelper(object):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.particle_b = QBrush()
        self.particle_p = QPen()
        self.mark_b = QBrush()
        self.trajectory_p = QPen()

    def particle_brush(self, index: int):
        # brush = QBrush()
        # brush.setStyle(Qt.BrushStyle.SolidPattern)
        # colors = self.settings.list_value(default_settings.particle_color)
        # colors = [QColor(c) for c in colors]
        # brush.setColor(colors[index % len(colors)])
        # return brush
        return self.particle_b

    def particle_pen(self, index: int):
        # pen = QPen()
        # colors = self.settings.list_value(default_settings.particle_color)
        # colors = [QColor(c) for c in colors]
        # pen.setColor(colors[index % len(colors)])
        # pen.setStyle(Qt.PenStyle.SolidLine)
        # pen.setWidth(0)
        # return pen
        return self.particle_p

    def mark_brush(self, index: int):
        # if self.settings.boolean_value(default_settings.same_mark_color_with_particle):
        #     return self.particle_brush(index)
        # else:
        #     brush = QBrush()
        #     colors = self.settings.list_value(default_settings.mark_color)
        #     colors = [QColor(c) for c in colors]
        #     brush.setStyle(Qt.BrushStyle.SolidPattern)
        #     brush.setColor(colors[index % len(colors)])
        #     return brush
        return self.mark_b

    def trajectory_pen(self, index: int):
        # if self.settings.boolean_value(default_settings.same_trajectory_color_with_particle):
        #     return self.particle_pen(index)
        # else:
        #     pen = QPen()
        #     colors = self.settings.list_value(default_settings.trajectory_color)
        #     colors = [QColor(c) for c in colors]
        #     pen.setStyle(Qt.PenStyle.SolidLine)
        #     pen.setColor(colors[index % len(colors)])
        #     pen.setWidth(self.settings.int_value(default_settings.trajectory_size))
        #     pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        #     pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        #     return pen
        return self.trajectory_p

    def visible(self, setting_item: default_settings.SettingItem, index: int):
        index_filter = self.settings.list_value(default_settings.index_filter)
        return self.settings.boolean_value(setting_item) and (index in index_filter or len(index_filter) == 0)


class ParticleItem(QGraphicsEllipseItem):

    def __init__(self, settings: Settings, index: int, x, y):
        radius = settings.int_value(default_settings.particle_size)
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
        super().__init__(prefix + str(index) + suffix)
        self.settings = settings
        self.settings_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        font = QFont(self.settings.value(default_settings.mark_font))
        font.setPixelSize(self.settings.int_value(default_settings.mark_size))
        self.setFont(font)
        self.setBrush(self.settings_helper.mark_brush(index))
        radius = self.settings.int_value(default_settings.particle_size)
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
        super().__init__()
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setX(x)
        self.setY(y)
        if self.setting_helper.visible(default_settings.show_particle, index):
            self.particle = ParticleItem(settings, index, x, y)
            self.addToGroup(self.particle)
        if self.setting_helper.visible(default_settings.show_mark, index):
            self.mark = MarkItem(settings, index, x, y)
            self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)


class TrajectoryItem(QGraphicsLineItem):
    def __init__(self, settings: Settings, index: int, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.settings = settings
        self.index = index
        self.settings_helper = SettingWidgetHelper(settings)
        self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.setPen(self.settings_helper.trajectory_pen(index))

    def update_pen(self):
        self.setPen(self.settings_helper.trajectory_pen(self.index))
