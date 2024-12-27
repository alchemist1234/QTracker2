import os
from typing import Tuple, List
import asyncio

import cv2
import numpy as np

from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QInputDialog, QMessageBox,
                               QLineEdit, QWidget, QGraphicsRectItem, QGraphicsItem)
from PySide6.QtGui import QPixmap, QImage, QKeyEvent, QPen, QColorConstants, QPainter
from PySide6.QtCore import Slot, QByteArray, QBuffer, QPointF, Qt, QRectF, Signal

from src.model.qt_models import DataHelper
from src.model.enums import OperationMode
from src.settings.default_settings import SettingKey
from src.settings.settings import Settings
from src.util.common_util import split_indexes_text


class VideoScene(QGraphicsScene):
    sig_export_start = Signal(int)
    sig_export_frame = Signal(int)
    sig_export_finish = Signal()
    sig_frame_changed = Signal(int)
    sig_calculate_particle = Signal(int, int)

    codes_map = {
        '.avi': 'XVID',
        '.flv': 'FLV1',
        '.mp4': 'X264',
        '.ogv': 'THEO'
    }

    def __init__(self, parent: QWidget = None, settings: Settings = None):
        super().__init__(parent)
        # 设置图形项搜索方法
        self.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)
        self.settings = settings
        # 当前操作模式
        self.mode = OperationMode.MOVE
        # 用base64存储图像数据，用QImage或者QPixmap存储内存占用过大
        self.frames_base64 = {}
        # GraphicItem存储容器
        self.data_helper = DataHelper(self.settings)
        # 当前添加到QGraphicsScene中的粒子Item
        self.particle_items = []
        # 当前添加到QGraphicsScene中的轨迹Item
        self.trajectory_items = []
        # 当前帧
        self.current_frame_index = -1
        # 当前鼠标按下位置
        self.mouse_press_pos = QPointF()

        # 帧图像对象
        self.current_frame_item = QGraphicsPixmapItem()
        self.addItem(self.current_frame_item)

        # 帧号对象
        self.frame_label_item = None

        # 裁切框
        self.crop_item: QGraphicsRectItem = self.create_crop_item()
        self.addItem(self.crop_item)
        # 粒子计算完后发出信号，更新状态栏
        self.data_helper.sig_calculate_particle.connect(self.__calculate_particle)

    @staticmethod
    def create_crop_item() -> QGraphicsRectItem:
        """
        创建裁切边框
        :return:
        """
        item = QGraphicsRectItem()
        pen = QPen()
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setColor(QColorConstants.Green)
        item.setPen(pen)
        item.setVisible(False)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        return item

    @Slot(int, np.ndarray)
    async def add_frame(self, index: int, frame: np.ndarray) -> None:
        """
        添加帧图像
        :param index: 帧ID
        :param frame: 帧数据
        """
        h, w, c = frame.shape
        img = QImage(frame.data, w, h, QImage.Format.Format_RGB888)
        await self.save_frame_base64(index, img)

    @Slot(int)
    def change_display(self, index: int) -> None:
        """
        切换帧显示
        """
        self.current_frame_index = index
        self.__change_frame_display(index)
        self.__change_trajectory_display(index)
        self.__change_particle_display(index)
        self.sig_frame_changed.emit(index)

    @Slot()
    def change_to_next_frame(self) -> None:
        """
        切换到下一帧
        """
        next_frame = self.current_frame_index + 1
        if next_frame not in self.frames_base64:
            next_frame = 0
        self.change_display(next_frame)

    def sorted_frame_indexes(self) -> List[int]:
        """
        当前所有帧号(顺序)
        :return: 有序帧号
        """
        frame_indexes = list(self.frames_base64.keys())
        frame_indexes.sort()
        return frame_indexes

    def __change_frame_display(self, frame_index: int) -> None:
        """
        切换图像显示
        :param frame_index: 帧ID
        """
        width, height = 0, 0
        if frame_index in self.frames_base64:
            base64 = self.frames_base64[frame_index]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            pixmap = QPixmap.fromImage(img)
            width, height = pixmap.width(), pixmap.height()
            self.current_frame_item.setPixmap(pixmap)
        # 帧号
        if self.frame_label_item:
            self.removeItem(self.frame_label_item)
        self.frame_label_item = self.data_helper.get_frame_label_item(frame_index)
        if self.frame_label_item:
            self.frame_label_item.refresh(width, height)
            self.addItem(self.frame_label_item)

    def __change_particle_display(self, frame_index: int) -> None:
        """
        切换粒子显示
        :param frame_index: 帧ID
        """
        for item in self.particle_items:
            self.removeItem(item)
        self.particle_items = self.data_helper.get_particle_items(frame_index)
        for item in self.particle_items:
            item.refresh()
            self.addItem(item)

    def __change_trajectory_display(self, frame_index: int) -> None:
        """
        切换轨迹显示
        :param frame_index: 帧ID
        """
        for item in self.trajectory_items:
            self.removeItem(item)
        self.trajectory_items = self.data_helper.get_trajectory_items(frame_index)
        for item in self.trajectory_items:
            item.refresh()
            self.addItem(item)

    @Slot(int, list)
    def add_frame_particles(self, frame_index: int, particles: List[Tuple[int, Tuple[int, int]]]):
        """
        添加一帧所有粒子
        :param frame_index: 帧ID
        :param particles: 粒子数据, {粒子ID:(x, y),...}
        """
        particle_map = {p[0]: p[1] for p in particles}
        self.data_helper.add_frame_particles(frame_index, particle_map)
        self.data_helper.add_frame_label(frame_index)

    @Slot()
    def combine_particles(self) -> None:
        """
        合并粒子
        """
        indexes = {item.index for item in self.selectedItems() if hasattr(item, 'index')}
        if len(indexes) == 0:
            text, ok = QInputDialog.getText(None, "输入", "待合并的粒子编号(,或者空格分隔)", QLineEdit.EchoMode.Normal)
            if ok:
                indexes = split_indexes_text(text)
                self.data_helper.combine_particles(indexes)
                self.change_display(self.current_frame_index)
        else:
            self.data_helper.combine_particles(indexes)
            self.change_display(self.current_frame_index)

    @Slot(bool)
    def set_particle_visible(self, show: bool) -> None:
        """
        是否显示粒子
        :param show: 是否显示
        """
        self.settings.set_value(SettingKey.show_particle, show)
        self.change_display(self.current_frame_index)

    @Slot(bool)
    def set_mark_visible(self, show: bool) -> None:
        """
        是否显示标记
        :param show: 是否显示
        """
        self.settings.set_value(SettingKey.show_mark, show)
        self.change_display(self.current_frame_index)

    @Slot(bool)
    def set_trajectory_visible(self, show: bool) -> None:
        """
        是否显示轨迹
        :param show: 是否显示
        """
        self.settings.set_value(SettingKey.show_trajectory, show)
        self.change_display(self.current_frame_index)

    @Slot(str)
    def set_filter(self, filter_str: str) -> None:
        """
        过滤粒子显示
        :param filter_str: 过滤字符串, 支持"-"进行范围过滤，多个粒子可以使用","或者" "分割
        """
        indexes = split_indexes_text(filter_str)
        self.settings.set_value(SettingKey.index_filter, indexes)
        self.change_display(self.current_frame_index)

    def set_frame_label_visible(self, show: bool) -> None:
        """
        是否显示帧号
        :param show: 是否隐藏
        """
        self.settings.set_value(SettingKey.show_frame_label, show)
        self.change_display(self.current_frame_index)

    async def save_frame_base64(self, index: int, img: QImage):
        """
        QImage 转 Base64
        :param index: 帧号
        :param img: QImage
        :return: Base64 bytes
        """
        # quality = self.settings.int_value(default_settings.frame_quality)
        byte_arr = QByteArray()
        buffer = QBuffer(byte_arr)
        buffer.open(QBuffer.OpenModeFlag.WriteOnly)
        img.save(buffer, 'jpg', 100)
        self.frames_base64[index] = byte_arr.toBase64().data()
        if index == 1:
            self.change_display(1)

    def clear_data(self) -> None:
        """
        清除所有数据
        """
        self.current_frame_index = -1
        # 通过切换帧到-1来清除Scene上的所有Item，避免把一些固有对象(比如图像Item和裁切Item)清除
        self.change_display(-1)
        self.data_helper.clear()
        self.frames_base64.clear()
        self.data_helper.clear()
        self.particle_items.clear()
        self.trajectory_items.clear()
        self.frame_label_item = None
        self.current_frame_item.setPixmap(QPixmap())

    @Slot(OperationMode)
    def update_mode(self, mode: OperationMode) -> None:
        """
        更新当前模式 MOVE/ADD/CROP
        :param mode: OperationMode
        """
        self.mode = mode

    def __calculate_particle(self, current: int, total: int) -> None:
        """
        中转粒子计算完信号
        :param current: 已计算完粒子数
        :param total: 总粒子数
        """
        self.sig_calculate_particle.emit(current, total)

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
                    self.data_helper.add_particle(self.current_frame_index, index, (scene_pos.x(), scene_pos.y()))
                    self.change_display(self.current_frame_index)
            else:
                QMessageBox.information(self, '提示', f'未加载视频')
        elif self.mode == OperationMode.CROP:
            # 裁切模式
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.crop_item.setRect(QRectF(event.scenePos(), event.scenePos()))
                self.crop_item.setVisible(True)
            if event.buttons() == Qt.MouseButton.RightButton:
                self.crop_item.setRect(QRectF(0, 0, 0, 0))
                self.crop_item.setVisible(False)
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
            selected = self.selectedItems()
            particle_ids = {item.index for item in selected if hasattr(item, 'index')}
            if len(particle_ids) > 0:
                # 所有选中的粒子ID
                self.data_helper.move_particles_by(self.current_frame_index, particle_ids, (moved.x(), moved.y()))
                self.data_helper.update_frame_items(self.current_frame_index)
                # 这里更新不能调用self.change_display(), 会导致selectedItems清空, 下次移动时坐标会变成(0, 0)
                self.__change_trajectory_display(self.current_frame_index)

        super(VideoScene, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        鼠标移动事件
        :param event: QGraphicsSceneMouseEvent
        """
        if self.mode == OperationMode.CROP:
            # 裁切模式下左键拖拽，绘制裁切框
            if event.buttons() == Qt.MouseButton.LeftButton:
                # 因导出的时候为避免将裁切边框显示出来，将裁切范围左、上位置缩小了1像素，所以在绘制边框时扩大1像素
                left = min(self.mouse_press_pos.x(), event.scenePos().x()) - 1
                right = max(self.mouse_press_pos.x(), event.scenePos().x())
                top = min(self.mouse_press_pos.y(), event.scenePos().y()) - 1
                bottom = max(self.mouse_press_pos.y(), event.scenePos().y())
                # 避免边框超出图片边界
                top = max(-1.0, top)
                left = max(-1.0, left)
                right = min(self.current_frame_item.pixmap().width() * 1.0, right)
                bottom = min(self.current_frame_item.pixmap().height() * 1.0, bottom)
                self.crop_item.setRect(QRectF(left, top, right - left, bottom - top))
        else:
            super(VideoScene, self).mouseMoveEvent(event)

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
                self.data_helper.remove_particles(self.current_frame_index, particle_ids)
                self.change_display(self.current_frame_index)
        super(VideoScene, self).keyPressEvent(event)

    @Slot(str, int)
    def export(self, file_path: str, fps: int) -> None:
        """
        视频导出，支持裁切
        TODO 异常处理
        :param file_path: 导出文件位置
        :param fps: 帧率
        """
        indexes = self.sorted_frame_indexes()
        self.sig_export_start.emit(indexes[-1])
        file_name, file_ext = os.path.splitext(file_path)

        # 获取图像高、宽，以及需要保存的区域
        if self.crop_item.rect().width() > 0 and self.crop_item.rect().height() > 0:
            img_width = int(self.crop_item.rect().width())
            img_height = int(self.crop_item.rect().height())
            rect = self.crop_item.rect()
            source = QRectF(rect.x() + 1, rect.y() + 1, img_width - 1, img_height - 1)
        else:
            img_width = self.current_frame_item.pixmap().width()
            img_height = self.current_frame_item.pixmap().height()
            source = QRectF(0, 0, img_width, img_height)

        writer = cv2.VideoWriter()
        fourcc = VideoScene.codes_map[file_ext]
        writer.open(file_path, cv2.VideoWriter.fourcc(*fourcc), fps, (img_width, img_height), True)

        painter = QPainter()

        # 逐帧导出
        for frame in indexes:
            self.change_display(frame)
            img = QImage(img_width, img_height, QImage.Format.Format_ARGB32)
            painter.begin(img)
            self.render(painter, source=source)
            painter.end()
            shape = (img.height(), img.bytesPerLine() * 8 // img.depth(), 4)
            ptr = img.bits()
            arr = np.array(ptr, dtype=np.uint8).reshape(shape)
            arr = arr[..., :3]
            writer.write(arr)
            self.sig_export_frame.emit(frame)

        writer.release()
        self.sig_export_finish.emit()

    def refresh_items(self) -> None:
        """
        显示设置更新后, 刷新item显示
        """
        self.change_display(self.current_frame_index)
