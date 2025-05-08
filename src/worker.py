from enum import Enum
from typing import Dict, Tuple, List
import time

import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
import cv2

from src.model.models import VideoMetaInfo, HistoryParticle
from src.settings.default_settings import SettingKey
from src.settings.settings import Settings


class VideoLoader(QObject):
    """
    视频加载器
    """
    sig_meta_info_updated = Signal(VideoMetaInfo)
    sig_frame_finished = Signal(int, np.ndarray)
    sig_first_frame_finished = Signal(int)
    sig_all_frame_finished = Signal()

    def __init__(self, settings: Settings, parent=None):
        super(VideoLoader, self).__init__(parent)
        self.settings = settings

    @Slot(str)
    def load(self, path: str) -> None:
        """
        加载视频文件
        :param path: 视频文件地址
        """
        start_frame = self.settings.int_value(SettingKey.start_frame)
        stop_frame = self.settings.int_value(SettingKey.stop_frame)

        video = cv2.VideoCapture(path)
        # get meta info
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        if start_frame > frame_count:
            start_frame = 1
        stop_frame = min(stop_frame, frame_count)
        if 0 < start_frame <= stop_frame and stop_frame > 0:
            frame_count = min(stop_frame - start_frame + 1, frame_count)
        meta_info = VideoMetaInfo(width, height, fps, frame_count)
        self.sig_meta_info_updated.emit(meta_info)

        skips = 0

        if video.isOpened():
            index = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    if index != frame_count:
                        # 如果读取的帧数与元数据帧数不一样，重新发送meta_info_updated信号
                        meta_info.frame_count = index
                        self.sig_meta_info_updated.emit(meta_info)
                    self.sig_all_frame_finished.emit()
                    break
                if skips < start_frame - 1:
                    skips += 1
                    continue

                index += 1

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.sig_frame_finished.emit(index, frame)
                # if index == 1:
                #     self.sig_first_frame_finished.emit(1)
                if index == frame_count:
                    self.sig_all_frame_finished.emit()
                    break


