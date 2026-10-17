"""轨迹显示增量算法差分测试:以旧版全量算法为 oracle,随机操作序列逐步比对。

运行: python -m unittest tests.test_trajectory_display -v
"""
import os
import random
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QImage, QColor
    HAS_QT = True
except Exception:
    HAS_QT = False

N_FRAMES = 60


@unittest.skipUnless(HAS_QT, 'PySide6 不可用')
class TrajectoryDisplayDifferentialTest(unittest.TestCase):
    """旧实现: 每次显示 = 移除全部已显示轨迹 + 按帧序重建全量列表并 refresh。
    新实现: 增量增删。两者在任意操作序列下必须显示同一组Item(按id集合比较)。"""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='qt_diff_')
        shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'config.ini'), os.path.join(self.tmp, 'config.ini'))
        from src.settings.settings import Settings
        from src.settings.default_settings import SettingKey
        self.settings = Settings(os.path.join(self.tmp, 'config.ini'))
        self.settings.set_value(SettingKey.show_trajectory, True)
        self.settings.set_value(SettingKey.trajectory_color_with_speed, True)
        self.SettingKey = SettingKey

        from src.view.video_scene import VideoScene
        self.scene = VideoScene(None, self.settings)

        img = QImage(160, 120, QImage.Format.Format_RGB888)
        img.fill(QColor(0, 0, 0))
        self.scene.cache_frame(1, img)
        first = self.scene.frame_cache[1]
        for i in range(1, N_FRAMES + 6):
            self.scene.frame_cache[i] = first

        self._feed_frames(1, N_FRAMES)

    def tearDown(self):
        self.scene.clear_data()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _feed_frames(self, start, end):
        for frame in range(start, end + 1):
            self.scene.data_helper.add_frame_particles(frame, {
                1: (10 + frame * 2, 20 + frame),
                2: (150 - frame, 100 - frame * 2),
            })

    def _oracle(self, frame_index, filter_set):
        """旧算法: DataHelper.get_trajectory_items 的语义(全量重建)。"""
        helper = self.scene.data_helper
        if frame_index not in helper.particle_group:
            return set()
        items = set()
        for f, source in helper.trajectory_items.items():
            if f > frame_index:
                continue
            for pid, item in source.items():
                if filter_set and pid not in filter_set:
                    continue
                items.add(id(item))
        return items

    def _actual(self):
        return {id(item) for item in self.scene.trajectory_items}

    def _filter_now(self):
        return set(self.settings.list_value(self.SettingKey.index_filter))

    def _check(self, label):
        fi = self.scene.current_frame_index
        expected = self._oracle(fi, self._filter_now())
        actual = self._actual()
        self.assertEqual(expected, actual,
                         f'{label}: frame={fi} expected={len(expected)} actual={len(actual)}')
        # 不变量: 已显示帧号不得超出当前帧
        for f in self.scene._shown_trajectory:
            self.assertLessEqual(f, fi, f'{label}: 已显示帧 {f} 超出当前帧 {fi}')

    def _random_ops(self, rng, steps=400):
        """随机执行显示切换/过滤变化/设置刷新/数据重建, 每步后与旧算法比对。"""
        filter_pool = [set(), {1}, {2}, {1, 2}]
        for step in range(steps):
            op = rng.random()
            fi = self.scene.current_frame_index
            if op < 0.45:
                # 随机跳转(含前后来回、越界帧)
                target = rng.randint(0, N_FRAMES + 3)
                self.scene.change_display(target)
                self._check(f'step{step} 跳转')
            elif op < 0.55:
                # 设置变化: 全量 refresh 路径
                self.scene.change_display(rng.randint(0, N_FRAMES + 1), refresh_items=True)
                self._check(f'step{step} refresh')
            elif op < 0.68:
                # 过滤条件变化(等价 scene.set_filter 的效果)
                self.settings.set_value(self.SettingKey.index_filter, rng.choice(filter_pool))
                self.scene.change_display(fi, refresh_items=True)
                self._check(f'step{step} 过滤')
            elif op < 0.88:
                # 数据重建: add_frame_particles 会重建该帧Item(触发脏帧)
                f = rng.randint(1, N_FRAMES)
                x = rng.randint(0, 300)
                self.scene.data_helper.add_frame_particles(f, {1: (x, x), 2: (300 - x, 200 - x)})
                self.scene.change_display(rng.randint(0, N_FRAMES + 1))
                self._check(f'step{step} 重建帧{f}')
            elif op < 0.95:
                # 顺序小步前后拖动(播放/回看热路径)
                delta = rng.choice([-3, -1, -1, 1, 1, 2])
                target = max(0, min(N_FRAMES + 2, fi + delta))
                self.scene.change_display(target)
                self._check(f'step{step} 拖动')
            else:
                # 新数据追加(分析过程中产生的新帧)
                self._feed_frames(N_FRAMES + 1, N_FRAMES + 2)
                self.scene.change_display(N_FRAMES + 2)
                self._check(f'step{step} 追加')

    def test_dense_random_sequence(self):
        rng = random.Random(20261017)
        self._random_ops(rng, steps=300)

    def test_sparse_manual_frames(self):
        """稀疏场景: 仅手动添加的零散帧(分析前的最小数据)。"""
        self.scene.clear_data()
        for f in (5, 17, 40, 41):
            self.scene.data_helper.add_frame_particles(f, {7: (f * 3, f * 2)})
        rng = random.Random(42)
        for step in range(200):
            target = rng.choice([0, 3, 5, 6, 17, 40, 41, 42, 59])
            self.scene.change_display(target, refresh_items=rng.random() < 0.2)
            self._check(f'sparse-step{step}')

    def test_refresh_path_equals_full_rebuild(self):
        """refresh=True 与旧全量行为逐帧等价(含过滤叠加)。"""
        for f in range(0, N_FRAMES + 3, 2):
            self.scene.change_display(f, refresh_items=True)
            self._check(f'refresh {f}')
        self.settings.set_value(self.SettingKey.index_filter, {1})
        for f in range(N_FRAMES + 2, -1, -3):
            self.scene.change_display(f, refresh_items=True)
            self._check(f'refresh+filter {f}')

    def test_clear_and_repopulate(self):
        self.scene.change_display(30)
        self._check('clear前')
        self.scene.clear_data()
        self.assertEqual(self._actual(), set(), 'clear_data 后应无显示轨迹')
        self.assertIsNone(self.scene._shown_max)
        self._feed_frames(1, 20)
        self.scene.change_display(20)
        self._check('clear后重建')


if __name__ == '__main__':
    unittest.main(verbosity=2)