import time, sys
from PySide6.QtCore import *
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, \
    QVBoxLayout


class Task(QObject):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.jobs = []
        self.running = False

    def run(self):
        while True:
            if not self.running:
                break
            print(f'running {self.id}')
            work = False
            if len(self.jobs) > 0:
                work = True
                job = self.jobs.pop()
                time.sleep(1)
                if self.running:
                    print(f'{self.id} job: {job}')
                    self.id += 1
                else:
                    break
            if not work:
                time.sleep(2)

    def start(self):
        self.running = True
        self.run()

    @Slot(int)
    def add_job(self, job):
        self.jobs.append(job)

    @Slot()
    def stop(self):
        self.running = False
        self.id = 1
        self.jobs.clear()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 160)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.btn_start = QPushButton('start')
        self.layout.addWidget(self.btn_start)
        self.btn_click = QPushButton('click')
        self.layout.addWidget(self.btn_click)
        self.btn_stop = QPushButton('stop')
        self.layout.addWidget(self.btn_stop)

        self.thread = QThread()
        self.task = Task()
        self.task.moveToThread(self.thread)
        self.thread.started.connect(self.task.start)
        self.thread.finished.connect(self.task.stop)
        # self.thread.started.connect(self.task.run)
        # self.thread.started.connect(lambda: self.task.start_job)

        self.btn_start.clicked.connect(self.thread.start)
        self.btn_click.clicked.connect(self.add_job)
        self.btn_stop.clicked.connect(self.stop)

    def add_job(self):
        self.task.add_job(1)

    def stop(self):
        self.task.stop()

    def closeEvent(self, event) -> None:
        self.stop()
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
