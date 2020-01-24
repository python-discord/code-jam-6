"""
SMASH ROCK!  FASTER SWING = MORE ROCK SMASHED! This app is a pre-historically accurate
representation of Paleolithic technology!  Re-invent the wheel with this (rock)cutting-edge
simulation! A caveman workout routine guaranteed to give you chiseled slabs fast!
"""
import contextvars
import math

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import BorderImage, Color
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.garden.navigationdrawer import NavigationDrawer

from cursor import Cursor
from i18n import DEFAULT_LOCALE, SYSTEM_LOCALE, LOCALES, TRANSLATIONS
from mixins import RepeatingBackground
from stone import Chisel, CHISEL_RADIUS_RANGE, CHISEL_POWER_RANGE

font = contextvars.ContextVar("font")

OPTIONS_BACKGROUND = "assets/img/options_background.png"
BORDER_IMAGE = "assets/img/sign-border-blank.png"
HAMMER_ICON = "assets/img/cursor/hammer_up_pixelized.png"

class Button(KivyButton):
    def __init__(self, text, **kwargs):
        super().__init__(
            text=text, font_name=font.get(), border=(0, 0, 0, 0), **kwargs,
        )
        self.n = 32
        with self.canvas.before:
            self.border_img = BorderImage(
                source=BORDER_IMAGE,
                size=(self.width + self.n, self.height + self.n),
                pos=(self.x - self.n / 2, self.y - self.n / 2),
                autoscale="both",
            )

        self.bind(size=self.resize_and_reposition, pos=self.resize_and_reposition)

    def resize_and_reposition(self, instance, value):
        self.border_img.size = (self.width + self.n, self.height + self.n)
        self.border_img.pos = (self.x - self.n / 2, self.y - self.n / 2)


class ChiselRadiusSlider(Slider):
    def __init__(self, chisel, **kwargs):
        self.chisel = chisel
        super().__init__(
            orientation="vertical",
            range=CHISEL_RADIUS_RANGE,
            value=chisel.chisel_radius,
            value_track=True,
            value_track_color=[1, 0, 1, 1],
            **kwargs,
        )

    def on_value(self, instance, value):
        self.chisel.set_radius(value)


class ChiselPowerSlider(Slider):
    def __init__(self, chisel, **kwargs):
        self.chisel = chisel
        super().__init__(
            orientation="vertical",
            range=CHISEL_POWER_RANGE,
            value=chisel.chisel_power,
            value_track=True,
            value_track_color=[1, 0, 1, 1],
            **kwargs,
        )

    def on_value(self, instance, value):
        self.chisel.set_power(value)


class OptionsPanel(RepeatingBackground, BoxLayout):
    def __init__(self, chisel):
        self.chisel = chisel
        self.dropdown = None
        super().__init__(
            orientation="vertical",
            spacing=10,
            padding=5,
            opacity=0,  # opacity is set when side panel is opened
        )
        self.setup_background(OPTIONS_BACKGROUND)

    def build(self, locale=SYSTEM_LOCALE):
        self.clear_widgets()
        if locale in LOCALES:
            TRANSLATIONS[locale].install()
        else:
            locale = DEFAULT_LOCALE
            TRANSLATIONS[DEFAULT_LOCALE].install()

        font.set(LOCALES[locale]["font"])

        # Title
        title = Label(
            text=_("Options"),
            font_name=font.get(),
            font_size=sp(40),
            size_hint=(1, 0.1),
        )

        # Language selection
        self.dropdown = DropDown()
        for locale_code, locale_info in LOCALES.items():
            btn = Button(locale_info["name"], size_hint_y=None, height=30)

            def _make_select_function(locale_code):
                return lambda btn: self.dropdown.select(locale_code)

            btn.bind(on_release=_make_select_function(locale_code))
            self.dropdown.add_widget(btn)
        dropdown_btn = Button(
            _("Select language"), font_size=sp(30), size_hint=(1, 0.1), width=100
        )
        dropdown_btn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, locale: self.build(locale))

        # Reset
        reset_btn = Button(_("Reset"), font_size=sp(30), size_hint=(1, 0.1), width=100)
        reset_btn.bind(on_release=lambda btn: self.chisel.reset())

        # Sliders
        slider_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.7))
        slider_layout.add_widget(ChiselRadiusSlider(self.chisel, size_hint=(0.5, 0.9)))
        slider_layout.add_widget(ChiselPowerSlider(self.chisel, size_hint=(0.5, 0.9)))
        slider_layout.add_widget(
            Image(source=HAMMER_ICON, size_hint=(0.5, 0.1))
        )
        slider_layout.add_widget(
            Image(source=HAMMER_ICON, size_hint=(0.5, 0.1))
        )

        self.add_widget(title)
        self.add_widget(dropdown_btn)
        self.add_widget(reset_btn)
        self.add_widget(slider_layout)

    def update_background(self, instance, value):
        # Overriden to snap to the right position
        self.bg_rect.texture.uvsize = self._get_uvsize()
        self.bg_rect.texture = self.bg_rect.texture  # required to trigger update
        bg_width, bg_height = self._get_background_size()
        self.bg_rect.pos = (self.right - bg_width, self.y)
        self.bg_rect.size = (bg_width, bg_height)


class ChiselApp(App):
    def build(self):
        root = FloatLayout()
        navdrawer = NavigationDrawer()
        navdrawer.anim_type = "slide_above_anim"
        chisel = Chisel()
        options_panel = OptionsPanel(chisel)

        navdrawer.add_widget(options_panel)
        rel_layout = RelativeLayout()
        rel_layout.add_widget(chisel)  # to push it when side panel is opened
        navdrawer.add_widget(rel_layout)
        options_panel.build()
        navdrawer.bind(_anim_progress=self._set_side_panel_opacity)

        root.add_widget(navdrawer)
        Window.add_widget(Cursor(), "after")
        return root

    def _set_side_panel_opacity(self, instance, value):
        instance.side_panel.opacity = math.ceil(instance._anim_progress)


if __name__ == "__main__":
    ChiselApp().run()
