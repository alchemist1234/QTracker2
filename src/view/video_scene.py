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
        h, w, c = frame.shape
        img = QImage(frame.data, w, h, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.frames_pixmap[index] = pixmap

    @Slot(int)
    def change_display(self, index: int):
        if index in self.frames_pixmap:
            self.current_frame_item.setPixmap(self.frames_pixmap[index])

    @Slot(int, dict)
    def add_frame_particles(self, frame_index: int, particles: Dict[int, Tuple[int, int]]):
        print(frame_index, particles)
        self.particle_data.add_frame_particles(frame_index, particles)
