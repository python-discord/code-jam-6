from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.core.window import Window

KV = """
FloatLayout
    MyMouse
        id: themouse

<MyMouse>:
    mouse_im_size: mouse_im.size
    auto_bring_to_front: True

    do_rotation:False
    do_scale:False
    do_translation_y:False

    Image
        id: mouse_im
        size: 40, 40 / self.image_ratio
        source: 'hammer.png'
"""

class MyMouse(Scatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.show_cursor = False
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_cursor_leave=self.on_cursor_leave)
        Window.bind(on_cursor_enter=self.on_cursor_enter)

    def on_mouse_pos(self, *args):
        x, y = args[-1]
        self.pos = x, y - self.mouse_im_size[1]

    def on_cursor_leave(self, *args):
        self.opacity = 0

    def on_cursor_enter(self, *args):
        self.opacity = 1


if __name__ == "__main__":
    class MyApp(App):
        def build(self):
            return Builder.load_string(KV)

    MyApp().run()