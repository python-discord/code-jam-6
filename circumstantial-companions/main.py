"""
SMASH ROCK!  FASTER SWING = MORE ROCK SMASHED! This app is a pre-historically accurate
representation of Paleolithic technology!  Re-invent the wheel with this (rock)cutting-edge
simulation! A caveman workout routine guaranteed to give you chiseled slabs fast!
"""
import contextvars
import math
import os
from itertools import cycle

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
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
FILE_EXTENSION = ".chisel-project"


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


class ImportPopup(SignBorder, Popup):
    def __init__(self, chisel):
        self.chisel = chisel
        layout = BoxLayout(orientation="vertical", spacing=dp(34), padding=(dp(20), dp(15)))
        self.file_chooser = FileChooserListView(path=".", filters=[self._filter_file], size_hint=(1, 0.85))
        self.btn = Button(_("Open..."), disabled=True, font_size=sp(16), size_hint=(1, 0.15))

        self.file_chooser.bind(path=self._change_title, selection=self._change_btn_name)
        self.btn.bind(on_release=self._select_file)

        layout.add_widget(self.file_chooser)
        layout.add_widget(self.btn)

        super().__init__(title="",
                         title_font=FONT.get(),
                         title_size=sp(20),
                         title_align="center",
                         content=layout,
                         separator_color=(0, 0, 0, 0),
                         size_hint=(0.7, 0.9))
        self._change_title()
        self.setup_border()

    @staticmethod
    def _filter_file(folder, filename):
        return filename.endswith(FILE_EXTENSION)

    def _change_title(self, *args):
        path = self.file_chooser.path
        if path == ".":
            path = os.getcwd()
        self.title = _("Import from {path}").format(path=path)

    def _change_btn_name(self, *args):
        selection = self.file_chooser.selection
        if selection:
            self.btn.text = _('Open "{filename}"').format(filename=os.path.basename(selection[0]))
            self.btn.disabled = False
        else:
            self.btn.text = _("Please select a file.")
            self.btn.disabled = True

    def _select_file(self, *args):
        selection = self.file_chooser.selection
        if selection:
            self.dismiss()
            self.chisel.load(selection[0])

    def on_dismiss(self, *args):
        self.file_chooser.cancel()


class SaveAsPopup(SignBorder, Popup):
    def __init__(self, chisel):
        self.chisel = chisel
        layout = BoxLayout(orientation="vertical", spacing=dp(34), padding=(dp(20), dp(15)))
        self.file_chooser = FileChooserListView(path=".", filters=[self._filter_file], size_hint=(1, 0.75))
        self.text_input = TextInput(text="Untitled" + FILE_EXTENSION, multiline=False, font_name=FONT.get(), font_size=sp(16), size_hint=(1, 0.1))
        self.btn = Button("", font_size=sp(16), size_hint=(1, 0.15))
        self._change_btn_name()

        self.file_chooser.bind(path=self._change_title, selection=self._set_text)
        self.text_input.bind(text=self._change_btn_name, on_text_validate=self._save_file)
        self.btn.bind(on_release=self._save_file)

        layout.add_widget(self.file_chooser)
        layout.add_widget(self.text_input)
        layout.add_widget(self.btn)

        super().__init__(title="",
                         title_font=FONT.get(),
                         title_size=sp(20),
                         title_align="center",
                         content=layout,
                         separator_color=(0, 0, 0, 0),
                         size_hint=(0.7, 0.9))
        self._change_title()
        self.setup_border()

    @staticmethod
    def _filter_file(folder, filename):
        return filename.endswith(FILE_EXTENSION)

    @staticmethod
    def _resolve_filename(string):
        if string.endswith(FILE_EXTENSION):
            return string
        return string + FILE_EXTENSION

    def _change_title(self, *args):
        path = self.file_chooser.path
        if path == ".":
            path = os.getcwd()
        self.title = _("Save to {path}").format(path=path)

    def _set_text(self, *args):
        selection = self.file_chooser.selection
        if selection:
            self.text_input.text = os.path.basename(selection[0])

    def _change_btn_name(self, *args):
        filename = self._resolve_filename(self.text_input.text)
        self.btn.text = _('Save as "{filename}"').format(filename=filename)

    def _save_file(self, *args):
        filename = self._resolve_filename(self.text_input.text)
        self.chisel.save(os.path.join(self.file_chooser.path, filename))
        self.dismiss()

    def on_dismiss(self, *args):
        self.file_chooser.cancel()


class OptionsPanel(RepeatingBackground, BoxLayout):
    def __init__(self, chisel):
        self.chisel = chisel
        super().__init__(orientation="vertical",
                         spacing=dp(32),
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
                      size_hint=(1, 0.05),
                      outline_color=(0, 0, 0),
                      outline_width=2)

        # Language selection
        language_btn = Button(_("Select language"),
                           font_size=sp(18),
                           size_hint=(1, None),
                           height=dp(42))
        language_btn.bind(on_release=self.open_language_popup)

        # Import
        import_btn = Button(_("Import..."),
                         font_size=sp(18),
                         size_hint=(1, None),
                         height=dp(42))
        import_btn.bind(on_release=lambda btn: ImportPopup(self.chisel).open(btn))

        # Save as
        save_as_btn = Button(_("Save as..."),
                         font_size=sp(18),
                         size_hint=(1, None),
                         height=dp(42))
        save_as_btn.bind(on_release=lambda btn: SaveAsPopup(self.chisel).open(btn))

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

        widgets = [title,
                   language_btn,
                   import_btn,
                   save_as_btn,
                   reset_btn,
                   src_btn,
                   animation]

        for widget in widgets:
            self.add_widget(widget)

    def update_background(self, instance, value):
        # Overriden to snap to the right position.
        self.bg_rect.texture.uvsize = self._get_uvsize()
        self.bg_rect.texture = self.bg_rect.texture  # Required to trigger update.
        bg_width, bg_height = self._get_background_size()
        self.bg_rect.pos = (self.right - bg_width, self.y)
        self.bg_rect.size = (bg_width, bg_height)

    def open_language_popup(self, btn):
        language_popup = SelectLanguagePopup()
        language_popup.bind(choice=lambda instance, choice: self.build(choice))
        language_popup.open(btn)


class ChiselApp(App):
    def build(self):
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

        Window.add_widget(Cursor(), "after")
        return navdrawer

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
