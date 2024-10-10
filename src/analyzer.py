import time

import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
import cv2


class Analyzer(QObject):
    sig_frame_finished = Signal(int, np.ndarray)

    def __init__(self, parent=None):
        super(Analyzer, self).__init__(parent)

    @Slot(str)
    def analyze(self, path: str) -> None:
        video = cv2.VideoCapture(path)
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        if video.isOpened():
            index = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                index += 1
                self.sig_frame_finished.emit(index, frame)
