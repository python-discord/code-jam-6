from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class Screen(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        super().__init__(**kwargs)

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

    def set_projection_matrix(self, matrices):
        self.canvas['projection_mat'] = matrices[0]
        self.canvas['modelview_mat'] = matrices[1]

    def render_screen(self, delta):
        """Wrapper method for render, should not be overrided"""
        with self.canvas:
            self.render(delta)
