from typing import List, Optional

from PySide6.QtCore import Signal, QSize, QModelIndex, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDialog, QListWidgetItem, QColorDialog, QInputDialog

from src.model.models import GradientColor
from src.view.custom_widget import GradientLabel, ColorItem, GradientItem
from src.ui.gradient_editor_ui import Ui_dialog_gradient_editor
from src.util.common_util import random_color


class GradientEditor(QDialog):
    # 颜色被改变信号，用于更新外部组件颜色
    sig_gradient_changed = Signal(GradientLabel, list)

    def __init__(self, parent: QDialog, label: Optional[GradientLabel] = None):
        super().__init__(parent)
        self.parent = parent
        self.label = label
        self.ui = Ui_dialog_gradient_editor()
        self.ui.setupUi(self)

        self.ui.btn_add.clicked.connect(lambda x: self.add_color())
        self.ui.btn_delete.clicked.connect(self.delete_color)
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.lw_colors.doubleClicked.connect(self.edit_color)

    def add_colors(self, colors: List[GradientColor]):
        """
        添加多个颜色
        :param colors: 颜色列表
        """
        for color in colors:
            self.add_color(color)

    @Slot(QColor)
    def add_color(self, color: Optional[GradientColor] = None) -> None:
        """
        添加颜色
        :param color: 待添加的颜色
        """
        if color is None:
            pos, _ = QInputDialog.getDouble(self, '设置颜色位置', '颜色位置(0-1)', 0)
        else:
            pos = color.pos
        color = GradientColor(pos, random_color()) if color is None else color
        item = QListWidgetItem(self.ui.lw_colors)
        size = self.ui.lw_colors.gridSize()
        widget = GradientItem(self.ui.lw_colors, color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.ui.lw_colors.addItem(item)
        self.ui.lw_colors.setItemWidget(item, widget)

    @Slot(QModelIndex)
    def edit_color(self, model_index: QModelIndex) -> None:
        """
        编辑颜色
        :param model_index: QModelIndex
        """
        widget = self.ui.lw_colors.indexWidget(model_index)
        origin_color = widget.gradient_color
        color = QColorDialog.getColor(origin_color.color, self)
        if color.isValid():
            widget.update_color(color)

    @Slot()
    def delete_color(self) -> None:
        """
        删除当前选中颜色
        """
        self.ui.lw_colors.takeItem(self.ui.lw_colors.currentRow())

    def get_colors(self) -> List[GradientColor]:
        """
        获取当前编辑的颜色列表
        :return: 颜色列表
        """
        colors = []
        for i in range(self.ui.lw_colors.count()):
            item = self.ui.lw_colors.item(i)
            color_widget = self.ui.lw_colors.itemWidget(item)
            colors.append(color_widget.gradient_color)
        return colors

    def accept(self) -> None:
        """
        确认颜色编辑
        """
        self.sig_gradient_changed.emit(self.label, self.get_colors())
        super(GradientEditor, self).accept()
