# 测试与检查

## 单元测试(unittest, 可被 `python -m unittest discover -s tests` 发现)

| 文件 | 覆盖 |
| --- | --- |
| `test_trajectory_display.py` | 轨迹显示增量算法差分测试: 以旧版全量算法为 oracle, 随机操作序列(跳转/播放/回看/过滤/设置刷新/数据重建/稀疏帧)逐步比对显示集合 |
| `test_gradient_label.py` | GradientLabel 渐变渲染与 colors 属性往返 |

运行:

```bash
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -t . -v
```

## 脚本式检查(独立运行, 打印式断言; 不带 test_ 前缀以免被 unittest 发现)

| 文件 | 覆盖 |
| --- | --- |
| `check_core_fixes.py` | feature-2.1 修复项逐项验证: common_util、分析器等价性/背压/停止、历史粒子裁剪、进度递增、模块导入 |
| `check_gui_smoke.py` | 离屏 GUI 冒烟: 真实 MainWindow 分析 2000 帧 + 帧切换 + 加载中关窗不卡死 + 二次分析 |
| `check_export_video.py` | 导出端到端: 正常导出、进度/完成/失败信号、格式校验 |
| `bench_trajectory_display.py` | 轨迹显示性能基准(顺序/逆序全帧切换), 传入帧数参数, 如 `python tests/bench_trajectory_display.py 1200` |

运行(无 root 环境需先解压提供 libEGL 的系统包并通过 `LD_LIBRARY_PATH` 指向):

```bash
LD_LIBRARY_PATH=<libEGL所在目录> QT_QPA_PLATFORM=offscreen python tests/check_core_fixes.py
```

`check_gui_smoke.py` 会在 `/tmp/qt_gui_smoke.avi` 生成/复用 2000 帧测试视频;
`check_export_video.py` 依赖同一视频, 建议先跑 GUI 冒烟。