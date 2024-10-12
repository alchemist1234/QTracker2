from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QWheelEvent


class VideoView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fixed_widgets = {}
        self.horizontalScrollBar().valueChanged.connect(self._update_fixed_widgets)
        self.verticalScrollBar().valueChanged.connect(self._update_fixed_widgets)

    def add_fixed_widget(self, widget: QWidget, alignment: Qt.AlignmentFlag):
        widget.setParent(self.viewport())
        self.fixed_widgets[widget] = alignment

    def showEvent(self, event):
        self._update_fixed_widgets()
        super().showEvent(event)

    def resizeEvent(self, event):
        self._update_fixed_widgets()
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
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

    def _update_fixed_widgets(self):
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
