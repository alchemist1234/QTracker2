from typing import Dict, Tuple, List
import time
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import QRandomGenerator
from PySide6.QtWidgets import QGraphicsSimpleTextItem, QGraphicsScene, QWidget, QGraphicsItem, QGraphicsPixmapItem
from PySide6.QtCore import Qt
from src.model.models import ParticlePositions, DataHelper, Settings, MarkItem
import pandas as pd

total_frames = 500
total_particles = 200
particle_per_frame = 50


def generate_all_particles() -> ParticlePositions:
    pos = ParticlePositions()
    for i in range(total_frames):
        pos.add_frame_particles(i, generate_particles(total_particles, particle_per_frame))
    return pos


def generate_particles(total: int, per: int) -> Dict[int, Tuple[int, int]]:
    c = QRandomGenerator.global_().bounded(per) + int(per * 0.5)
    pos = {}
    for i in range(c):
        index = QRandomGenerator.global_().bounded(total)
        x = QRandomGenerator.global_().bounded(500)
        y = QRandomGenerator.global_().bounded(500)
        pos[index] = (x, y)
    return pos


if __name__ == '__main__':
    pos = generate_all_particles()
    settings = Settings('D:\\workspaces\\projects\\study\\python\\QTracker2\\config.ini')
    graphic_items = DataHelper(pos, settings)

    t1 = time.time()
    for i in range(total_frames):
        graphic_items.__update_particle_items(i)
        graphic_items.__update_trajectory_items(i)
    t2 = time.time()
    print(t2 - t1)
    print('finish')
    df = pd.read_csv('')
    for _, row in df.iterrows():
        data = row.tolist()

