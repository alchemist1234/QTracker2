import math
from typing import Union, List

from PySide6.QtCore import Qt, Signal, QPoint, QRectF, QPropertyAnimation, QPointF
from PySide6.QtGui import QBrush, QPainter, QPixmap, QMouseEvent, QColor, QFont, QPen, QLinearGradient, QColorConstants
from PySide6.QtWidgets import (QLabel, QWidget, QHBoxLayout, QListView, QSizePolicy, QSpacerItem, QGraphicsEllipseItem,
                               QGraphicsItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsItemGroup,
                               QGraphicsRectItem)

from src.model.enums import FrameLabelPos
from src.model.models import GradientColor
from src.settings.default_settings import SettingKey
from src.settings.settings import Settings
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


class GradientLabel(QLabel):
    clicked = Signal(QMouseEvent)

    def __init__(self, parent=None):
        super(GradientLabel, self).__init__(parent=parent)
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.LinearGradientPattern)
        self.painter = QPainter()
        self._colors = []

    @property
    def colors(self) -> List[GradientColor]:
        return self._colors

    def set_gradient(self, gradient_colors: Union[List[GradientColor], GradientColor]) -> None:
        if not isinstance(gradient_colors, list):
            gradient_colors = [gradient_colors]
        self._colors = gradient_colors
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for gradient_color in gradient_colors:
            gradient.setColorAt(gradient_color.pos, gradient_color.color)
        self.brush = QBrush(gradient)
        pixmap = QPixmap(self.width(), self.height())
        self.painter.begin(pixmap)
        self.painter.setBrush(self.brush)
        self.painter.drawRect(0, 0, self.width(), self.height())
        self.painter.end()
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(ev)
        super(GradientLabel, self).mousePressEvent(ev)


