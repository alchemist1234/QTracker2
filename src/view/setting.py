from typing import List

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot, Qt

from src.ui.settings_ui import Ui_Dialog
from src.settings.settings import Settings
from src.settings.default_settings import *
from src.view.custom_widget import ColorLabel
from src.view.color_editor import ColorEditor


class SettingDialog(QDialog):
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
        self.load_settings()
        self.setup_connects()

    def setup_connects(self) -> None:
        """
        设置信号-槽连接
        """
        self.ui.lb_particle_color_display.clicked.connect(lambda x: self.edit_colors(self.ui.lb_particle_color_display))
        self.ui.lb_mark_color_display.clicked.connect(lambda x: self.edit_colors(self.ui.lb_mark_color_display))
        self.ui.lb_trajectory_color_display.clicked.connect(
            lambda x: self.edit_colors(self.ui.lb_trajectory_color_display))
        self.ui.chb_same_mark_color_with_particle.checkStateChanged.connect(self.mark_color_state)
        self.ui.chb_same_trajectory_color_with_particle.checkStateChanged.connect(self.trajectory_color_state)

    @Slot(Qt.CheckState)
    def mark_color_state(self, state: Qt.CheckState) -> None:
        """
        启用/禁用MarkColor
        :param state: 与粒子相同颜色复选框状态
        """
        self.ui.lb_mark_color_display.setEnabled(state != Qt.CheckState.Checked)

    @Slot(Qt.CheckState)
    def trajectory_color_state(self, state: Qt.CheckState) -> None:
        """
        启用/禁用TrajectoryColor
        :param state: 与粒子相同颜色复选框状态
        """
        self.ui.lb_trajectory_color_display.setEnabled(state != Qt.CheckState.Checked)

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

    def load_settings(self) -> None:
        """
        从配置中加载数据到窗口
        """
        self.ui.spb_median_blur.setValue(self.settings.int_value(median_blur))
        self.ui.spb_gaussian_blur.setValue(self.settings.int_value(gaussian_blur))
        self.ui.spb_opening_size.setValue(self.settings.int_value(opening_size))
        self.ui.spb_closing_size.setValue(self.settings.int_value(closing_size))
        self.ui.chb_apply_hist_eq.setChecked(self.settings.boolean_value(apply_hist_eq))
        self.ui.spb_adaptive_hist_eq.setValue(self.settings.int_value(adaptive_hist_eq))
        self.ui.spb_bilateral_filter_size.setValue(self.settings.int_value(bilateral_size))
        self.ui.spb_bilateral_filter_color.setValue(self.settings.int_value(bilateral_color))
        self.ui.spb_bilateral_filter_space.setValue(self.settings.int_value(bilateral_space))
        self.ui.spb_search_radius.setValue(self.settings.int_value(search_radius))
        self.ui.spb_min_detect_area.setValue(self.settings.int_value(minimum_area_for_detection))
        self.ui.spb_max_detect_area.setValue(self.settings.int_value(maximum_area_for_detection))
        self.ui.spb_memory_frames.setValue(self.settings.int_value(memory_frames))
        self.ui.spb_threshold.setValue(self.settings.int_value(threshold))
        self.ui.spb_derivative_order.setValue(self.settings.int_value(derivative_order))
        self.ui.spb_kernel_size.setValue(self.settings.int_value(kernel_size))
        self.ui.chb_split_particles.setChecked(self.settings.boolean_value(split_circular_particles))
        self.ui.spb_particle_radius_for_split.setValue(self.settings.int_value(split_radius))
        self.ui.chb_fit_to_screen.setChecked(self.settings.boolean_value(fit_to_screen))
        self.ui.spb_skip_frames.setValue(self.settings.int_value(skip_frames))
        self.ui.spb_from_frames.setValue(self.settings.int_value(from_frames))
        self.ui.spb_to_frames.setValue(self.settings.int_value(to_frames))
        # Display
        self.ui.lb_particle_color_display.set_color(self.settings.value(particle_color))
        self.ui.spb_particle_size.setValue(self.settings.int_value(particle_size))
        self.ui.lb_mark_color_display.set_color(self.settings.value(mark_color))
        self.ui.spb_mark_size.setValue(self.settings.int_value(mark_size))
        self.ui.fcb_mark_font.setCurrentFont(self.settings.value(mark_font))
        self.ui.chb_same_mark_color_with_particle.setChecked(self.settings.boolean_value(same_mark_color_with_particle))
        self.ui.lb_trajectory_color_display.set_color(self.settings.value(trajectory_color))
        self.ui.spb_trajectory_width.setValue(self.settings.int_value(trajectory_width))
        self.ui.chb_same_trajectory_color_with_particle.setChecked(
            self.settings.boolean_value(same_trajectory_color_with_particle))

    def save_settings(self) -> None:
        """
        保存配置信息到Setting对象，并刷新配置文件
        """
        # analyze
        self.settings.set_value(median_blur, self.ui.spb_median_blur.value())
        self.settings.set_value(gaussian_blur, self.ui.spb_gaussian_blur.value())
        self.settings.set_value(opening_size, self.ui.spb_opening_size.value())
        self.settings.set_value(closing_size, self.ui.spb_closing_size.value())
        self.settings.set_value(apply_hist_eq, self.ui.chb_apply_hist_eq.isChecked())
        self.settings.set_value(adaptive_hist_eq, self.ui.spb_adaptive_hist_eq.value())
        self.settings.set_value(bilateral_size, self.ui.spb_bilateral_filter_size.value())
        self.settings.set_value(bilateral_color, self.ui.spb_bilateral_filter_color.value())
        self.settings.set_value(bilateral_space, self.ui.spb_bilateral_filter_space.value())
        self.settings.set_value(search_radius, self.ui.spb_search_radius.value())
        self.settings.set_value(minimum_area_for_detection, self.ui.spb_min_detect_area.value())
        self.settings.set_value(maximum_area_for_detection, self.ui.spb_max_detect_area.value())
        self.settings.set_value(memory_frames, self.ui.spb_memory_frames.value())
        self.settings.set_value(threshold, self.ui.spb_threshold.value())
        self.settings.set_value(derivative_order, self.ui.spb_derivative_order.value())
        self.settings.set_value(kernel_size, self.ui.spb_kernel_size.value())
        self.settings.set_value(split_circular_particles, self.ui.chb_split_particles.isChecked())
        self.settings.set_value(split_radius, self.ui.spb_particle_radius_for_split.value())
        self.settings.set_value(fit_to_screen, self.ui.chb_fit_to_screen.isChecked())
        self.settings.set_value(skip_frames, self.ui.spb_skip_frames.value())
        self.settings.set_value(from_frames, self.ui.spb_from_frames.value())
        self.settings.set_value(to_frames, self.ui.spb_to_frames.value())

        # Display
        self.settings.set_value(particle_color, self.ui.lb_particle_color_display.colors)
        self.settings.set_value(particle_size, self.ui.spb_particle_size.value())
        self.settings.set_value(mark_color, self.ui.lb_mark_color_display.colors)
        self.settings.set_value(mark_size, self.ui.spb_mark_size.value())
        self.settings.set_value(mark_font, self.ui.fcb_mark_font.currentFont())
        self.settings.set_value(same_mark_color_with_particle, self.ui.chb_same_mark_color_with_particle.isChecked())
        self.settings.set_value(trajectory_color, self.ui.lb_trajectory_color_display.colors)
        self.settings.set_value(trajectory_width, self.ui.spb_trajectory_width.value())
        self.settings.set_value(same_trajectory_color_with_particle,
                                self.ui.chb_same_trajectory_color_with_particle.isChecked())

        self.settings.sync()
