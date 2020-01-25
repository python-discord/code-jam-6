"""
SMASH ROCK!  FASTER SWING = MORE ROCK SMASHED! This app is a pre-historically accurate
representation of Paleolithic technology!  Re-invent the wheel with this (rock)cutting-edge
simulation! A caveman workout routine guaranteed to give you chiseled slabs fast!
"""
import contextvars
import math
from itertools import cycle

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.garden.navigationdrawer import NavigationDrawer

from cursor import Cursor
from i18n import DEFAULT_LOCALE, SYSTEM_LOCALE, LOCALES, TRANSLATIONS
from mixins import RepeatingBackground, SignBorder
from stone import Chisel

FONT = contextvars.ContextVar("font")
OPTIONS_BACKGROUND = "assets/img/options_background.png"
CAVEMAN = tuple(f"assets/img/caveman{i}.png" for i in range(4))
BUTTON_NORMAL = "assets/img/button_normal.png"
BUTTON_HOVER = "assets/img/button_hover.png"
BUTTON_PRESSED = "assets/img/button_pressed.png"

class Button(SignBorder, KivyButton):
    def __init__(self, text, **kwargs):
        super().__init__(text=text, font_name=FONT.get(), **kwargs)
        self.setup_border()
        Window.bind(mouse_pos=self._on_mouse_pos)
        self.background_normal = BUTTON_NORMAL
        self.background_down = BUTTON_PRESSED

    def _on_mouse_pos(self, window, pos):
        if self.collide_point(*self.to_widget(*pos)):
            self.background_normal = BUTTON_HOVER
        else:
            self.background_normal = BUTTON_NORMAL


class SelectLanguagePopup(SignBorder, Popup):
    choice = StringProperty()

    def __init__(self):
        layout = BoxLayout(orientation="vertical", spacing=dp(34), padding=(dp(20), dp(15)))
        for locale_code, locale_info in LOCALES.items():
            btn = Button(locale_info["name"], font_size=sp(16))

            def _make_select_function(locale_code):
                def _select(btn):
                    self.dismiss()
                    self.choice = locale_code

                return _select

            btn.bind(on_release=_make_select_function(locale_code))
            layout.add_widget(btn)

        super().__init__(title=_("Select language"),
                         title_font=FONT.get(),
                         title_size=sp(20),
                         title_align="center",
                         content=layout,
                         separator_color=(0, 0, 0, 0),
                         size_hint=(0.5, 0.8))
        self.setup_border()


class OptionsPanel(RepeatingBackground, BoxLayout):
    def __init__(self, chisel):
        self.chisel = chisel
        self.popup = None
        super().__init__(orientation="vertical",
                         spacing=dp(34),
                         padding=(dp(20), dp(15)),
                         opacity=0)  # opacity is set when side panel is opened
        self.setup_background(OPTIONS_BACKGROUND)

    def build(self, locale=SYSTEM_LOCALE):
        self.clear_widgets()
        if locale in LOCALES:
            TRANSLATIONS[locale].install()
        else:
            locale = DEFAULT_LOCALE
            TRANSLATIONS[DEFAULT_LOCALE].install()

        FONT.set(LOCALES[locale]["font"])

        # Title
        title = Label(text=_("Options"),
                      font_name=FONT.get(),
                      font_size=sp(30),
                      size_hint=(1, 0.05))

        # Language selection
        self.popup = SelectLanguagePopup()
        popup_btn = Button(_("Select language"),
                           font_size=sp(18),
                           size_hint=(1, None),
                           height=dp(42))
        popup_btn.bind(on_release=self.popup.open)
        self.popup.bind(choice=lambda instance, choice: self.build(choice))

        # Reset
        reset_btn = Button(_("Reset"),
                           font_size=sp(18),
                           size_hint=(1, None),
                           height=dp(42))
        reset_btn.bind(on_release=lambda btn: self.chisel.reset())

        # Source code
        src_btn = Button(_("Source code"),
                         font_size=sp(18),
                         size_hint=(1, None),
                         height=dp(42))

        # Animation - Normal loading of an animation won't apply desired mag_filter to each
        # individual texture, so we load each frame and cycle through the textures 'by-hand'.
        images = []
        for source in CAVEMAN:
            image = Image(source=source, size_hint=(1, 1), allow_stretch=True)
            image.texture.mag_filter = 'nearest'
            images.append(image)
        images = cycle(images)

        animation = Image(source=CAVEMAN[0], size_hint=(1, 1), allow_stretch=True)
        animation.texture.mag_filter = 'nearest'

        def next_texture(*args):
            animation.texture = next(images).texture
        Clock.schedule_interval(next_texture, .2)

        self.add_widget(title)
        self.add_widget(popup_btn)
        self.add_widget(reset_btn)
        self.add_widget(src_btn)
        self.add_widget(animation)

    def update_background(self, instance, value):
        # Overriden to snap to the right position.
        self.bg_rect.texture.uvsize = self._get_uvsize()
        self.bg_rect.texture = self.bg_rect.texture  # Required to trigger update.
        bg_width, bg_height = self._get_background_size()
        self.bg_rect.pos = (self.right - bg_width, self.y)
        self.bg_rect.size = (bg_width, bg_height)


class ChiselApp(App):
    def build(self):
        root = FloatLayout()
        navdrawer = NavigationDrawer()
        navdrawer.toggle_state()
        navdrawer.anim_type = "slide_above_anim"

        self.chisel = chisel = Chisel()
        self.chisel_on_touch_down = chisel.on_touch_down
        self.chisel_on_touch_move = chisel.on_touch_move

        options_panel = OptionsPanel(chisel)
        navdrawer.add_widget(options_panel)

        rel_layout = RelativeLayout()
        rel_layout.add_widget(chisel)  # To push it when side panel is opened.
        navdrawer.add_widget(rel_layout)
        options_panel.build()
        navdrawer.bind(_anim_progress=self._set_side_panel_opacity)
        navdrawer.bind(_anim_progress=self.disable_chisel)

        root.add_widget(navdrawer)
        Window.add_widget(Cursor(), "after")
        return root

    def _set_side_panel_opacity(self, instance, value):
        instance.side_panel.opacity = math.ceil(instance._anim_progress)

    def disable_chisel(self, instance, value):
        if instance._anim_progress > 0:
            self.chisel.on_touch_down = self.chisel.on_touch_move = lambda *args: None
        else:
            self.chisel.on_touch_down = self.chisel_on_touch_down
            self.chisel.on_touch_move = self.chisel_on_touch_move


if __name__ == "__main__":
    ChiselApp().run()
