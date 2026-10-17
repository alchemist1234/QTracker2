"""GradientLabel 单元测试: 渐变设置往返、渲染与颜色属性。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QColor, QPixmap
    HAS_QT = True
except Exception:
    HAS_QT = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


@unittest.skipUnless(HAS_QT, 'PySide6 不可用')
class GradientLabelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def _make_colors(self):
        from src.model.models import GradientColor
        return [GradientColor(0.0, QColor(255, 0, 0)),
                GradientColor(0.5, QColor(0, 255, 0)),
                GradientColor(1.0, QColor(0, 0, 255))]

    def test_set_gradient_and_colors_roundtrip(self):
        from src.view.custom_widget import GradientLabel
        label = GradientLabel()
        colors = self._make_colors()
        label.set_gradient(colors)
        got = label.colors
        self.assertEqual(len(got), 3)
        self.assertEqual([c.pos for c in got], [0.0, 0.5, 1.0])
        self.assertEqual(QColor(got[0].color).name(), QColor(255, 0, 0).name())
        # set_gradient 应产出可视 pixmap(原实现在此持有被移除的插值器引用)
        self.assertIsInstance(label.pixmap(), QPixmap)
        self.assertFalse(label.pixmap().isNull())

    def test_set_gradient_accepts_single_color(self):
        from src.view.custom_widget import GradientLabel
        from src.model.models import GradientColor
        label = GradientLabel()
        label.set_gradient(GradientColor(0.2, QColor(1, 2, 3)))
        self.assertEqual(len(label.colors), 1)

    def test_trajectory_item_shares_single_interpolator(self):
        """所有 TrajectoryItem 共享同一个速度颜色插值器(内存优化)。"""
        import shutil
        import tempfile
        from src.settings.settings import Settings
        from src.settings.default_settings import SettingKey
        from src.view.custom_widget import TrajectoryItem
        from src.model.models import GradientColor

        tmp = tempfile.mkdtemp(prefix='qt_si_')
        try:
            shutil.copy(os.path.join(ROOT, 'config.ini'), os.path.join(tmp, 'config.ini'))
            settings = Settings(os.path.join(tmp, 'config.ini'))
            settings.set_value(SettingKey.trajectory_color_with_speed, True)
            a = TrajectoryItem(settings, 1, 0, 0, 10, 10, 1.0)
            b = TrajectoryItem(settings, 2, 10, 10, 20, 20, 1.0)
            self.assertIs(a.create_interpolated(), b.create_interpolated(),
                          '同设置下两条轨迹应共享插值器')
            old = a.create_interpolated()
            # 速度颜色设置变化后应重建共享插值器, 旧引用保持有效
            settings.set_value(SettingKey.trajectory_speed_color,
                               [GradientColor(0.0, QColor(0, 0, 0)),
                                GradientColor(1.0, QColor(255, 255, 255))])
            new = a.create_interpolated()
            self.assertIsNot(new, old, '设置变化后应重建插值器')
            c = TrajectoryItem(settings, 3, 0, 0, 5, 5, 1.0)
            self.assertIs(new, c.create_interpolated(), '新构造Item应复用新插值器')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)