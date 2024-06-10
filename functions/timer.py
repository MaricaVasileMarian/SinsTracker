import time
import threading

class Timer:
    def __init__(self, callback):
        self._start_time = 0
        self._elapsed_time = 0
        self._running = False
        self._paused = False
        self.update_callback = callback

    def start(self):
        if not self._running and not self._paused:
            self._running = True
            self._start_time = time.time()
            threading.Thread(target=self._run).start()

    def pause_continue(self):
        if self._running:
            self._running = False
            self._paused = True
            self._elapsed_time += time.time() - self._start_time
        elif self._paused:
            self._running = True
            self._paused = False
            self._start_time = time.time()
            threading.Thread(target=self._run).start()

    def stop(self):
        if self._running or self._paused:
            self._running = False
            self._paused = False
            self._elapsed_time += time.time() - self._start_time
        elapsed = self._elapsed_time
        self._elapsed_time = 0
        self.update_callback("00:00:00")
        return elapsed

    def _run(self):
        while self._running:
            elapsed = time.time() - self._start_time + self._elapsed_time
            self.update_callback(self._format_time(elapsed))
            time.sleep(0.1)

    def _format_time(self, elapsed):
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
