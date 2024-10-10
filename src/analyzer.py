import time

import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
import cv2


class Analyzer(QObject):
    sig_meta_info_updated = Signal(int)
    sig_frame_finished = Signal(int, np.ndarray)
    sig_first_frame_finished = Signal(int)
    sig_all_frame_finished = Signal()

    def __init__(self, parent=None):
        super(Analyzer, self).__init__(parent)

    @Slot(str)
    def analyze(self, path: str) -> None:
        video = cv2.VideoCapture(path)
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.sig_meta_info_updated.emit(total)
        if video.isOpened():
            index = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                index += 1
                self.sig_frame_finished.emit(index, frame)
                if index == 1:
                    self.sig_first_frame_finished.emit(1)
                if index == total:
                    self.sig_all_frame_finished.emit()
