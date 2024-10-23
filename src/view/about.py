from PySide6.QtWidgets import QDialog

from src.ui.about_ui import Ui_dialog_about


class AboutDialog(QDialog):
    """
    关于窗口
    """

    def __init__(self):
        """
        分析结果对话框
        """
        super().__init__()
        self.ui = Ui_dialog_about()
        self.ui.setupUi(self)
        self.setModal(True)

