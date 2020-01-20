from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scatter import Scatter
from kivy.core.window import Window

Window.show_cursor = False

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
        size: 100, 100 / self.image_ratio
        source: 'pickaxe.jpg'

"""

class MyMouse(Scatter):
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_cursor_leave=self.on_cursor_leave)
        Window.bind(on_cursor_enter=self.on_cursor_enter)
        super(MyMouse, self).__init__(**kwargs)


    def on_touch_down(self, *touch):
        return

    def on_mouse_pos(self, *args):
        x,y = args[1]
        self.pos = [x,y-self.mouse_im_size[1]]

    def on_cursor_leave(self, *args):
        App.get_running_app().root.ids.themouse.opacity = 0

    def on_cursor_enter(self, *args):
        App.get_running_app().root.ids.themouse.opacity = 1


class MyApp(App):
    def build(self):
        self.root = Builder.load_string(KV)

MyApp().run()