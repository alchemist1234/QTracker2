from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QPoint, Slot
from PySide6.QtGui import QWheelEvent


class VideoView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fixed_widgets = {}
        # 滚动条滑动没有对应事件，通过值改变信号连接
        self.horizontalScrollBar().valueChanged.connect(self._update_fixed_widgets)
        self.verticalScrollBar().valueChanged.connect(self._update_fixed_widgets)

    def add_fixed_widget(self, widget: QWidget, alignment: Qt.AlignmentFlag) -> None:
        """
        添加固定控件
        :param widget: 控件
        :param alignment: 对齐方式
        """
        widget.setParent(self.viewport())
        self.fixed_widgets[widget] = alignment

    def showEvent(self, event):
        """
        显示事件
        """
        self._update_fixed_widgets()
        super().showEvent(event)

    def resizeEvent(self, event):
        """
        窗口缩放事件
        """
        self._update_fixed_widgets()
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        鼠标滚动事件
        """
        mouse_pos = event.position()
        scene_pos = self.mapToScene(mouse_pos.toPoint())
        view_w = self.viewport().width()
        view_h = self.viewport().height()
        h_scale = mouse_pos.x() / view_w
        v_scale = mouse_pos.y() / view_h

        wheel_delta = event.angleDelta().y()
        if wheel_delta > 0:
            self.scale(1.2, 1.2)
        else:
            self.scale(1 / 1.2, 1 / 1.2)
        view_point = self.transform().map(scene_pos)
        self.horizontalScrollBar().setValue(int(view_point.x() - view_w * h_scale))
        self.verticalScrollBar().setValue(int(view_point.y() - view_h * v_scale))
        self._update_fixed_widgets()

    @Slot()
    def _update_fixed_widgets(self) -> None:
        """
        渲染固定控件
        """
        r = self.viewport().rect()
        for w, a in self.fixed_widgets.items():
            p = QPoint()

            if a & Qt.AlignmentFlag.AlignHCenter:
                p.setX((r.width() - w.width()) / 2)
            elif a & Qt.AlignmentFlag.AlignRight:
                p.setX(r.width() - w.width())

            if a & Qt.AlignmentFlag.AlignVCenter:
                p.setY((r.height() - w.height()) / 2)
            elif a & Qt.AlignmentFlag.AlignBottom:
                p.setY(r.height() - w.height())
            w.move(p)
