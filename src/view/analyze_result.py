from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot

from src.ui.analyze_result_ui import Ui_dialog_result
from src.model.models import AnalyzeResultModel
from src.view.video_scene import VideoScene


class ResultDialog(QDialog):
    """
    粒子运动结果窗口
    """
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

    def showEvent(self, event: QShowEvent) -> None:
        """
        窗口显示事件，加载下拉选项
        :param event: 显示事件
        """
        ids = self.scene.graphic_items.get_all_particle_ids()
        self.ui.cb_particle.clear()
        if len(ids) > 0:
            # 需要把List[int]转成List[str]
            self.ui.cb_particle.addItems([str(i) for i in ids])
            self.ui.cb_particle.setCurrentIndex(0)

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
        results = self.scene.graphic_items.get_analyze_result(particle_id)
        model = AnalyzeResultModel(results)
        self.ui.tv_data.setModel(model)
