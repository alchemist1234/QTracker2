from PySide6.QtWidgets import QGraphicsSimpleTextItem, QGraphicsTextItem, QGraphicsScene, QGraphicsWidget

total_frames = 500
total_particles = 50
particle_per_frame = 10


class A:
    def __init__(self):
        self.data = {1: {1: (1, 2), 2: (1, 2)}, 2: {1: (11, 22), 2: (11, 22)}}

    def func(self, index):
        particles = {k: {k2: v2 for k2, v2 in v.items() if k2 == index}
                     for k, v in self.data.items()}
        res = {k: v[index] for k, v in particles.items() if len(v) > 0}
        return res


class B:
    def __init__(self, a: A):
        self.a = a

    def func(self, index):
        x = self.a.func(index)
        print(x)


if __name__ == '__main__':
    pass

