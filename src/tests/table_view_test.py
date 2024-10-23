import sys
from typing import List, Any
from PySide6.QtWidgets import QTableView, QDialog, QApplication, QCompleter
from PySide6.QtCore import QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel
from scipy.interpolate import insert

from src.ui.analyze_result_ui import Ui_dialog_result


class ListModel(QStandardItemModel):
    def __init__(self, data: List[Any]):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return 1

    def data(self, index, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]


class Model(QAbstractTableModel):
    def __init__(self, data: List[List[Any]]):
        super(Model, self).__init__()
        self._data = data
        self.headers = ['id', 'x', 'y']

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index: QModelIndex, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

    def reset_data(self, data: List[List[Any]]):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.ui = Ui_dialog_result()
        self.ui.setupUi(self)
        self.model = Model([])
        self.ui.tv_data.setModel(self.model)
        self.ui.btn_export.clicked.connect(self.update_data)
        completer = QCompleter(self.ui.cb_particle.model())
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.ui.cb_particle.setCompleter(completer)
        # self.ui.cb_particle.currentTextChanged.connect(self.text_changed)
        self.ui.cb_particle.currentIndexChanged.connect(self.text_changed)

    def text_changed(self, t):
        print(type(t))
        print(t)
    def update_data(self):
        data = [[1, 10, 10], [2, 20, 20]]
        self.model.reset_data(data)
        self.ui.cb_particle.addItems(['1', '2', '784'])
        # self.ui.chb_particle.setModel(ListModel([1, 2, 784]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dialog()
    window.show()
    sys.exit(app.exec())