class Analyzer(QObject):
    """
    视频分析器
    """
    sig_frame_analyzed = Signal(int, list)

    class Judgement(Enum):
        FALSE = 0b_00
        TRUE = 0b_01
        TOUCHING_FALSE = 0b_10
        TOUCHING_TRUE = 0b_11

    def __init__(self, settings: Settings, parent=None):
        super(Analyzer, self).__init__(parent)
        self.settings = settings
        self.history_particles = {}
        self.max_label = 0

        # 待分析视频帧数据
        # [(frame_index, ndarray)]
        self.data_queue: List[Tuple[int, np.ndarray]] = []
        # 是否正在分析
        self.working = False
        # 当前视频所有帧是否已全部发送到self.data_queue
        self.receiving = False
        # 是否在循环中
        # self.working用于外部更改使循环停止, self.running用于记录循环真实运行情况
        self.running = False

    @Slot()
    def run(self) -> None:
        self.running = True
        # 循环分析视频帧
        while True:
            if not self.working:
                # 停止任务时结束循环
                break
            if not self.receiving and len(self.data_queue) == 0:
                # 分析完成时结束循环
                break
            # 本次循环是否有任务进行，没有则等待0.5s后进入下一循环，避免死循环频率过高占用CPU
            work = False
            if len(self.data_queue) > 0:
                work = True
                data = self.data_queue.pop(0)
                frame_index, frame = data
                particle_pos = self.analyze(frame_index, frame)
                if self.working and particle_pos is not None:
                    # 发送帧分析完成信号
                    self.sig_frame_analyzed.emit(frame_index, list(particle_pos.items()))
            if not work:
                time.sleep(0.5)
        self.running = False

    def start_and_run(self) -> None:
        """
        开始分析视频
        """
        self.working = True
        self.receiving = True
        if not self.running:
            self.run()

    def stop(self) -> None:
        """
        停止分析, 清空数据
        1. 停止接收数据、停止循环（非强行停止，需要等到当前循环结束）
        2. 清除已接收数据
        3. 清除历史数据
        4. 最大粒子ID重置为0
        """
        self.working = False
        self.receiving = False
        self.data_queue.clear()
        self.history_particles.clear()
        self.max_label = 0

    def add_data(self, frame_index: int, frame: np.ndarray) -> None:
        """
        添加视频帧数据
        :param frame_index: 视频帧ID
        :param frame: 视频帧数据
        """
        self.data_queue.append((frame_index, frame))

    def all_data_received(self):
        """
        所有视频帧已接收完成
        """
        self.receiving = False

    def analyze(self, frame_index: int, frame: np.ndarray) -> Dict[int, Tuple[int, int]]:
        """
        分析视频数据
        :param frame_index: 帧ID
        :param frame: 帧数据
        :return: 当前帧所有粒子
        """
        frame_particles = {}
        frame, frame_gray = self.smooth(frame)
        binary = self.binary(frame_gray)
        contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        m_list, cnt_list = self.get_contours(contours)

        ordered_centers = [self.get_contour_info(m) for m in m_list]

        memory_frames = self.settings.int_value(SettingKey.memory_frames)
        search_radius = self.settings.int_value(SettingKey.search_radius)

        x = 0
        try:
            for center_tuple in ordered_centers:
                for index, history_center in self.history_particles.items():
                    x += 1
                    if frame_index - history_center.frame_index <= memory_frames and \
                            self.same_particle(history_center.center, center_tuple, search_radius):
                        history_center.frame_index = frame_index
                        history_center.center = center_tuple
                        frame_particles[index] = center_tuple
                        break
                else:
                    frame_particles[self.max_label] = center_tuple
                    self.history_particles[self.max_label] = HistoryParticle(frame_index, center_tuple)
                    self.max_label += 1
        except Exception as e:
            # 防止分析过程中重新加载视频，self.history_particles被清空，遍历时报错导致线程退出后无法再次分析
            pass
        return frame_particles

    @staticmethod
    def same_particle(old_center: Tuple[int, int], new_center: Tuple[int, int], dis: int) -> bool:
        """
        判断两个粒子是否为同一个
        :param old_center: 原位置
        :param new_center: 新位置
        :param dis: 判断范围
        :return: 是否同一粒子
        """
        return abs(new_center[0] - old_center[0]) <= dis and abs(new_center[1] - old_center[1]) <= dis

    def smooth(self, frame):
        """
        图像平滑
        :param frame: 图像帧
        :return: 平滑后图像, 灰度图像
        """
        if len(frame.shape) == 3:
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = frame
        # 直方图均衡化
        if self.settings.boolean_value(SettingKey.apply_hist_eq):
            image_gray = cv2.equalizeHist(image_gray)
        # 自适应直方图均衡化
        adaptive_hist_limit = self.settings.int_value(SettingKey.adaptive_hist_limit)
        clahe = cv2.createCLAHE(clipLimit=adaptive_hist_limit, tileGridSize=(8, 8))
        image_gray = clahe.apply(image_gray)
        # 双边滤波
        bilateral_size = self.settings.int_value(SettingKey.bilateral_size)
        bilateral_color = self.settings.int_value(SettingKey.bilateral_color)
        bilateral_space = self.settings.int_value(SettingKey.bilateral_space)
        if bilateral_size != 0:
            image_gray = cv2.bilateralFilter(image_gray, bilateral_size, bilateral_color, bilateral_space)
        # 中值模糊
        image_gray = cv2.medianBlur(image_gray, self.settings.int_value(SettingKey.median_blur))
        # 高斯模糊
        image_gray = cv2.GaussianBlur(image_gray, (self.settings.int_value(SettingKey.gaussian_blur),) * 2, 0)
        frame = image_gray.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame, image_gray

    def binary(self, image):
        """
        二值化
        :param image: 图像帧
        :return: 二值化后图像
        """
        derivative_order = self.settings.int_value(SettingKey.derivative_order)
        sobel_x = self.get_sobel(image, derivative_order, 0)
        sobel_y = self.get_sobel(image, 0, derivative_order)
        sobel_both = cv2.bitwise_or(sobel_x, sobel_y)
        return sobel_both

    def get_sobel(self, image, x, y):
        kernel_size = self.settings.int_value(SettingKey.kernel_size)
        sobel = cv2.Sobel(image, cv2.CV_64F, x, y, kernel_size)
        sobel = np.absolute(sobel)
        sobel = sobel - sobel.min()
        thresh = np.zeros(sobel.shape, np.uint8)
        thresh[sobel > kernel_size] = 255
        sobel = self.morphology(thresh)
        return sobel

    def morphology(self, image):
        kernel = np.ones((self.settings.int_value(SettingKey.closing_size),) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((self.settings.int_value(SettingKey.opening_size),) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return image

    def get_contours(self, contours):
        m_list = []
        cnt_list = []
        max_area = self.settings.int_value(SettingKey.maximum_area_for_detection)
        min_area = self.settings.int_value(SettingKey.minimum_area_for_detection)
        split_radius = self.settings.int_value(SettingKey.split_radius)
        split_area = (split_radius * 1.05) ** 2 * np.pi
        split = self.settings.boolean_value(SettingKey.split_circular_particles)

        for cnt_index in range(len(contours)):
            cnt = contours[cnt_index]
            judgement, moment = self.particle_test(cnt, min_area, max_area, split, split_area)

            if judgement == Analyzer.Judgement.TRUE.value:
                m_list.append(moment)
                cnt_list.append(cnt)
        return m_list, cnt_list

    @staticmethod
    def particle_test(contours, min_area: int, max_area: int, split: bool, split_area: float | None):
        moments = cv2.moments(contours)
        area = moments['m00']

        judgement = Analyzer.Judgement.FALSE.value
        if min_area < area <= max_area:
            judgement = Analyzer.Judgement.TRUE.value

        if split:
            is_touching = split_area <= area
            if is_touching:
                judgement = judgement | 0b_10
        return judgement, moments

    @staticmethod
    def get_contour_info(m):
        area = m['m00']
        cx = int(round(m['m10'] / area))
        cy = int(round(m['m01'] / area))
        return cx, cy

    @staticmethod
    def split_particles_roi(radius, cnt):
        x, y, w, h = cv2.boundingRect(cnt)
        roi_touching = np.zeros((h, w), dtype=np.uint8)
        cnt = cnt - np.array([x, y])
        cv2.drawContours(roi_touching, [cnt], 0, 255, -1)

        ff = 3
        roi_touching = cv2.resize(roi_touching, None, fx=ff, fy=ff, interpolation=cv2.INTER_LINEAR)
        radius = ff * radius
        cnt_list_split = Analyzer.split_particles(roi_touching, radius)
        cnt_list_split = [c / ff + np.array([x, y]) for c in cnt_list_split]
        return cnt_list_split

    @staticmethod
    def split_particles(binary, radius):
        r = int(radius * 0.75)
        kernel = Analyzer.circular_kernel(r)
        eroded = cv2.erode(binary, kernel, iterations=1)
        erode_contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnt_list_split = []
        for cnt in erode_contours:
            split_particle = np.zeros(binary.shape, np.uint8)
            cv2.drawContours(split_particle, [cnt], 0, 255, -1)
            split_particle = cv2.dilate(split_particle, kernel, iterations=1)
            split_cnt, _ = cv2.findContours(split_particle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt_list_split.append(split_cnt[0])
        return cnt_list_split

    @staticmethod
    def circular_kernel(r: int):
        y, x = np.ogrid[-r: r + 1, -r: r + 1]
        return (y * y + x * x <= r * r).astype(np.uint8)
