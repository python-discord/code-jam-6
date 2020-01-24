from kivy import Config

Config.set('graphics', 'minimum_width', '1300')
Config.set('graphics', 'minimum_height', '650')
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '650')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen
)

from .footer.footer import Footer
from .terminal.terminal import Terminal
from .manager.browser import FileBrowser
from .editor.editor import TextEditor

Builder.load_file('./ancient_tech/main.kv')


class Main(Screen, FloatLayout):
    pass


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.add_widget(TextEditor(name='text_editor'))
        self.add_widget(Main(name='browser'))

        super().__init__(**kwargs)
        self.config_keyboard()

    def on_touch_down(self, touch):
        self.isTextInput = False

        def filter(widget):
            for child in widget.children:
                filter(child)
            if isinstance(widget, TextInput) and widget.collide_point(*touch.pos):
                self.isTextInput = True
                widget.on_touch_down(touch)

        filter(self)

        if not self.isTextInput and self._keyboard is None:
            self.config_keyboard()

    def config_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('INFO: The key', keycode, 'has been pressed')

        return True


class AncientTechApp(App):

    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
