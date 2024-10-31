from enum import Enum


class OperationMode(Enum):
    """
    VideoScene 的操作类型
    """
    MOVE = 0
    CROP = 1
    ADD = 2


class WorkingState(Enum):
    LOAD = 0, '加载'
    ANALYZE = 1, '分析'
    CALCULATE = 2, '计算'
    EXPORT = 3, '导出'


class FrameLabelPos(Enum):
    LEFT_TOP = 0
    LEFT_BOTTOM = 1
    RIGHT_TOP = 2
    RIGHT_BOTTOM = 3
