import sys
from typing import Union, List, Optional

from PySide6.QtWidgets import (QDialog, QHBoxLayout, QListWidget, QListView, QPushButton, QDialogButtonBox,
                               QApplication, QLabel, QSizePolicy, QWidget, QSpacerItem, QListWidgetItem, QColorDialog,
                               QVBoxLayout)
from PySide6.QtGui import QColor, QMouseEvent, QBrush, QPainter, QPixmap
from PySide6.QtCore import Qt, QSize, Signal, QModelIndex, Slot, QRandomGenerator


class ColorLabel(QLabel):
    clicked = Signal(QMouseEvent)

    def __init__(self, parent=None):
        super(ColorLabel, self).__init__(parent=parent)
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.painter = QPainter()
        self._colors = []

    @property
    def colors(self):
        return self._colors

    def set_color(self, colors: Union[List[QColor], QColor]):
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
        self.clicked.emit(ev)
        super(ColorLabel, self).mousePressEvent(ev)


class ColorEditorUi(object):
    def __init__(self, color_editor: QDialog):
        self.color_editor = color_editor
        self.hbox_base = QHBoxLayout(color_editor)
        self.lv_color = QListWidget(color_editor)

        # self.lv_color.dropEvent = self.drop_event
        self.lv_color.setDragDropMode(QListView.DragDropMode.InternalMove)

        self.lv_color.setMovement(QListView.Movement.Snap)
        self.lv_color.setGridSize(QSize(100, 32))
        self.lv_color.setViewMode(QListView.ViewMode.ListMode)

        self.bt_add = QPushButton(color_editor)
        self.bt_delete = QPushButton(color_editor)
        self.bt_random = QPushButton(color_editor)
        self.bt_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                       QDialogButtonBox.StandardButton.Cancel,
                                       Qt.Orientation.Vertical, color_editor)
        self.bt_box.addButton(self.bt_add, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.addButton(self.bt_delete, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.addButton(self.bt_random, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.accepted.connect(color_editor.accept)
        self.bt_box.rejected.connect(color_editor.reject)

        self.hbox_base.addWidget(self.lv_color)
        self.hbox_base.addWidget(self.bt_box)

        self.translate()

    def translate(self):
        self.bt_add.setText('add')
        self.bt_delete.setText('delete')
        self.bt_random.setText('random')

    def drop_event(self, e):
        print(e)


class ColorWidgetUi(object):
    def __init__(self, parent: QWidget, color: QColor, height: int):
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


class ColorWidget(QWidget):
    def __init__(self, parent: QListView, color: QColor, height: int):
        super().__init__(parent)
        self.ui = ColorWidgetUi(self, color, height)
        self.color = color
        self.color_name = QColor(color).name()

    def update_color(self, color: QColor):
        self.color = color
        self.color_name = QColor(color).name()
        self.ui.lb_color.set_color(color)
        self.ui.lb_color_name.setText(self.color_name)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.parent().mouseDoubleClickEvent(event)


class ColorEditor(QDialog):
    default_color = QColor(255, 0, 0)
    sig_color_changed = Signal(ColorLabel, list)

    def __init__(self, parent: QDialog, label: Optional[ColorLabel] = None):
        super().__init__(parent)
        self.parent = parent
        self.label = label
        self.ui = ColorEditorUi(self)

        self.ui.bt_add.clicked.connect(lambda x: self.add_color())
        self.ui.lv_color.doubleClicked.connect(self.edit_color)

    def add_colors(self, colors: List[QColor]):
        for color in colors:
            self.add_color(color)

    def add_color(self, color: Optional[QColor] = None):
        color = random_color() if color is None else color
        item = QListWidgetItem(self.ui.lv_color)
        size = self.ui.lv_color.gridSize()
        widget = ColorWidget(self.ui.lv_color, color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.ui.lv_color.addItem(item)
        self.ui.lv_color.setItemWidget(item, widget)

    def edit_color(self, model_index: QModelIndex):
        widget = self.ui.lv_color.indexWidget(model_index)
        origin_color = widget.color
        color = QColorDialog.getColor(origin_color, self)
        if color.isValid():
            widget.update_color(color)

    def get_colors(self):
        colors = []
        for i in range(self.ui.lv_color.count()):
            item = self.ui.lv_color.item(i)
            color_widget = self.ui.lv_color.itemWidget(item)
            colors.append(color_widget.color)
        return colors

    def accept(self) -> None:
        self.sig_color_changed.emit(self.label, self.get_colors())
        super(ColorEditor, self).accept()


def random_color():
    return QColor.fromHsl(QRandomGenerator.global_().bounded(360) % 360,
                          QRandomGenerator.global_().bounded(256) % 256,
                          QRandomGenerator.global_().bounded(200) % 200)


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 300)
        self.layout = QVBoxLayout()
        self.label = ColorLabel()
        self.label.set_color(random_color())
        self.label.clicked.connect(lambda x: self.edit_color(self.label))
        self.btn = QPushButton('Edit')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def edit_color(self, label: ColorLabel):
        editor = ColorEditor(self, label)
        editor.add_colors(label.colors)
        editor.sig_color_changed.connect(self.update_color)
        editor.exec()

    @Slot(ColorLabel, list)
    def update_color(self, label: ColorLabel, colors: List[QColor]):
        label.set_color(colors)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
