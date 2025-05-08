import time


class StopWatch:
    def __init__(self):
        """
        秒表工具
        """
        self._start_time = None
        self._elapsed_time = 0
        self._tasks = dict()
        self._current_task = None
        self._current_start_time = None

    def start(self, task_name):
        if self._start_time is not None:
            raise RuntimeError("StopWatch already running")
        self._start_time = time.perf_counter()
        self._current_task = task_name

    def stop(self):
        if self._start_time is None:
            raise RuntimeError("StopWatch not running")
        self._elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        self._tasks[self._current_task] = self._elapsed_time if self._current_task not in self._tasks else self._tasks[self._current_task] + self._elapsed_time
        self._elapsed_time = 0

    def reset(self):
        self._start_time = None
        self._elapsed_time = 0
        self._tasks.clear()
        self._current_task = None
        self._current_start_time = None

    def elapsed(self):
        if self._start_time is not None:
            return self._elapsed_time + (time.perf_counter() - self._start_time)
        return self._elapsed_time

    def print_result(self):
        total = 0
        for task_name, elapsed_time in self._tasks.items():
            total += elapsed_time
            print(f"{task_name}: {elapsed_time:.6f}")
        print(f'total: {total:.6f}\n')
