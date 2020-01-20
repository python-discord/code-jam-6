from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class Screen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.render_context = RenderContext()

    def render(self, delta):
        """Override this method and render graphics"""

    def update(self, delta):
        """Override this method for updating state"""

    def on_create(self):
        """Called when initialized from screen manager"""

    def on_destroy(self):
        """Called when removed from screen manager"""

    def on_open(self):
        """Called when the screen is opened"""

    def on_close(self):
        """Called when the screen is closed"""

    def on_resize(self, width: int, height: int):
        """Called on window resize"""

    def clear(self):
        self.canvas.clear()

    def render_screen(self, delta):
        """Wrapper method for render, should not be overrided"""
        with self.canvas:
            self.render(delta)
