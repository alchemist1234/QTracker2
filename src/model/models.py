from dataclasses import dataclass
from typing import Tuple, Any, Dict, List, Collection, Optional
from enum import Enum

from src.view.custom_widget import TrajectoryItem, ParticleGroup
from src.settings.settings import Settings
from src.settings.default_settings import index_filter


class OperationMode(Enum):
    """
    VideoScene 的操作类型
    """
    MOVE = 0
    CROP = 1
    ADD = 2


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
        particle_pos = self.particles.get(particle_id, {})
        particle_pos[frame_index] = pos
        self.particles[particle_id] = particle_pos

    def move_particle_by(self, frame_index: int, particle_id: int, vector: Tuple[int, int]) -> None:
        """
        移动粒子
        :param frame_index: 帧
        :param particle_id: 粒子ID
        :param vector: 位移 (dx, dy)
        """
        particle_pos = self.particles.get(particle_id, {})
        if frame_index in particle_pos:
            pos = particle_pos[frame_index]
            particle_pos[frame_index] = (pos[0] + vector[0], pos[1] + vector[1])

    def remove_particle(self, frame_index: int, particle_id: int) -> None:
        """
        删除粒子
        :param frame_index: 帧
        :param particle_id: 粒子ID
        """
        particle_pos = self.particles.get(particle_id, {})
        if frame_index in particle_pos:
            del particle_pos[frame_index]

    def next_frame(self, frame_index: int, particle_id: int) -> Optional[int]:
        """
        获取某个粒子在一帧之后首次出现的帧，如果之后再未出现过，返回None
        :param frame_index: 帧
        :param particle_id: 粒子ID
        :return: 粒子下一次出现的帧，可能为None
        """
        particle_pos = self.particles.get(particle_id, {})
        # 粒子后续出现的所有帧
        next_frame_indexes = [i for i in particle_pos.keys() if i > frame_index]
        # 取最小值
        return min(next_frame_indexes) if len(next_frame_indexes) > 0 else None

    def remove_frame_particles(self, frame_index: int) -> None:
        """
        移除一帧所有粒子
        :param frame_index: 帧ID
        """
        self.particles = {particle_id: {frame: pos for frame, pos in frame_pos_dict.items() if frame != frame_index}
                          for particle_id, frame_pos_dict in self.particles.items()}

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

    def combine_particles(self, particle_ids: Collection[int]) -> List[int]:
        """
        合并多个粒子，新粒子会以最小粒子ID作为新ID，每一帧的粒子位置优先设置为原ID更小的粒子位置
        例如
        粒子1在各帧的位置为 {1: (x11, y11), 2: (x12, y12)}
        粒子2在各帧的位置为 {2: (x22, y22), 3: (x23, y23)}
        粒子3在各帧的位置为 {4: (x34, y34), 5: (x35, y35)}
        1、2、3粒子合并后
        新粒子ID为1, 各帧位置为{1: (x11, y11), 2: (x12, y12), 3: (x23, y23), 4: (x34, y34), 5: (x35, y35)}
        :param particle_ids: 需要合并的粒子
        :return: 新粒子所在的帧
        """
        if particle_ids is None or len(particle_ids) <= 1:
            return []
        # 粒子ID倒序排列
        particle_ids_desc = list(particle_ids)
        particle_ids_desc.sort(reverse=True)
        min_id = particle_ids_desc[-1]
        max_id = particle_ids_desc[0]
        particle_pos = self.particles.get(max_id, {})
        for particle_id in particle_ids_desc:
            # 倒序遍历所有粒子
            if particle_id in self.particles:
                pos = self.particles.get(particle_id, {})
                # 合并两个粒子位置，同时存在的帧使用ID更小的粒子位置
                particle_pos.update(pos)
                # 删除旧粒子数据
                del self.particles[particle_id]
        # 合并后的粒子使用原最小ID
        self.particles[min_id] = particle_pos
        return list(particle_pos.keys())

    def get_frame_particles(self, frame_index: int, particle_ids: Collection[int] = None) -> Dict[int, Tuple[int, int]]:
        """
        获取一帧所有粒子
        :param frame_index: 帧ID
        :param particle_ids: 需要过滤的粒子ID, 默认不过滤
        :return: 粒子集合, {粒子ID: (x, y)}
        """
        if not particle_ids:
            # particle_ids为None时返回所有粒子
            particle_ids = set()
        # 过滤出粒子在目标帧所在的位置, value可能为{}
        # {粒子ID: {目标帧ID: 粒子位置}, ...}
        particles = {particle_id: {frame: pos for frame, pos in frame_pos_dict.items()
                                   if frame == frame_index}
                     for particle_id, frame_pos_dict in self.particles.items()
                     if particle_id in particle_ids or not particle_ids}
        # 将结果转换成{粒子ID: 粒子位置, ...}，并过滤掉在该帧没有数据的粒子
        return {particle_id: frame_pos_dict[frame_index] for particle_id, frame_pos_dict in particles.items()
                if len(frame_pos_dict) > 0}

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
        return {particle_id: [frame_pos_dict[frame] for frame in sorted(frame_pos_dict.keys())
                              if frame <= frame_index]
                for particle_id, frame_pos_dict in self.particles.items()
                if frame_index in frame_pos_dict and len(frame_pos_dict[frame_index]) > 0
                and (particle_id in particle_ids or not particle_ids)}

    def clear(self):
        self.particles.clear()


