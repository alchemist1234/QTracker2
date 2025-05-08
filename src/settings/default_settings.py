from dataclasses import dataclass
from typing import Any
from enum import Enum
from PySide6.QtGui import QColor, QFont, QColorConstants

from src.model.models import GradientColor


@dataclass
class SettingItem:
    """
    设置项
    :param section       配置段
    :param key           配置项
    :param default_value 配置默认值
    """
    section: str
    key: str
    default_value: Any
    save_to_file: bool = True


default_speed_color = [
    GradientColor(0, QColorConstants.Blue),
    GradientColor(0.5, QColorConstants.Green),
    GradientColor(1, QColorConstants.Red)
]


class SettingKey(Enum):
    main_width = SettingItem(section='main', key='width', default_value=800)
    main_height = SettingItem(section='main', key='height', default_value=600)
    median_blur = SettingItem(section='analyze', key='median_blur', default_value=1)
    gaussian_blur = SettingItem(section='analyze', key='gaussian_blur', default_value=3)
    opening_size = SettingItem(section='analyze', key='opening_size', default_value=1)
    closing_size = SettingItem(section='analyze', key='closing_size', default_value=1)
    apply_hist_eq = SettingItem(section='analyze', key='apply_hist_eq', default_value=False)
    adaptive_hist_limit = SettingItem(section='analyze', key='adaptive_hist_limit', default_value=0)
    bilateral_size = SettingItem(section='analyze', key='bilateral_size', default_value=6)
    bilateral_color = SettingItem(section='analyze', key='bilateral_color', default_value=75)
    bilateral_space = SettingItem(section='analyze', key='bilateral_space', default_value=75)
    search_radius = SettingItem(section='analyze', key='search_radius', default_value=40)
    minimum_area_for_detection = SettingItem(section='analyze', key='minimum_area_for_detection', default_value=30)
    maximum_area_for_detection = SettingItem(section='analyze', key='maximum_area_for_detection', default_value=3000)
    memory_frames = SettingItem(section='analyze', key='memory_frames', default_value=40)
    threshold = SettingItem(section='analyze', key='threshold', default_value=175)
    derivative_order = SettingItem(section='analyze', key='derivative_order', default_value=1)
    kernel_size = SettingItem(section='analyze', key='kernel_size', default_value=5)
    split_circular_particles = SettingItem(section='analyze', key='split_circular_particles', default_value=False)
    split_radius = SettingItem(section='analyze', key='split_radius', default_value=10)
    # fit_to_screen = SettingItem(section='analyze', key='fit_to_screen', default_value=True)
    show_binary_image = SettingItem(section='analyze', key='show_binary_image', default_value=False)
    start_frame = SettingItem(section='analyze', key='start_frame', default_value=1)
    stop_frame = SettingItem(section='analyze', key='stop_frame', default_value=-1)
    file_path = SettingItem(section='analyze', key='file_path', default_value=None)
    dir_path = SettingItem(section='analyze', key='dir_path', default_value=None)
    frame_quality = SettingItem(section='analyze', key='frame_quality', default_value=80)
    scale = SettingItem(section='analyze', key='scale', default_value=0)
    fps = SettingItem(section='analyze', key='fps', default_value=0, save_to_file=False)

    particle_color = SettingItem(section='display', key='particle_color', default_value=QColor(0, 255, 0))
    particle_size = SettingItem(section='display', key='particle_size', default_value=4)
    show_particle = SettingItem(section='display', key='show_particle', default_value=True, save_to_file=False)
    mark_color = SettingItem(section='display', key='mark_color', default_value=QColor(255, 0, 0))
    mark_size = SettingItem(section='display', key='mark_size', default_value=4)
    mark_font = SettingItem(section='display', key='mark_font', default_value=QFont('SimHei'))
    show_mark = SettingItem(section='display', key='show_mark', default_value=True, save_to_file=False)
    same_mark_color_with_particle = SettingItem(section='display', key='same_mark_color_with_particle',
                                                default_value=False)
    trajectory_color = SettingItem(section='display', key='trajectory_color', default_value=QColor(0, 0, 255))
    trajectory_width = SettingItem(section='display', key='trajectory_size', default_value=2)
    show_trajectory = SettingItem(section='display', key='show_trajectory', default_value=True, save_to_file=False)
    same_trajectory_color_with_particle = SettingItem(section='display', key='same_trajectory_color_with_particle',
                                                      default_value=False)
    trajectory_color_with_speed = SettingItem(section='display', key='trajectory_color_change_with_speed',
                                              default_value=False)
    trajectory_speed_color = SettingItem(section='display', key='trajectory_speed_color',
                                         default_value=default_speed_color)
    min_color_speed = SettingItem(section='display', key='min_color_speed', default_value=0)
    max_color_speed = SettingItem(section='display', key='max_color_speed', default_value=100)
    frame_label_color = SettingItem(section='display', key='frame_label_color', default_value=QColor(0, 0, 255))
    frame_label_size = SettingItem(section='display', key='frame_label_size', default_value=18)
    frame_label_font = SettingItem(section='display', key='frame_label_font', default_value=QFont('SimHei'))
    frame_label_pos = SettingItem(section='display', key='frame_label_pos', default_value=0)
    show_frame_label = SettingItem(section='display', key='show_frame_label', default_value=True, save_to_file=False)
    index_filter = SettingItem(section='display', key='index_filter', default_value=[], save_to_file=False)
