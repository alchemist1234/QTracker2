import csv

from PySide6.QtGui import QShowEvent, QCloseEvent
from PySide6.QtWidgets import QDialog, QCompleter, QInputDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, Slot, Qt

from src.ui.analyze_result_ui import Ui_dialog_result
from src.model.qt_models import AnalyzeResultModel
from src.view.video_scene import VideoScene
from src.util import common_util


class ResultDialog(QDialog):
    """
    粒子运动结果窗口
    """
    sig_closed = Signal()

    def __init__(self, scene: VideoScene):
        """
        分析结果对话框
        """
        super().__init__()
        self.ui = Ui_dialog_result()
        self.ui.setupUi(self)
        self.setModal(False)
        # 保存VideoScene对象，用于获取粒子运动结果数据
        self.scene = scene

        self.ui.cb_particle.currentIndexChanged.connect(self.change_result)
        self.ui.btn_export.clicked.connect(self.export)
        self.ui.btn_close.clicked.connect(self.close)

    def showEvent(self, event: QShowEvent) -> None:
        """
        窗口显示事件，加载下拉选项
        :param event: 显示事件
        """
        ids = self.scene.data_helper.get_all_particle_ids()
        self.ui.cb_particle.clear()
        if len(ids) > 0:
            # 需要把List[int]转成List[str]
            self.ui.cb_particle.addItems([str(i) for i in ids])
            self.ui.cb_particle.setCurrentIndex(0)
            # 模糊查询
            completer = QCompleter(self.ui.cb_particle.model())
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.ui.cb_particle.setCompleter(completer)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        关闭事件, 通知外部更新按钮状态
        :param event: 关闭事件
        """
        self.sig_closed.emit()
        super().closeEvent(event)

    @Slot(int)
    def change_result(self, model_index: int) -> None:
        """
        下拉选项变更，更新TableView中数据
        :param model_index: 选项索引
        """
        item_str = self.ui.cb_particle.itemText(model_index)
        if not item_str.isdigit():
            return
        particle_id = int(item_str)
        model = self.scene.data_helper.get_analyze_result_model(particle_id)
        self.ui.tv_data.setModel(model)

    def export(self) -> None:
        """
        导出数据到CSV文件
        """
        # 输入粒子ID，为空输出所有粒子
        text, ok = QInputDialog.getText(self, '请输入', '粒子ID')
        ids = self.scene.data_helper.get_all_particle_ids()
        if not ok:
            return
        text_ids = common_util.split_indexes_text(text)
        if len(text_ids) > 0:
            ids = list(text_ids)
            ids.sort()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Export Data', '', filter='CSV File(*.csv)')
        if not file_name:
            return
        try:
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                for particle_id in ids:
                    writer.writerow([f'粒子{particle_id}'])
                    model: AnalyzeResultModel = self.scene.data_helper.get_analyze_result_model(particle_id)
                    writer.writerow(model.headers)
                    for r in range(model.rowCount()):
                        row = []
                        for c in range(model.columnCount()):
                            index = model.index(r, c)
                            cell = model.data(index, Qt.ItemDataRole.DisplayRole)
                            row.append(str(cell))
                        writer.writerow(row)
                    writer.writerow([])
        except OSError:
            # 无写入权限/路径不存在时提示用户, 而不是异常退出
            QMessageBox.warning(self, '导出失败', '无法写入文件, 请检查路径与写入权限')
