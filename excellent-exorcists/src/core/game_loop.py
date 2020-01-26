from kivy.clock import Clock


class GameLoop:
    def __init__(self):
        self.loop = None
        self.callback_ = lambda _: _

    def set_callback(self, callback):
        self.callback_ = callback

    def callback(self, delta):
        self.callback_(delta)

    def start(self, fps: int):
        self.loop = Clock.schedule_interval(self.callback, 1.0 / float(fps))

    def stop(self):
        if self.loop is not None:
            self.loop.cancel()
