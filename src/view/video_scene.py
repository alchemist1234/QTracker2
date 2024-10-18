import numpy as np
from typing import Tuple, List

from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QInputDialog, QMessageBox,
                               QLineEdit, QWidget)
from PySide6.QtGui import QPixmap, QImage, QKeyEvent
from PySide6.QtCore import Slot, QByteArray, QBuffer, QPointF, Qt

from src.model.models import GraphicItems, OperationMode
from src.settings.default_settings import show_particle, show_mark, show_trajectory, index_filter
from src.settings.settings import Settings
from src.util.common_util import split_indexes_text


class VideoScene(QGraphicsScene):
    def __init__(self, parent: QWidget = None, settings: Settings = None):
        super().__init__(parent)
        self.settings = settings
        # 当前操作模式
        self.mode = OperationMode.MOVE
        # 用base64存储图像数据，用QImage或者QPixmap存储内存占用过大
        self.frames_base64 = {}
        # GraphicItem存储容器
        self.graphic_items = GraphicItems(self.settings)
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
        self.__change_trajectory_display(index)
        self.__change_particle_display(index)

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

    def __change_particle_display(self, frame_index: int) -> None:
        """
        切换粒子显示
        :param frame_index: 帧ID
        """
        for item in self.particle_items:
            self.removeItem(item)
        # 设置显示/隐藏
        particle_shown = self.settings.boolean_value(show_particle)
        mark_shown = self.settings.boolean_value(show_mark)
        self.particle_items = self.graphic_items.get_particle_items(frame_index)
        for item in self.particle_items:
            item.particle_visible(particle_shown)
            item.mark_visible(mark_shown)
            self.addItem(item)

    def __change_trajectory_display(self, frame_index: int) -> None:
        """
        切换轨迹显示
        :param frame_index: 帧ID
        """
        for item in self.trajectory_items:
            self.removeItem(item)
        self.trajectory_items = self.graphic_items.get_trajectory_items(frame_index)
        for item in self.trajectory_items:
            item.setVisible(self.settings.boolean_value(show_trajectory))
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
        self.graphic_items.add_frame_particles(frame_index, particle_map)

    def combine_particles(self) -> None:
        """
        合并粒子
        """
        items = self.selectedItems()
        if len(items) == 0:
            text, ok = QInputDialog.getText(None, "输入", "待合并的粒子编号(,或者空格分隔)", QLineEdit.EchoMode.Normal)
            if ok:
                indexes = split_indexes_text(text)
                self.graphic_items.combine_particles(indexes)
                self.change_display(self.current_frame_index)
        else:
            indexes = {i.index for i in items}
            self.graphic_items.combine_particles(indexes)
            self.change_display(self.current_frame_index)

    def set_particle_visible(self, show: bool) -> None:
        """
        是否显示粒子
        :param show: 是否显示
        """
        self.settings.set_value(show_particle, show)
        self.change_display(self.current_frame_index)

    def set_mark_visible(self, show: bool) -> None:
        """
        是否显示标记
        :param show: 是否显示
        """
        self.settings.set_value(show_mark, show)
        self.change_display(self.current_frame_index)

    def set_trajectory_visible(self, show: bool) -> None:
        """
        是否显示轨迹
        :param show: 是否显示
        """
        self.settings.set_value(show_trajectory, show)
        self.change_display(self.current_frame_index)

    def set_filter(self, filter_str: str) -> None:
        """
        过滤粒子显示
        :param filter_str: 过滤字符串, 支持"-"进行范围过滤，多个粒子可以使用","或者" "分割
        """
        print(f'filter string: {filter_str}')
        indexes = split_indexes_text(filter_str)
        print(f'filter list: {indexes}')
        self.settings.set_value(index_filter, indexes)
        self.change_display(self.current_frame_index)

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

    def update_mode(self, mode: OperationMode) -> None:
        """
        更新当前模式 MOVE/ADD/CROP
        :param mode: OperationMode
        """
        self.mode = mode

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        鼠标按下事件
        :param event: QGraphicsSceneMouseEvent
        """
        self.mouse_press_pos = event.scenePos()
        if self.mode == OperationMode.ADD:
            # 添加模式
            if self.current_frame_index in self.frames_base64:
                scene_pos = event.scenePos().toPoint()
                index, ok = QInputDialog.getInt(None, '输入', '粒子编号', 1)
                if ok:
                    self.graphic_items.add_particle(self.current_frame_index, index, (scene_pos.x(), scene_pos.y()))
                    self.change_display(self.current_frame_index)
            else:
                QMessageBox.information(self, '提示', f'未加载视频')
        super(VideoScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        鼠标松开事件
        :param event: QGraphicsSceneMouseEvent
        """
        pos = event.scenePos()
        # 移动距离
        moved = pos - self.mouse_press_pos
        # 如果有移动距离，并且有所选对象，进行移动
        if moved.manhattanLength() > 0:
            if len(self.selectedItems()) > 0:
                # 所有选中的粒子ID
                particle_ids = {item.index for item in self.selectedItems()}
                self.graphic_items.move_particles_by(self.current_frame_index, particle_ids, (moved.x(), moved.y()))
                self.change_display(self.current_frame_index)
        super(VideoScene, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        键盘事件
        :param event: QKeyEvent
        """
        if event.key() == Qt.Key.Key_Delete:
            # 按下删除键
            if len(self.selectedItems()) > 0:
                # 所有选中的粒子ID
                particle_ids = {item.index for item in self.selectedItems()}
                self.graphic_items.remove_particles(self.current_frame_index, particle_ids)
                self.change_display(self.current_frame_index)
        super(VideoScene, self).keyPressEvent(event)