class Ui_GradientItem(object):
    def __init__(self, parent: QWidget, gradient_color: GradientColor, height: int):
        """
        ListWidget中用来显示颜色的Item UI
        :param parent: 父对象
        :param gradient_color: 颜色
        :param height: 色块高度
        """
        margin = 4
        self.layout = QHBoxLayout(parent)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(margin)
        self.lb_pos = QLabel()
        self.lb_pos.setText(str(gradient_color.pos))
        self.color_name = QColor(gradient_color.color).name()
        self.lb_color = GradientLabel(parent)
        self.lb_color.setFixedSize(64, height - 2 * margin)
        self.lb_color.set_gradient([gradient_color])
        self.lb_color_name = QLabel(parent)
        self.lb_color_name.setText(self.color_name)
        self.layout.addWidget(self.lb_pos)
        self.layout.addWidget(self.lb_color)
        self.layout.addWidget(self.lb_color_name)
        self.layout.addItem(QSpacerItem(20, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


class GradientItem(QWidget):
    def __init__(self, parent: QListView, gradient_color: GradientColor, height: int):
        """
        ListWidget中用来显示颜色的Item
        :param parent: ListWidget父对象
        :param gradient_color: 颜色
        :param height: 色块高度
        """
        super().__init__(parent)
        self.ui = Ui_GradientItem(self, gradient_color, height)
        self.gradient_color = gradient_color
        self.color_name = QColor(gradient_color.color).name()

    def update_color(self, gradient_color: GradientColor) -> None:
        """
        更新颜色
        :param gradient_color: 颜色
        """
        self.gradient_color = gradient_color
        self.color_name = QColor(gradient_color.color).name()
        self.ui.lb_color.set_gradient(gradient_color)
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
        radius = settings.int_value(SettingKey.particle_size)
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.settings = settings
        self.index = index
        self.center_x = x
        self.center_y = y
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setToolTip(str(index))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setWidth(0)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.setBrush(brush)
        self.refresh()

    def center(self) -> QPoint:
        """
        获取粒子中心位置
        """
        return QPoint(self.center_x, self.center_y)

    def refresh(self) -> None:
        """
        刷新显示
        """
        # 颜色
        colors = self.settings.list_value(SettingKey.particle_color)
        colors = [QColor(c) for c in colors]
        color = colors[self.index % len(colors)]
        # 需要重新设置brush和pen，直接self.brush().setColor()不会生效
        brush = self.brush()
        brush.setColor(color)
        self.setBrush(brush)
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        # 大小
        size = self.settings.int_value(SettingKey.particle_size)
        self.setRect(QRectF(self.center_x - size, self.center_y - size, size * 2, size * 2))
        # 显示/隐藏
        show_particle = self.settings.boolean_value(SettingKey.show_particle)
        self.setVisible(show_particle)


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
        self.index = index
        self.center_x = center_x
        self.center_y = center_y
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.setBrush(brush)
        self.refresh()

    def refresh(self):
        """
        刷新显示
        """
        # 字体
        font = QFont(self.settings.value(SettingKey.mark_font))
        font.setPointSize(self.settings.int_value(SettingKey.mark_size))
        self.setFont(font)
        # 颜色
        same_color_with_particle = self.settings.boolean_value(SettingKey.same_mark_color_with_particle)
        if same_color_with_particle:
            colors = self.settings.list_value(SettingKey.particle_color)
        else:
            colors = self.settings.list_value(SettingKey.mark_color)
        colors = [QColor(c) for c in colors]
        color = colors[self.index % len(colors)]
        brush = self.brush()
        brush.setColor(color)
        self.setBrush(brush)
        # 位置
        radius = self.settings.int_value(SettingKey.particle_size)
        x = self.center_x - radius - self.boundingRect().width()
        y = self.center_y - radius - self.boundingRect().height()
        if x < 0:
            x = self.center_x + radius
        if y < 0:
            y = self.center_y + radius
        self.setX(x)
        self.setY(y)
        # 显示/隐藏
        show_mark = self.settings.boolean_value(SettingKey.show_mark)
        self.setVisible(show_mark)


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
        self.index = index
        self.setX(x)
        self.setY(y)
        self.particle = ParticleItem(settings, index, x, y)
        self.addToGroup(self.particle)
        self.mark = MarkItem(settings, index, x, y)
        self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges, True)

    def refresh(self) -> None:
        """
        刷新粒子和标记组
        """
        # 必须先解组，再成组，不然位置会出现问题
        self.removeFromGroup(self.particle)
        self.removeFromGroup(self.mark)
        self.particle.refresh()
        self.mark.refresh()
        self.addToGroup(self.particle)
        self.addToGroup(self.mark)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            scene = self.scene()
            if scene:
                rect = scene.sceneRect()
                if not rect.contains(value):
                    value.setX(min(rect.right(), max(value.x(), rect.left())))
                    value.setY(min(rect.bottom(), max(value.y(), rect.top())))
                    return value
        return super().itemChange(change, value)


class TrajectoryItem(QGraphicsLineItem):
    max_duration = 1000

    def __init__(self, settings: Settings, index: int, x1, y1, x2, y2, frame_interval, pre_speed: float = None):
        """
        轨迹Item（一段）
        :param settings: 配置信息
        :param index: 粒子序号
        :param x1: 起点x坐标
        :param y1: 起点y坐标
        :param x2: 终点x坐标
        :param y2: 终点y坐标
        :param frame_interval: 帧间隔
        """
        super().__init__(x1, y1, x2, y2)
        self.settings = settings
        self.index = index
        self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.speed = self.distance / frame_interval
        self.pre_speed = pre_speed
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.setPen(pen)
        self._interpolated = self.create_interpolated()
        self._max_color_speed = self.settings.float_value(SettingKey.max_color_speed)
        self._min_color_speed = self.settings.float_value(SettingKey.min_color_speed)

        self.refresh()

    # 所有轨迹共用的速度颜色插值器(仅在轨迹速度颜色设置变化时重建),
    # 避免每条轨迹各持有一个 QPropertyAnimation 造成内存与构造开销
    _shared_interpolator = None
    _shared_interpolator_key: tuple = ()

    def create_interpolated(self) -> QPropertyAnimation:
        """获取速度颜色插值器(所有TrajectoryItem共享, 速度颜色设置变化时自动重建)"""
        speed_colors = self.settings.value(SettingKey.trajectory_speed_color) or []
        key = tuple((float(color.pos), str(color.color)) for color in speed_colors)
        cls = type(self)
        if cls._shared_interpolator is None or cls._shared_interpolator_key != key:
            interpolated = QPropertyAnimation()
            interpolated.setDuration(1000)
            for speed_color in speed_colors:
                interpolated.setKeyValueAt(speed_color.pos, speed_color.color)
            cls._shared_interpolator = interpolated
            cls._shared_interpolator_key = key
        return cls._shared_interpolator

    def get_speed_color(self, speed: float) -> QColor:
        speed = min(self._max_color_speed, speed)
        speed = max(self._min_color_speed, speed)
        pos = (speed - self._min_color_speed) / (self._max_color_speed - self._min_color_speed)
        self._interpolated.setCurrentTime(int(pos * self.max_duration))
        return self._interpolated.currentValue()

    def refresh(self):
        """
        刷新显示
        """
        # 颜色
        enable_speed_color = self.settings.boolean_value(SettingKey.trajectory_color_with_speed)
        pen = self.pen()
        if enable_speed_color:
            gradient = QLinearGradient(self.line().x1(), self.line().y1(), self.line().x2(), self.line().y2())
            end_color = self.get_speed_color(self.speed)
            start_color = end_color if self.pre_speed is None else self.get_speed_color(self.pre_speed)
            gradient.setColorAt(0, start_color)
            gradient.setColorAt(1, end_color)
            brush = QBrush(gradient)
            brush.setStyle(Qt.BrushStyle.LinearGradientPattern)
            pen.setBrush(brush)
        else:
            color = self.__choose_color()
            pen.setColor(color)
        self.setPen(pen)
        # 显示/隐藏
        show_trajectory = self.settings.boolean_value(SettingKey.show_trajectory)
        self.setVisible(show_trajectory)

    def __choose_color(self):
        same_color_with_particle = self.settings.boolean_value(SettingKey.same_trajectory_color_with_particle)
        if same_color_with_particle:
            colors = self.settings.list_value(SettingKey.particle_color)
        else:
            colors = self.settings.list_value(SettingKey.trajectory_color)
        colors = [QColor(c) for c in colors]
        return colors[self.index % len(colors)]


class FrameLabelItem(QGraphicsSimpleTextItem):
    def __init__(self, settings: Settings, index: int, x=0, y=0):
        """
        轨迹Item（一段）
        :param settings: 配置信息
        :param index: 粒子序号
        :param x: 起点x坐标
        :param y: 起点y坐标
        """
        super().__init__(str(index))
        self.settings = settings
        self.index = index
        self.setX(x)
        self.setY(y)
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.setBrush(brush)
        self.refresh()

    def refresh(self, width: int = None, height: int = None):
        """
        刷新显示
        :param width 图片宽度, 用于计算帧标签在图片右侧时的位置
        :param height 图片高度, 用于计算帧标签在图片下方时的位置
        """
        # 字体
        font = QFont(self.settings.value(SettingKey.frame_label_font))
        font.setPointSize(self.settings.int_value(SettingKey.frame_label_size))
        self.setFont(font)
        # 颜色
        colors = self.settings.list_value(SettingKey.frame_label_color)
        colors = [QColor(c) for c in colors]
        color = colors[self.index % len(colors)]
        brush = self.brush()
        brush.setColor(color)
        self.setBrush(brush)
        # 显示/隐藏
        show_frame_label = self.settings.boolean_value(SettingKey.show_frame_label)
        self.setVisible(show_frame_label)
        pos = self.settings.int_value(SettingKey.frame_label_pos)
        if not width:
            # 没有传入图片宽、高时，默认在左上角
            return
        # 设置标签位置
        if pos == FrameLabelPos.LEFT_TOP.value:
            self.setX(0)
            self.setY(0)
        elif pos == FrameLabelPos.LEFT_BOTTOM.value:
            self.setX(0)
            self.setY(height - self.boundingRect().height())
        elif pos == FrameLabelPos.RIGHT_TOP.value:
            self.setX(width - self.boundingRect().width())
            self.setY(0)
        else:
            self.setX(width - self.boundingRect().width())
            self.setY(height - self.boundingRect().height())


class CropRectItem(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        pen = QPen()
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setColor(QColorConstants.Green)
        self.setPen(pen)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            scene = self.scene()
            if scene:
                rect = scene.sceneRect()
                bounding = self.boundingRect()
                left_top = QPointF(value.x() + bounding.left(), value.y() + bounding.top())
                right_bottom = QPointF(value.x() + bounding.right(), value.y() + bounding.bottom())
                if not rect.contains(left_top) or not rect.contains(right_bottom):
                    value.setX(min(rect.right() - bounding.width(), max(value.x(), rect.left())))
                    value.setY(min(rect.bottom() - bounding.height(), max(value.y(), rect.top())))
                    return value
        return super().itemChange(change, value)
