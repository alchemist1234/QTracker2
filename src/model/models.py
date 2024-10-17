from dataclasses import dataclass
from typing import Tuple, Any, Dict, Set, List, Collection

from src.view.custom_widget import ParticleItem, MarkItem, TrajectoryItem
from src.settings.settings import Settings


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


class ParticlePositions(object):
    """
    用于记录一个视频每一帧的粒子位置
    """

    def __init__(self):
        # {粒子ID : {帧ID : (x, y)}}
        self.particles: Dict[int, Dict[int, Tuple[int, int]]] = {}

    def add_particle(self, frame_index: int, particle_id: int, pos: Tuple[int, int]) -> None:
        """
        添加单个粒子
        :param frame_index: 帧ID
        :param particle_id: 粒子ID
        :param pos: 位置
        """
        frame_pos = self.particles.get(particle_id, {})
        frame_pos[frame_index] = pos
        self.particles[particle_id] = frame_pos

    def remove_frame_particles(self, frame_index: int) -> None:
        """
        移除一帧所有粒子
        :param frame_index: 帧ID
        """
        self.particles = {k: {k2: v2 for k2, v2 in v.items() if k2 != frame_index} for k, v in self.particles.items()}

    def add_frame_particles(self, frame_index: int, particles: Dict[int, Tuple[int, int]]) -> None:
        """
        添加一帧所有粒子
        :param frame_index: 帧ID
        :param particles: 所有粒子, {粒子ID: (x, y)}
        """
        # 移除所有粒子，再添加
        self.remove_frame_particles(frame_index)
        for particle_id, pos in particles.items():
            self.add_particle(frame_index, particle_id, pos)

    def get_frame_particles(self, frame_index: int, particle_ids: Collection[int] = None) -> Dict[int, Tuple[int, int]]:
        """
        获取一帧所有粒子
        :param frame_index: 帧ID
        :param particle_ids: 需要过滤的粒子ID, 默认不过滤
        :return: 粒子集合, {粒子ID: (x, y)}
        """
        if not particle_ids:
            particle_ids = set()
        particles = {k: {k2: v2 for k2, v2 in v.items() if k2 == frame_index}
                     for k, v in self.particles.items() if k in particle_ids or not particle_ids}
        return {k: v[frame_index] for k, v in particles.items() if len(v) > 0}

    def get_particles_before_frame(self, frame_index: int, particle_ids: Collection[int] = None) \
            -> Dict[int, List[Tuple[int, int]]]:
        """
        获取一帧之前（含当前帧）所有粒子有序点位，用于计算粒子轨迹
        :param frame_index: 帧ID
        :param particle_ids: 需要过滤的粒子ID, 默认不过滤
        :return: 粒子历史位置 {粒子ID: [(x1, y1), (x2, y2), ...]}
        """
        if not particle_ids:
            particle_ids = set()
        return {k: [v[k2] for k2 in sorted(v.keys()) if k2 <= frame_index] for
                k, v in self.particles.items() if frame_index in v and len(v[frame_index]) > 0
                and (k in particle_ids or not particle_ids)}

    def clear(self):
        self.particles.clear()


class GraphicItems(object):
    def __init__(self, particle_positions: ParticlePositions, settings: Settings):
        """
        存放所有帧的绘制Item
        :param particle_positions: 所有粒子数据
        :param settings: 配置信息
        """
        self.particle_positions = particle_positions
        self.settings = settings
        # {帧ID: {粒子ID: 粒子Item, ...}, ...}
        self.particle_items = {}
        # {帧ID: {粒子ID: 标记Item, ...}, ...}
        self.mark_items = {}
        # {帧ID: {粒子ID: 轨迹Item, ...}, ...}
        # 每帧轨迹ID只保存当前帧新增轨迹，显示时需要把小于等于当前帧所有轨迹Item全部展示
        self.trajectory_items = {}
        # self.particle_update_frames = set()
        # self.trajectory_update_frames = set()

    def generate_particle_items(self, frame_index: int) -> None:
        """
        创建帧粒子Item、标记Item
        :param frame_index: 帧ID
        """
        frame_particles = self.particle_positions.get_frame_particles(frame_index)
        if frame_index in self.particle_items:
            del self.particle_items[frame_index]
        if frame_index in self.mark_items:
            del self.mark_items[frame_index]
        frame_particle_items = {}
        frame_mark_items = {}
        for particle_id, pos in frame_particles.items():
            frame_particle_items[particle_id] = ParticleItem(self.settings, particle_id, pos[0], pos[1])
            # TODO 调用QGraphicsSimpleTextItem的setText方法会导致程序异常退出，怀疑是PySide版本问题，暂时屏蔽
            # frame_mark_items[particle_id] = MarkItem(self.settings, particle_id, pos[0], pos[1])

        self.particle_items[frame_index] = frame_particle_items
        self.mark_items[frame_index] = frame_mark_items

    def generate_trajectory_items(self, frame_index: int) -> None:
        """
        创建帧轨迹ID
        :param frame_index: 帧ID
        """
        particles = self.particle_positions.get_particles_before_frame(frame_index)
        if frame_index in self.trajectory_items:
            del self.trajectory_items[frame_index]
        frame_trajectory_items = {}
        for particle_id, pos_list in particles.items():
            if len(pos_list) < 2:
                continue
            start_pos = pos_list[-2]
            end_pos = pos_list[-1]
            frame_trajectory_items[particle_id] = TrajectoryItem(self.settings, particle_id, start_pos[0], start_pos[1],
                                                                 end_pos[0], end_pos[1])
        self.trajectory_items[frame_index] = frame_trajectory_items

    def get_particle_items(self, frame_index: int) -> List[ParticleItem]:
        """
        返回一帧所有粒子Item对象列表
        :param frame_index: 帧ID
        :return: 粒子Item对象列表
        """
        if frame_index in self.particle_items:
            return list(self.particle_items[frame_index].values())
        return []

    def get_trajectory_items(self, frame_index: int) -> List[TrajectoryItem]:
        """
        返回一帧所有轨迹Item对象列表
        :param frame_index: 帧ID
        :return: 轨迹Item对象列表
        """
        return [item for f_index, item_dict in self.trajectory_items.items() if f_index <= frame_index
                for item in item_dict.values()]

    def clear(self) -> None:
        """
        清空数据
        """
        self.particle_positions.clear()
        self.particle_items.clear()
        self.mark_items.clear()
        self.trajectory_items.clear()