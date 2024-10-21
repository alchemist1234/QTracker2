from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtCore import Qt

from src.settings.settings import Settings
from src.settings.default_settings import SettingKey


class SettingWidgetHelper(object):
    def __init__(self, settings: Settings):
        """
        用于方便获取绘制图像用的QPen、QBrush
        :param settings:
        """
        self.settings = settings

    def particle_brush(self, index: int) -> QBrush:
        """
        绘制粒子的QBrush
        :param index: 粒子序号
        :return: QBrush
        """
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        colors = self.settings.list_value(SettingKey.particle_color)
        colors = [QColor(c) for c in colors]
        brush.setColor(colors[index % len(colors)])
        return brush

    def particle_pen(self, index: int) -> QPen:
        """
        绘制粒子边框的QPen
        :param index: 粒子序号
        :return: QPen
        """
        pen = QPen()
        colors = self.settings.list_value(SettingKey.particle_color)
        colors = [QColor(c) for c in colors]
        pen.setColor(colors[index % len(colors)])
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setWidth(0)
        return pen

    def mark_brush(self, index: int) -> QBrush:
        """
        绘制标记的QBrush
        :param index: 粒子序号
        :return: QBrush
        """
        if self.settings.boolean_value(SettingKey.same_mark_color_with_particle):
            return self.particle_brush(index)
        else:
            brush = QBrush()
            colors = self.settings.list_value(SettingKey.mark_color)
            colors = [QColor(c) for c in colors]
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            brush.setColor(colors[index % len(colors)])
            return brush

    def frame_label_brush(self, index: int) -> QBrush:
        """
        绘制帧号的QBrush
        :param index: 粒子序号
        :return: QBrush
        """
        brush = QBrush()
        colors = self.settings.list_value(SettingKey.frame_label_color)
        colors = [QColor(c) for c in colors]
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        brush.setColor(colors[index % len(colors)])
        return brush

    def trajectory_pen(self, index: int) -> QPen:
        """
        绘制轨迹的QPen
        :param index: 粒子序号
        :return: QPen
        """
        if self.settings.boolean_value(SettingKey.same_trajectory_color_with_particle):
            return self.particle_pen(index)
        else:
            pen = QPen()
            colors = self.settings.list_value(SettingKey.trajectory_color)
            colors = [QColor(c) for c in colors]
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setColor(colors[index % len(colors)])
            pen.setWidth(self.settings.int_value(SettingKey.trajectory_width))
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            return pen

    def visible(self, setting_key: SettingKey, index: int) -> bool:
        """
        控制粒子显示/隐藏
        :param setting_key: 显示粒子/显示标记/显示轨迹
        :param index: 粒子序号
        :return: 显示/隐藏粒子
        """
        index_filter = self.settings.list_value(SettingKey.index_filter)
        return self.settings.boolean_value(setting_key) and (index in index_filter or len(index_filter) == 0)


