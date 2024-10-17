from typing import List, Optional

from PySide6.QtCore import Signal, QSize, QModelIndex
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDialog, QListWidgetItem, QColorDialog

from src.view.custom_widget import ColorLabel, ColorItem
from src.ui.color_editor_ui import Ui_dialog_color_editor
from src.util.common_util import random_color

class ColorEditor(QDialog):
    default_color = QColor(255, 0, 0)
    sig_color_changed = Signal(ColorLabel, list)

    def __init__(self, parent: QDialog, label: Optional[ColorLabel] = None):
        super().__init__(parent)
        self.parent = parent
        self.label = label
        self.ui = Ui_dialog_color_editor()
        self.ui.setupUi(self)

        self.ui.btn_add.clicked.connect(lambda x: self.add_color())
        self.ui.lw_colors.doubleClicked.connect(self.edit_color)

    def add_colors(self, colors: List[QColor]):
        for color in colors:
            self.add_color(color)

    def add_color(self, color: Optional[QColor] = None):
        color = random_color() if color is None else color
        item = QListWidgetItem(self.ui.lw_colors)
        size = self.ui.lw_colors.gridSize()
        widget = ColorItem(self.ui.lw_colors, color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.ui.lw_colors.addItem(item)
        self.ui.lw_colors.setItemWidget(item, widget)

    def edit_color(self, model_index: QModelIndex):
        widget = self.ui.lw_colors.indexWidget(model_index)
        origin_color = widget.color
        color = QColorDialog.getColor(origin_color, self)
        if color.isValid():
            widget.update_color(color)

    def get_colors(self):
        colors = []
        for i in range(self.ui.lw_colors.count()):
            item = self.ui.lw_colors.item(i)
            color_widget = self.ui.lw_colors.itemWidget(item)
            colors.append(color_widget.color)
        return colors

    def accept(self) -> None:
        self.sig_color_changed.emit(self.label, self.get_colors())
        super(ColorEditor, self).accept()
