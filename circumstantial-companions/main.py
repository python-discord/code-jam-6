'''
Modified 3D Rotating Monkey Head example -- rotation can be controlled with mouse.
'''
import gettext
import json
import locale
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown

# Internationalization constants

DEFAULT_LOCALE = "en_US"
SYSTEM_LOCALE = locale.getdefaultlocale()[0]

with open("locales.json", encoding="utf-8") as file:
    LOCALES = json.load(file)

TRANSLATIONS = {
    locale: gettext.translation("messages", "locales", [locale])
    for locale in LOCALES
    if locale != DEFAULT_LOCALE
}
TRANSLATIONS[DEFAULT_LOCALE] = gettext.NullTranslations()

# Renderer constants

ROTATE_SPEED = 500


class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = 'simple.glsl'
        self.scene = ObjFile('monkey.obj') # We'll want to generate meshes on-the-fly instead.
                                           # I assume a triangulated random cloud of points
                                           # will be stony enough. We should be able to remove
                                           # all dependency on objloader though. Then again, if
                                           # we add save/load methods we may want objloader --
                                           # could use a bit of rewrite in that case.
        super().__init__(**kwargs)

        with self.canvas:
            self.cb = Callback(lambda *args: glEnable(GL_DEPTH_TEST))
            self.setup_scene()
            self.cb = Callback(lambda *args: glDisable(GL_DEPTH_TEST))

        self.indices = self.mesh.indices.copy()
        self.fewer = self.indices[3:]

        def set_aspect():
            asp = self.width / self.height
            proj = Matrix().view_clip(-asp, asp, -1, 1, .5, 100, 1)
            self.canvas['projection_mat'] = proj
        Clock.schedule_once(lambda dt: set_aspect())

    def on_touch_move(self, touch):
        """
        We should have two different drags --- one to rotate the stone and one to chip the
        stone.  Probably 'right' and 'left' click differentiated.
        """
        if touch.button == 'right':
            self.rotate(touch.dsx)
        else:
            self.chip_away(touch)

    def chip_away(self, touch):
        """
        Need collision detection with mesh and a method to remove points from mesh.  I think
        this function will be the most difficult to flesh out.
        """

        if self.mesh.indices == self.indices:
            print(touch.spos)
            x, y ,z = self.mesh.indices[:3]
            # with objloader sorted i can find the actual face coordinates and compare them
            # to touch.spos --- hopefully this leads to collision detection
            print(*(self.mesh.vertices[i * 8:i * 8 + 3] for i in (x, y, z)))
            self.mesh.indices = self.fewer
        else:
            self.mesh.indices = self.indices
        #self.mesh.indices = self.mesh.indices[3:] # This makes a pretty creepy monkey.

    def rotate(self, dx):
        self.rotx.angle += dx * ROTATE_SPEED

    def setup_scene(self):
        Translate(0, 0, -2) # Maybe zoom in more?
        self.rotx = Rotate(0, 0, 1, 0)
        m, *_ = self.scene.objects.values()
        UpdateNormalMatrix()
        self.mesh = Mesh(vertices=m.vertices,
                         indices=m.indices,
                         fmt=m.vertex_format,
                         mode='triangles')

    def reset_model(self):
        print("reset_model")

    def reset_view(self):
        print("reset_view")
        self.rotx.set(0, 0, 1, 0)

    def reset_all(self):
        # Do we reset_model and reset_view sequentially,
        # or do we "delete" this widget and immediately replace with a new one?
        # How does the memory work?
        print("reset_all")


class ResetButton(Button):

    def __init__(self, renderer, reset_type, **kwargs):
        self.renderer = renderer
        self.reset_type = reset_type
        super().__init__(**kwargs)
    
    def on_release(self):
        method = getattr(self.renderer, f"reset_{self.reset_type}")
        method()


class ButtonPanel(BoxLayout):
    def __init__(self, renderer, **kwargs):
        super().__init__(**kwargs)
        self.renderer = renderer
        self.dropdown = None
        self.button_widgets = []

    def build(self, locale=SYSTEM_LOCALE):
        print(locale)
        for widget in self.button_widgets:
            self.remove_widget(widget)
        if locale in LOCALES:
            TRANSLATIONS[locale].install()
        else:
            TRANSLATIONS[DEFAULT_LOCALE].install()

        self.dropdown = DropDown()
        for locale_code, locale_name in LOCALES.items():
            btn = Button(text=locale_name, size_hint_y=None, height=20)
            def _make_select_function(locale_code):
                return lambda btn: self.dropdown.select(locale_code)
            btn.bind(on_release=_make_select_function(locale_code))
            self.dropdown.add_widget(btn)
            print(locale_code, locale_name)
        dropdown_btn = Button(text=_("Select language"))
        dropdown_btn.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance, locale: self.build(locale))

        self.button_widgets = [
            dropdown_btn,
            ResetButton(self.renderer, "model", text=_("Reset model")),
            ResetButton(self.renderer, "view", text=_("Reset view")),
            ResetButton(self.renderer, "all", text=_("Reset all"))
        ]
        for widget in self.button_widgets:
            self.add_widget(widget)


class RendererApp(App):
    def __init__(self):
        super().__init__()

    def build(self):
        renderer = Renderer(size_hint=(1, 0.9))
        main_layout = BoxLayout(orientation="vertical", spacing=10)
        btn_panel = ButtonPanel(renderer, orientation="horizontal", spacing=10, size_hint=(1, 0.1))

        main_layout.add_widget(renderer)
        main_layout.add_widget(btn_panel)

        btn_panel.build()

        return main_layout

if __name__ == "__main__":
    # Convenience function while developing,
    # Create .mo file from .po files.
    os.system("pybabel compile -d locales")

    RendererApp().run()