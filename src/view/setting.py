from PySide6.QtWidgets import QDialog

from src.ui.settings_ui import Ui_Dialog
from src.settings.settings import Settings
from src.settings.default_settings import *


class SettingDialog(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.settings = settings
        self.load_settings()

    def load_settings(self):
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

    def save_settings(self):
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
        # display
        self.settings.sync()
