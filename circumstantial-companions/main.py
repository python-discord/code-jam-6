"""
SMASH ROCK!  FASTER SWING = MORE ROCK SMASHED! This app is a pre-historically accurate
representation of Paleolithic technology!  Re-invent the wheel with this (rock)cutting-edge
simulation! A caveman workout routine guaranteed to give you chiseled slabs fast!
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.garden.navigationdrawer import NavigationDrawer

from cursor import Cursor
from i18n import DEFAULT_LOCALE, SYSTEM_LOCALE, LOCALES, TRANSLATIONS
from mixins import RepeatingBackground
from stone import Chisel, CHISEL_RADIUS_RANGE, CHISEL_POWER_RANGE


class ChiselRadiusSlider(Slider):
    def __init__(self, chisel):
        self.chisel = chisel
        super().__init__(orientation="vertical",
                         range=CHISEL_RADIUS_RANGE,
                         value=chisel.chisel_radius,
                         value_track=True,
                         value_track_color=[1, 0, 1, 1])

    def on_value(self, instance, value):
        self.chisel.set_radius(value)


class ChiselPowerSlider(Slider):
    def __init__(self, chisel):
        self.chisel = chisel
        super().__init__(orientation="vertical",
                         range=CHISEL_POWER_RANGE,
                         value=chisel.chisel_power,
                         value_track=True,
                         value_track_color=[1, 0, 1, 1])

    def on_value(self, instance, value):
        self.chisel.set_power(value)


class OptionsPanel(RepeatingBackground, BoxLayout):
    def __init__(self, chisel):
        self.chisel = chisel
        self.dropdown = None
        super().__init__(orientation="vertical", spacing=10, padding=5)
        self.setup_background("assets/img/options_background.png")

    def build(self, locale=SYSTEM_LOCALE):
        self.clear_widgets()
        if locale in LOCALES:
            TRANSLATIONS[locale].install()
        else:
            TRANSLATIONS[DEFAULT_LOCALE].install()

        # Language selection
        self.dropdown = DropDown()
        for locale_code, locale_name in LOCALES.items():
            btn = Button(text=locale_name, size_hint_y=None, height=20)

            def _make_select_function(locale_code):
                return lambda btn: self.dropdown.select(locale_code)

            btn.bind(on_release=_make_select_function(locale_code))
            self.dropdown.add_widget(btn)
        dropdown_btn = Button(text=_("Select language"), size_hint=(1, 0.1))
        dropdown_btn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, locale: self.build(locale))

        reset_btn = Button(text=_("Reset"), size_hint=(1, 0.1))
        reset_btn.bind(on_release=lambda btn: self.chisel.reset())

        slider_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.7))
        slider_layout.add_widget(ChiselRadiusSlider(self.chisel))
        slider_layout.add_widget(ChiselPowerSlider(self.chisel))

        self.add_widget(Label(text=_("Options"), size_hint=(1, 0.1)))
        self.add_widget(dropdown_btn)
        self.add_widget(reset_btn)
        self.add_widget(slider_layout)


class ChiselApp(App):
    def __init__(self):
        super().__init__()

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

        root.add_widget(navdrawer)
        Window.add_widget(Cursor(), "after")
        return root


if __name__ == "__main__":
    ChiselApp().run()
