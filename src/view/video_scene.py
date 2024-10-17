import numpy as np
from typing import Tuple, List

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, QByteArray, QBuffer

from src.model.models import ParticlePositions


class VideoScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 用base64存储图像数据，用QImage或者QPixmap存储内存占用过大
        self.frames_base64 = {}
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
        # pixmap = QPixmap.fromImage(img)
        self.frames_base64[index] = self.img_to_base64(img)

    @Slot(int)
    def change_display(self, index: int) -> None:
        """
        切换帧显示
        :param index: 需要显示的帧
        """
        if index in self.frames_base64:
            # self.current_frame_item.setPixmap(self.frames_pixmap[index])
            # self.current_frame_item.setPixmap(QPixmap.fromImage(self.frames_pixmap[index]))
            base64 = self.frames_base64[index]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            self.current_frame_item.setPixmap(QPixmap.fromImage(img))

    @Slot(int, list)
    def add_frame_particles(self, frame_index: int, particles: List[Tuple[int, Tuple[int, int]]]):
        """
        添加一帧所有粒子
        :param frame_index: 帧ID
        :param particles: 粒子数据, {粒子ID:(x, y),...}
        """
        print(frame_index, particles)
        particle_map = {p[0]: p[1] for p in particles}
        self.particle_data.add_frame_particles(frame_index, particle_map)

    def img_to_base64(self, img: QImage) -> bytes:
        # quality = self.settings.int_value(default_settings.frame_quality)
        byte_arr = QByteArray()
        buffer = QBuffer(byte_arr)
        buffer.open(QBuffer.OpenModeFlag.WriteOnly)
        img.save(buffer, 'jpg', 100)
        return byte_arr.toBase64().data()