class GraphicItems(object):
    def __init__(self, settings: Settings):
        """
        存放所有帧的绘制Item
        :param settings: 配置信息
        """
        self.particle_positions = ParticlePositions()
        self.settings: Settings = settings
        # {帧ID: {粒子ID: 粒子Group, ...}, ...}
        self.particle_group: Dict[int, Dict[int, ParticleGroup]] = {}
        # {帧ID: {粒子ID: 轨迹Item, ...}, ...}
        # 每帧轨迹ID只保存当前帧新增轨迹，显示时需要把小于等于当前帧所有轨迹Item全部展示
        self.trajectory_items: Dict[int, Dict[int, TrajectoryItem]] = {}

    def add_particle(self, frame_index: int, particle_id: int, pos: Tuple[int, int]) -> None:
        """
        添加单个粒子，并更新受影响的帧对象
        :param frame_index: 帧
        :param particle_id: 粒子ID
        :param pos: 粒子位置
        """
        self.particle_positions.add_particle(frame_index, particle_id, pos)
        self.update_frame_items(frame_index)
        self.update_frame_items(self.particle_positions.next_frame(frame_index, particle_id))

    def add_frame_particles(self, frame_index: int, particles: Dict[int, Tuple[int, int]]) -> None:
        """
        更新一帧所有粒子
        不会更新所有受影响的帧对象，只会更新当前帧对象
        :param frame_index: 帧
        :param particles: 粒子位置 {粒子ID: (x, y), ...}
        :return:
        """
        self.particle_positions.add_frame_particles(frame_index, particles)
        self.update_frame_items(frame_index)

    def remove_particle(self, frame_index: int, particle_id: int) -> None:
        """
        删除单个粒子，并更新所有受影响的帧
        :param frame_index: 帧
        :param particle_id: 粒子ID
        """
        self.particle_positions.remove_particle(frame_index, particle_id)
        self.update_frame_items(frame_index)
        self.update_frame_items(self.particle_positions.next_frame(frame_index, particle_id))

    def remove_particles(self, frame_index: int, particle_ids: Collection[int]) -> None:
        """
        删除多个粒子，并更新所有受影响的帧
        :param frame_index: 帧
        :param particle_ids: 粒子ID集合
        """
        updated_frames = {frame_index}
        for particle_id in particle_ids:
            self.particle_positions.remove_particle(frame_index, particle_id)
            updated_frames.add(self.particle_positions.next_frame(frame_index, particle_id))
        for frame in updated_frames:
            self.update_frame_items(frame)

    def remove_frame_particles(self, frame_index: int) -> None:
        """
        删除一帧所有粒子
        不会更新所有受影响的帧对象，只会更新当前帧对象
        :param frame_index: 帧
        """
        self.particle_positions.remove_frame_particles(frame_index)
        self.update_frame_items(frame_index)

    def move_particle_by(self, frame_index: int, particle_id: int, vector: Tuple[int, int]) -> None:
        """
        移动单个粒子，并更新所有受影响的帧
        :param frame_index: 帧
        :param particle_id: 粒子ID
        :param vector: 位移 (dx, dy)
        """
        self.particle_positions.move_particle_by(frame_index, particle_id, vector)
        self.update_frame_items(frame_index)
        self.update_frame_items(self.particle_positions.next_frame(frame_index, particle_id))

    def move_particles_by(self, frame_index: int, particle_ids: Collection[int], vector: Tuple[int, int]) -> None:
        """
        移动多个粒子，并更新所有受影响的帧
        :param frame_index: 帧
        :param particle_ids: 粒子ID
        :param vector: 位移 (dx, dy)
        """
        print(f'move particles {particle_ids} at frame {frame_index} by {vector}')
        updated_frames = {frame_index}
        for particle_id in particle_ids:
            self.particle_positions.move_particle_by(frame_index, particle_id, vector)
            updated_frames.add(self.particle_positions.next_frame(frame_index, particle_id))
        for frame in updated_frames:
            self.update_frame_items(frame)

    def combine_particles(self, particle_ids: Collection[int]) -> None:
        """
        合并多个粒子，并更新所有涉及帧对象
        :param particle_ids: 需要合并的粒子
        """
        if particle_ids is None or len(particle_ids) == 0:
            return
        frame_index = self.particle_positions.combine_particles(particle_ids)
        for frame in frame_index:
            self.update_frame_items(frame)

    def update_frame_items(self, frame_index: int) -> None:
        """
        更新一帧所有QGraphicItem，并更新所有受影响的帧
        :param frame_index: 帧
        """
        if frame_index is not None:
            self.__update_particle_items(frame_index)
            self.__update_trajectory_items(frame_index)

    def __update_particle_items(self, frame_index: int) -> None:
        """
        更新帧粒子Item、标记Item
        :param frame_index: 帧ID
        """
        frame_particles = self.particle_positions.get_frame_particles(frame_index)
        if frame_index in self.particle_group:
            del self.particle_group[frame_index]
        frame_particle_group = {}
        for particle_id, pos in frame_particles.items():
            frame_particle_group[particle_id] = ParticleGroup(self.settings, particle_id, pos[0], pos[1])

        self.particle_group[frame_index] = frame_particle_group

    def __update_trajectory_items(self, frame_index: int) -> None:
        """
        更新帧轨迹Item
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

    def get_particle_items(self, frame_index: int) -> List[ParticleGroup]:
        """
        返回一帧所有粒子Item对象列表
        :param frame_index: 帧ID
        :return: 粒子Item对象列表
        """
        if frame_index in self.particle_group:
            filtered_particles = self.settings.list_value(index_filter)
            return [item for particle_id, item in self.particle_group[frame_index].items()
                    if particle_id in filtered_particles or not filtered_particles]
        return []

    def get_trajectory_items(self, frame_index: int) -> List[TrajectoryItem]:
        """
        返回一帧所有轨迹Item对象列表
        :param frame_index: 帧ID
        :return: 轨迹Item对象列表
        """
        filtered_particles = self.settings.list_value(index_filter)
        return [item for f_index, item_dict in self.trajectory_items.items() if f_index <= frame_index
                for particle_id, item in item_dict.items()
                if particle_id in filtered_particles or not filtered_particles]

    def clear(self) -> None:
        """
        清空数据
        """
        self.particle_positions.clear()
        self.trajectory_items.clear()
