from typing import List

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QColor, QGradient

from src.model.models import GradientColor
from src.ui.settings_ui import Ui_Dialog
from src.settings.settings import Settings
from src.settings.default_settings import SettingKey
from src.view.custom_widget import ColorLabel, GradientLabel
from src.view.color_editor import ColorEditor
from src.view.gradient_editor import GradientEditor


class SettingDialog(QDialog):
    # 显示设置改变信号
    sig_display_settings_changed = Signal()

    def __init__(self, settings: Settings):
        """
        设置对话框
        :param settings: 设置数据
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.settings = settings
        self.ui.lb_particle_color_display.setFixedSize(76, 20)
        self.ui.lb_mark_color_display.setFixedSize(76, 20)
        self.ui.lb_trajectory_color_display.setFixedSize(76, 20)
        self.ui.lb_speed_color_display.setFixedSize(76, 20)
        self.ui.lb_frame_label_display.setFixedSize(76, 20)
        self.load_settings()
        self.setup_connects()
        self.init_state()

    def setup_connects(self) -> None:
        """
        设置信号-槽连接
        """
        self.ui.lb_particle_color_display.clicked.connect(lambda x: self.edit_colors(self.ui.lb_particle_color_display))
        self.ui.lb_mark_color_display.clicked.connect(lambda x: self.edit_colors(self.ui.lb_mark_color_display))
        self.ui.lb_trajectory_color_display.clicked.connect(
            lambda x: self.edit_colors(self.ui.lb_trajectory_color_display))
        self.ui.lb_frame_label_display.clicked.connect(lambda x: self.edit_colors(self.ui.lb_frame_label_display))
        self.ui.chb_same_mark_color_with_particle.checkStateChanged.connect(self.mark_color_state)
        self.ui.chb_same_trajectory_color_with_particle.clicked.connect(self.trajectory_color_with_particle_clicked)
        self.ui.chb_color_with_speed.clicked.connect(self.speed_color_clicked)
        self.ui.lb_speed_color_display.clicked.connect(lambda x: self.edit_gradient(self.ui.lb_speed_color_display))
        # 按钮
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.btn_load_settings.clicked.connect(self.load_settings_from_file)
        self.ui.btn_save_settings.clicked.connect(self.save_settings_to_file)
        self.accepted.connect(self.save_settings)

    @Slot(Qt.CheckState)
    def mark_color_state(self, state: Qt.CheckState) -> None:
        """
        启用/禁用MarkColor
        :param state: 与粒子相同颜色复选框状态
        """
        self.ui.lb_mark_color_display.setEnabled(state != Qt.CheckState.Checked)

    @Slot(Qt.CheckState)
    def trajectory_color_with_particle_clicked(self, checked: bool) -> None:
        """
        启用/禁用TrajectoryColor
        :param checked: 与粒子相同颜色复选框状态
        """
        self.ui.lb_trajectory_color_display.setEnabled(not checked)
        self.ui.chb_color_with_speed.setChecked(False)
        self.ui.lb_speed_color_display.setEnabled(False)
        self.ui.dsb_color_speed_min.setEnabled(False)
        self.ui.dsb_color_speed_max.setEnabled(False)

    @Slot(Qt.CheckState)
    def speed_color_clicked(self, checked: bool) -> None:
        """
        启用/禁用轨迹颜色随速度变化
        :param checked: 轨迹颜色随速度变化复选框状态
        """
        self.ui.lb_trajectory_color_display.setEnabled(not checked)
        self.ui.chb_same_trajectory_color_with_particle.setChecked(False)
        self.ui.lb_speed_color_display.setEnabled(checked)
        self.ui.dsb_color_speed_min.setEnabled(checked)
        self.ui.dsb_color_speed_max.setEnabled(checked)

    @Slot(ColorLabel)
    def edit_colors(self, label: ColorLabel) -> None:
        """
        打开颜色编辑窗
        :param label: 颜色标签
        """
        editor = ColorEditor(self, label)
        editor.add_colors(label.colors)
        editor.sig_color_changed.connect(self.update_color)
        editor.exec()

    @Slot(ColorLabel, list)
    def update_color(self, label: ColorLabel, colors: List[QColor]) -> None:
        """
        更新ColorLabel颜色
        :param label: 需要设置颜色的ColorLabel
        :param colors: 颜色
        """
        label.set_color(colors)

    @Slot(GradientLabel)
    def edit_gradient(self, label: GradientLabel):
        editor = GradientEditor(self, label)
        editor.add_colors(label.colors)
        editor.sig_gradient_changed.connect(self.update_gradient)
        editor.exec()

    @Slot(GradientLabel, list)
    def update_gradient(self, label: GradientLabel, gradients: List[GradientColor]) -> None:
        label.set_gradient(gradients)

    def init_state(self) -> None:
        """
        初始化控状态
        """
        self.mark_color_state(self.ui.chb_same_mark_color_with_particle.checkState())
        same_traject_color_with_particle = self.ui.chb_same_trajectory_color_with_particle.isChecked()
        speed_color = self.ui.chb_color_with_speed.isChecked()
        if same_traject_color_with_particle:
            self.trajectory_color_with_particle_clicked(True)
        elif speed_color:
            self.speed_color_clicked(True)
        else:
            self.trajectory_color_with_particle_clicked(False)

    def load_settings_from_file(self) -> None:
        """
        导入外部配置文件
        """
        path, _ = QFileDialog.getOpenFileName(self, caption='Open Settings',
                                              filter='Setting Files(*.ini);;All File(*.*)')
        if path:
            temp_settings = Settings(path)
            self.load_settings(temp_settings)

    def save_settings_to_file(self) -> None:
        """
        导出配置到文件
        """
        path, _ = QFileDialog.getSaveFileName(self, caption='Save Settings',
                                              filter='Setting Files(*.ini)')
        if path:
            temp_settings = Settings(path)
            self.save_settings(temp_settings)

    def load_settings(self, settings: Settings = None) -> None:
        """
        从配置中加载数据到窗口
        :param settings 需要加载的配置文件, 默认为程序当前目录下config.ini
        """
        source_settings = settings if settings else self.settings
        self.ui.spb_median_blur.setValue(source_settings.int_value(SettingKey.median_blur))
        self.ui.spb_gaussian_blur.setValue(source_settings.int_value(SettingKey.gaussian_blur))
        self.ui.spb_opening_size.setValue(source_settings.int_value(SettingKey.opening_size))
        self.ui.spb_closing_size.setValue(source_settings.int_value(SettingKey.closing_size))
        self.ui.chb_apply_hist_eq.setChecked(source_settings.boolean_value(SettingKey.apply_hist_eq))
        self.ui.spb_adaptive_hist_eq.setValue(source_settings.int_value(SettingKey.adaptive_hist_eq))
        self.ui.spb_bilateral_filter_size.setValue(source_settings.int_value(SettingKey.bilateral_size))
        self.ui.spb_bilateral_filter_color.setValue(source_settings.int_value(SettingKey.bilateral_color))
        self.ui.spb_bilateral_filter_space.setValue(source_settings.int_value(SettingKey.bilateral_space))
        self.ui.spb_search_radius.setValue(source_settings.int_value(SettingKey.search_radius))
        self.ui.spb_min_detect_area.setValue(source_settings.int_value(SettingKey.minimum_area_for_detection))
        self.ui.spb_max_detect_area.setValue(source_settings.int_value(SettingKey.maximum_area_for_detection))
        self.ui.spb_memory_frames.setValue(source_settings.int_value(SettingKey.memory_frames))
        self.ui.spb_threshold.setValue(source_settings.int_value(SettingKey.threshold))
        self.ui.spb_derivative_order.setValue(source_settings.int_value(SettingKey.derivative_order))
        self.ui.spb_kernel_size.setValue(source_settings.int_value(SettingKey.kernel_size))
        self.ui.chb_split_particles.setChecked(source_settings.boolean_value(SettingKey.split_circular_particles))
        self.ui.spb_particle_radius_for_split.setValue(source_settings.int_value(SettingKey.split_radius))
        self.ui.spb_skip_frames.setValue(source_settings.int_value(SettingKey.skip_frames))
        self.ui.spb_from_frames.setValue(source_settings.int_value(SettingKey.from_frames))
        self.ui.spb_to_frames.setValue(source_settings.int_value(SettingKey.to_frames))
        self.ui.dspb_scale.setValue(source_settings.float_value(SettingKey.scale))
        # Display
        self.ui.lb_particle_color_display.set_color(source_settings.value(SettingKey.particle_color))
        self.ui.spb_particle_size.setValue(source_settings.int_value(SettingKey.particle_size))
        self.ui.lb_mark_color_display.set_color(source_settings.value(SettingKey.mark_color))
        self.ui.spb_mark_size.setValue(source_settings.int_value(SettingKey.mark_size))
        self.ui.fcb_mark_font.setCurrentFont(source_settings.value(SettingKey.mark_font))
        self.ui.chb_same_mark_color_with_particle.setChecked(
            source_settings.boolean_value(SettingKey.same_mark_color_with_particle))
        self.ui.lb_trajectory_color_display.set_color(source_settings.value(SettingKey.trajectory_color))
        self.ui.spb_trajectory_width.setValue(source_settings.int_value(SettingKey.trajectory_width))
        self.ui.chb_same_trajectory_color_with_particle.setChecked(
            source_settings.boolean_value(SettingKey.same_trajectory_color_with_particle))
        self.ui.chb_color_with_speed.setChecked(source_settings.boolean_value(SettingKey.trajectory_color_with_speed))
        self.ui.lb_speed_color_display.set_gradient(source_settings.value(SettingKey.trajectory_speed_color))
        self.ui.dsb_color_speed_min.setValue(source_settings.float_value(SettingKey.min_color_speed))
        self.ui.dsb_color_speed_max.setValue(source_settings.float_value(SettingKey.max_color_speed))
        self.ui.lb_frame_label_display.set_color(source_settings.value(SettingKey.frame_label_color))
        self.ui.spb_frame_label_size.setValue(source_settings.int_value(SettingKey.frame_label_size))
        self.ui.fcb_frame_label_font.setCurrentFont(source_settings.value(SettingKey.frame_label_font))
        self.ui.cb_frame_label_pos.setCurrentIndex(source_settings.int_value(SettingKey.frame_label_pos))

    def save_settings(self, settings: Settings = None) -> None:
        """
        保存配置信息到Setting对象，并刷新配置文件
        :param settings 需要保存的配置文件, 默认为程序当前目录下config.ini
        """
        # 判断显示设置是否有改变
        display_updated = False
        if settings is None:
            if self.settings.value(SettingKey.particle_color) != self.ui.lb_particle_color_display.colors \
                    or self.settings.int_value(SettingKey.particle_size) != self.ui.spb_particle_size.value() \
                    or self.settings.value(SettingKey.mark_color) != self.ui.lb_mark_color_display.colors \
                    or self.settings.int_value(SettingKey.mark_size) != self.ui.spb_mark_size.value() \
                    or self.settings.boolean_value(
                SettingKey.same_mark_color_with_particle) != self.ui.chb_same_mark_color_with_particle.isChecked() \
                    or self.settings.value(SettingKey.mark_font) != self.ui.fcb_mark_font.currentFont() \
                    or self.settings.value(SettingKey.trajectory_color) != self.ui.lb_trajectory_color_display.colors \
                    or self.settings.int_value(SettingKey.trajectory_width) != self.ui.spb_trajectory_width.value() \
                    or self.settings.boolean_value(
                SettingKey.same_trajectory_color_with_particle) != self.ui.chb_same_trajectory_color_with_particle.isChecked() \
                    or self.settings.value(SettingKey.frame_label_color) != self.ui.lb_frame_label_display.colors \
                    or self.settings.int_value(SettingKey.frame_label_size) != self.ui.spb_frame_label_size.value() \
                    or self.settings.value(SettingKey.frame_label_font) != self.ui.fcb_frame_label_font.currentFont() \
                    or self.settings.value(SettingKey.frame_label_pos) != self.ui.cb_frame_label_pos.currentIndex() \
                    or self.settings.boolean_value(
                SettingKey.trajectory_color_with_speed) != self.ui.chb_color_with_speed.isChecked() \
                    or self.settings.value(SettingKey.trajectory_speed_color) != self.ui.lb_speed_color_display.colors \
                    or self.settings.float_value(SettingKey.max_color_speed) != self.ui.dsb_color_speed_max.value() \
                    or self.settings.float_value(SettingKey.min_color_speed) != self.ui.dsb_color_speed_min.value():
                display_updated = True

        target_settings = settings if settings else self.settings
        # analyze
        target_settings.set_value(SettingKey.median_blur, self.ui.spb_median_blur.value())
        target_settings.set_value(SettingKey.gaussian_blur, self.ui.spb_gaussian_blur.value())
        target_settings.set_value(SettingKey.opening_size, self.ui.spb_opening_size.value())
        target_settings.set_value(SettingKey.closing_size, self.ui.spb_closing_size.value())
        target_settings.set_value(SettingKey.apply_hist_eq, self.ui.chb_apply_hist_eq.isChecked())
        target_settings.set_value(SettingKey.adaptive_hist_eq, self.ui.spb_adaptive_hist_eq.value())
        target_settings.set_value(SettingKey.bilateral_size, self.ui.spb_bilateral_filter_size.value())
        target_settings.set_value(SettingKey.bilateral_color, self.ui.spb_bilateral_filter_color.value())
        target_settings.set_value(SettingKey.bilateral_space, self.ui.spb_bilateral_filter_space.value())
        target_settings.set_value(SettingKey.search_radius, self.ui.spb_search_radius.value())
        target_settings.set_value(SettingKey.minimum_area_for_detection, self.ui.spb_min_detect_area.value())
        target_settings.set_value(SettingKey.maximum_area_for_detection, self.ui.spb_max_detect_area.value())
        target_settings.set_value(SettingKey.memory_frames, self.ui.spb_memory_frames.value())
        target_settings.set_value(SettingKey.threshold, self.ui.spb_threshold.value())
        target_settings.set_value(SettingKey.derivative_order, self.ui.spb_derivative_order.value())
        target_settings.set_value(SettingKey.kernel_size, self.ui.spb_kernel_size.value())
        target_settings.set_value(SettingKey.split_circular_particles, self.ui.chb_split_particles.isChecked())
        target_settings.set_value(SettingKey.split_radius, self.ui.spb_particle_radius_for_split.value())
        target_settings.set_value(SettingKey.skip_frames, self.ui.spb_skip_frames.value())
        target_settings.set_value(SettingKey.from_frames, self.ui.spb_from_frames.value())
        target_settings.set_value(SettingKey.to_frames, self.ui.spb_to_frames.value())
        target_settings.set_value(SettingKey.scale, self.ui.dspb_scale.value())

        # Display
        target_settings.set_value(SettingKey.particle_color, self.ui.lb_particle_color_display.colors)
        target_settings.set_value(SettingKey.particle_size, self.ui.spb_particle_size.value())
        target_settings.set_value(SettingKey.mark_color, self.ui.lb_mark_color_display.colors)
        target_settings.set_value(SettingKey.mark_size, self.ui.spb_mark_size.value())
        target_settings.set_value(SettingKey.mark_font, self.ui.fcb_mark_font.currentFont())
        target_settings.set_value(SettingKey.same_mark_color_with_particle,
                                  self.ui.chb_same_mark_color_with_particle.isChecked())
        target_settings.set_value(SettingKey.trajectory_color, self.ui.lb_trajectory_color_display.colors)
        target_settings.set_value(SettingKey.trajectory_width, self.ui.spb_trajectory_width.value())
        target_settings.set_value(SettingKey.same_trajectory_color_with_particle,
                                  self.ui.chb_same_trajectory_color_with_particle.isChecked())
        target_settings.set_value(SettingKey.trajectory_color_with_speed, self.ui.chb_color_with_speed.isChecked())
        target_settings.set_value(SettingKey.trajectory_speed_color, self.ui.lb_speed_color_display.colors)
        target_settings.set_value(SettingKey.min_color_speed, self.ui.dsb_color_speed_min.value())
        target_settings.set_value(SettingKey.max_color_speed, self.ui.dsb_color_speed_max.value())
        target_settings.set_value(SettingKey.frame_label_color, self.ui.lb_frame_label_display.colors)
        target_settings.set_value(SettingKey.frame_label_size, self.ui.spb_frame_label_size.value())
        target_settings.set_value(SettingKey.frame_label_font, self.ui.fcb_frame_label_font.currentFont())
        target_settings.set_value(SettingKey.frame_label_pos, self.ui.cb_frame_label_pos.currentIndex())

        # 显示设置变动，通知更新页面显示
        if display_updated:
            self.sig_display_settings_changed.emit()
