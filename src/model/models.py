from dataclasses import dataclass
from typing import Tuple, Any

from PySide6.QtGui import QColor


@dataclass
class VideoMetaInfo:
    """
    视频元数据对象
    """
    width: int = 0
    height: int = 0
    fps: int = 0
    frame_count: int = 0


@dataclass
class HistoryParticle:
    """
    历史粒子位置对象
    """
    frame_index: int
    center: Tuple[Any, ...]


@dataclass
class AnalyzeResult:
    """
    粒子分析数据
    frame: 帧
    particle_id: 粒子ID
    duration: 耗时, 秒
    x_px: 粒子x轴位置, 像素
    y_px: 粒子y轴位置, 像素
    x_micro: 粒子x轴位置, 微米
    y_micro: 粒子y轴位置, 微米
    distance: 距离, 微米
    velocity: 速度, 微米/秒
    angle: 角度, 与y轴正方向夹角, y轴正方向为0, 顺时针方向转动, 度[0, 360)
    """
    frame: int
    particle_id: int
    duration: float = 0
    x_px: float = 0
    y_px: float = 0
    x_micro: float = 0
    y_micro: float = 0
    distance: float = 0
    # velocity: float = 0
    angle: float = 0

    @property
    def velocity(self):
        return 0 if self.duration == 0 else self.distance / self.duration

    def data(self, index: int):
        if index == 0:
            return self.frame
        elif index == 1:
            return self.duration
        elif index == 2:
            return float(self.x_px)
        elif index == 3:
            return float(self.y_px)
        elif index == 4:
            return float(self.x_micro)
        elif index == 5:
            return float(self.y_micro)
        elif index == 6:
            return float(self.distance)
        elif index == 7:
            return float(self.velocity)
        elif index == 8:
            return float(self.angle)
        else:
            return None


@dataclass
class GradientColor:
    """
    渐变色每个位置颜色
    """
    pos: float
    color: QColor
