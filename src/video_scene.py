from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot
import numpy as np


class VideoScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frames_items = {}
        self.current_frame_item = QGraphicsPixmapItem()
        self.addItem(self.current_frame_item)

    @Slot(int, np.ndarray)
    def add_frame(self, index: int, frame: np.ndarray) -> None:
        h, w, c = frame.shape
        img = QImage(frame.data, w, h, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.frames_items[index] = QGraphicsPixmapItem(pixmap)

    @Slot(int)
    def update_frame(self, index: int):
        if index in self.frames_items:
            self.current_frame_item.setPixmap(self.frames_items[index])
