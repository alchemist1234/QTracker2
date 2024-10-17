import numpy as np
from typing import Tuple, List

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QInputDialog, QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, QByteArray, QBuffer, QPointF

from src.model.models import ParticlePositions, GraphicItems, OperationMode
from src.settings.settings import Settings


class VideoScene(QGraphicsScene):
    def __init__(self, parent=None, settings: Settings = None):
        super().__init__(parent)
        self.settings = settings
        # 当前操作模式
        self.mode = OperationMode.MOVE
        # 用base64存储图像数据，用QImage或者QPixmap存储内存占用过大
        self.frames_base64 = {}
        # 粒子位置原始数据
        self.particle_data = ParticlePositions()
        # GraphicItem存储容器
        self.graphic_items = GraphicItems(self.particle_data, self.settings)
        # 当前添加到QGraphicsScene中的粒子Item
        self.particle_items = []
        # 当前添加到QGraphicsScene中的轨迹Item
        self.trajectory_items = []
        # 当前帧
        self.current_frame_index = -1
        # 当前鼠标按下位置
        self.mouse_press_pos = QPointF()

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
        self.frames_base64[index] = self.img_to_base64(img)

    @Slot(int)
    def change_display(self, index: int) -> None:
        """
        切换帧显示
        """
        self.current_frame_index = index
        self.change_frame_display(index)
        self.change_particle_display(index)
        self.change_trajectory_display(index)

    def change_frame_display(self, index: int) -> None:
        """
        切换图像显示
        :param index: 帧ID
        """
        if index in self.frames_base64:
            base64 = self.frames_base64[index]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            self.current_frame_item.setPixmap(QPixmap.fromImage(img))

    def change_particle_display(self, index: int) -> None:
        """
        切换粒子显示
        :param index: 帧ID
        """
        for item in self.particle_items:
            self.removeItem(item)
        self.particle_items = self.graphic_items.get_particle_items(index)
        for item in self.particle_items:
            self.addItem(item)

    def change_trajectory_display(self, index: int) -> None:
        """
        切换轨迹显示
        :param index: 帧ID
        """
        for item in self.trajectory_items:
            self.removeItem(item)
        self.trajectory_items = self.graphic_items.get_trajectory_items(index)
        for item in self.trajectory_items:
            self.addItem(item)

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
        self.graphic_items.generate_particle_items(frame_index)
        self.graphic_items.generate_trajectory_items(frame_index)

    def img_to_base64(self, img: QImage) -> bytes:
        """
        QImage 转 Base64
        :param img: QImage
        :return: Base64 bytes
        """
        # quality = self.settings.int_value(default_settings.frame_quality)
        byte_arr = QByteArray()
        buffer = QBuffer(byte_arr)
        buffer.open(QBuffer.OpenModeFlag.WriteOnly)
        img.save(buffer, 'jpg', 100)
        return byte_arr.toBase64().data()

    def clear_data(self) -> None:
        """
        清除所有数据
        """
        self.current_frame_index = -1
        self.graphic_items.clear()
        self.particle_items.clear()
        self.trajectory_items.clear()
        self.clear()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.mouse_press_pos = event.scenePos()
        if self.mode == OperationMode.ADD:
            if self.current_frame_index in self.frames_base64:
                scene_pos = event.scenePos().toPoint()
                index, ok = QInputDialog.getInt(self, '输入', '粒子编号', 1)
                if ok:
                    self.particle_data.add_particle(self.current_frame_index, index, (scene_pos.x(), scene_pos.y()))
                    self.update_frame_item(self.current_frame_index)
                    self.change_display(self.current_frame_index)
            else:
                QMessageBox.information(self, '提示', f'未加载视频')
        super(VideoScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        moved = pos - self.mouse_press_pos
        if moved.manhattanLength() > 0:
            if len(self.selectedItems()) > 0:
                for item in self.selectedItems():
                    index = item.index
                    next_frame = self.particle_data.move_particle_by(self.current_frame_index, index,
                                                                     (moved.x(), moved.y()))
                    if next_frame:
                        self.update_frame_item(next_frame)
                self.update_frame_item(self.current_frame_index)
                self.change_display(self.current_frame_index)
        super(VideoScene, self).mouseReleaseEvent(event)

    def update_frame_item(self, frame_index: int):
        self.graphic_items.generate_particle_items(frame_index)
        self.graphic_items.generate_trajectory_items(frame_index)
