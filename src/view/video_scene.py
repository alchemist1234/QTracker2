import os
from typing import Tuple, List

import cv2
import numpy as np

from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QInputDialog, QMessageBox,
                               QLineEdit, QWidget, QGraphicsRectItem, QGraphicsItem)
from PySide6.QtGui import QPixmap, QImage, QKeyEvent, QPen, QColorConstants, QPainter
from PySide6.QtCore import Slot, QByteArray, QBuffer, QPointF, Qt, QRectF, Signal

from src.model.models import DataHelper, OperationMode
from src.settings.default_settings import SettingKey
from src.settings.settings import Settings
from src.util.common_util import split_indexes_text


class VideoScene(QGraphicsScene):
    sig_export_start = Signal(int)
    sig_export_frame = Signal(int)
    sig_export_finish = Signal()

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
        self.graphic_items = DataHelper(self.settings)
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
    def add_frame(self, index: int, frame: np.ndarray) -> None:
        """
        添加帧图像
        :param index: 帧ID
        :param frame: 帧数据
        """
        h, w, c = frame.shape
        img = QImage(frame.data, w, h, QImage.Format.Format_RGB888)
        self.frames_base64[index] = self.__img_to_base64(img)

    @Slot(int)
    def change_display(self, index: int) -> None:
        """
        切换帧显示
        """
        self.current_frame_index = index
        self.__change_frame_display(index)
        self.__change_trajectory_display(index)
        self.__change_particle_display(index)

    @Slot()
    def change_to_next_frame(self) -> None:
        """
        切换到下一帧
        """
        next_frame = self.current_frame_index + 1
        if next_frame not in self.frames_base64:
            next_frame = 0
        self.change_display(next_frame)

    def sorted_frame_indexes(self):
        frame_indexes = list(self.frames_base64.keys())
        frame_indexes.sort()
        return frame_indexes

    def __change_frame_display(self, frame_index: int) -> None:
        """
        切换图像显示
        :param frame_index: 帧ID
        """
        if frame_index in self.frames_base64:
            base64 = self.frames_base64[frame_index]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            self.current_frame_item.setPixmap(QPixmap.fromImage(img))
        # 帧号
        if self.frame_label_item:
            self.removeItem(self.frame_label_item)
        self.frame_label_item = self.graphic_items.get_frame_label_item(frame_index)
        if self.frame_label_item:
            self.addItem(self.frame_label_item)

    def __change_particle_display(self, frame_index: int) -> None:
        """
        切换粒子显示
        :param frame_index: 帧ID
        """
        for item in self.particle_items:
            self.removeItem(item)
        # 设置显示/隐藏
        particle_shown = self.settings.boolean_value(SettingKey.show_particle)
        mark_shown = self.settings.boolean_value(SettingKey.show_mark)
        self.particle_items = self.graphic_items.get_particle_items(frame_index)
        for item in self.particle_items:
            item.set_particle_visible(particle_shown)
            item.set_mark_visible(mark_shown)
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
            item.setVisible(self.settings.boolean_value(SettingKey.show_trajectory))
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
        self.graphic_items.add_frame_label(frame_index)

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
                self.graphic_items.combine_particles(indexes)
                self.change_display(self.current_frame_index)
        else:
            self.graphic_items.combine_particles(indexes)
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

    @staticmethod
    def __img_to_base64(img: QImage) -> bytes:
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

    @Slot(OperationMode)
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
                self.graphic_items.move_particles_by(self.current_frame_index, particle_ids, (moved.x(), moved.y()))
                self.graphic_items.update_frame_items(self.current_frame_index)
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
                left = min(self.mouse_press_pos.x(), event.scenePos().x())
                right = max(self.mouse_press_pos.x(), event.scenePos().x())
                top = min(self.mouse_press_pos.y(), event.scenePos().y())
                bottom = max(self.mouse_press_pos.y(), event.scenePos().y())
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
                self.graphic_items.remove_particles(self.current_frame_index, particle_ids)
                self.change_display(self.current_frame_index)
        super(VideoScene, self).keyPressEvent(event)

    @Slot(str, int)
    def export(self, file_path: str, fps: int) -> None:
        """
        视频导出，支持裁切
        TODO 优化宽度高度获取
        TODO 区域的选择，裁切边框去除
        TODO 异常处理
        :param file_path: 导出文件位置
        :param fps: 帧率
        """
        indexes = self.sorted_frame_indexes()
        self.sig_export_start.emit(indexes[-1])
        file_name, file_ext = os.path.splitext(file_path)

        if self.crop_item.rect().width() > 0 and self.crop_item.rect().height() > 0:
            img_width = int(self.crop_item.rect().width())
            img_height = int(self.crop_item.rect().height())
            source = self.crop_item.rect()
        else:
            base64 = self.frames_base64[1]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            img_width = img.width()
            img_height = img.height()
            source = QRectF(0, 0, img_width, img_height)

        writer = cv2.VideoWriter()
        fourcc = VideoScene.codes_map[file_ext]
        writer.open(file_path, cv2.VideoWriter.fourcc(*fourcc), fps, (img_width, img_height), True)

        painter = QPainter()

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
