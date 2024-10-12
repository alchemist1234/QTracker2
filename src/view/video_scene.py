import numpy as np
from typing import Dict, Tuple

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot

from src.model.models import ParticlePositions


class VideoScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frames_pixmap = {}
        self.particle_data = ParticlePositions()
        self.current_frame_item = QGraphicsPixmapItem()
        self.addItem(self.current_frame_item)

    @Slot(int, np.ndarray)
    def add_frame(self, index: int, frame: np.ndarray) -> None:
        """
        添加帧图像
        :param index: 帧ID
        :param frame: 帧数据
        """
        h, w, c = frame.shape
        img = QImage(frame.data, w, h, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.frames_pixmap[index] = pixmap

    @Slot(int)
    def change_display(self, index: int) -> None:
        """
        切换帧显示
        :param index: 需要显示的帧
        """
        if index in self.frames_pixmap:
            self.current_frame_item.setPixmap(self.frames_pixmap[index])

    @Slot(int, dict)
    def add_frame_particles(self, frame_index: int, particles: Dict[int, Tuple[int, int]]):
        """
        添加一帧所有粒子
        :param frame_index: 帧ID
        :param particles: 粒子数据, {粒子ID:(x, y),...}
        """
        print(frame_index, particles)
        self.particle_data.add_frame_particles(frame_index, particles)
