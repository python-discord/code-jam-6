from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class CursorImage(Image):
    def __init__(self):
        super().__init__(source="chisel.png")
        self.size = (40, 40 / self.image_ratio)


class Cursor(Widget):
    def __init__(self):
        super().__init__(size=(0, 0))
        self.cursor_img = CursorImage()
        self.add_widget(self.cursor_img)
        Window.show_cursor = False
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_cursor_leave=self.on_cursor_leave)
        Window.bind(on_cursor_enter=self.on_cursor_enter)

    def on_mouse_pos(self, *args):
        x, y = args[-1]
        self.cursor_img.pos = x, y - self.cursor_img.size[1]

    def on_cursor_leave(self, *args):
        self.opacity = 0

    def on_cursor_enter(self, *args):
        self.opacity = 1
