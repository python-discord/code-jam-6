from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class Screen(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        self.disable = False
        self.engine = None

        super().__init__(**kwargs)

    def set_engine(self, engine):
        self.engine = engine

    def is_key_just_pressed(self, code: int) -> bool:
        return code in self.engine.just_pressed_keys

    def is_key_pressed(self, code: int) -> bool:
        return code in self.engine.pressed_keys

    def get_mouse_position(self):
        return self.engine.mouse_position

    def set_disabled(self, value: bool):
        self.disable = value

    def update(self, delta):
        """Override this method for updating state"""

    def on_resize(self, width: int, height: int):
        """Called on window resize"""

    def clear(self, canvas: RenderContext):
        canvas.clear()
