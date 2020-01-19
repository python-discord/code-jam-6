from pathlib import Path
from datetime import datetime

from kivy import Config

Config.set('graphics', 'minimum_width', '1250')
Config.set('graphics', 'minimum_height', '500')
Config.set('graphics', 'width', '1250')
Config.set('graphics', 'height', '500')

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup

from kivy.properties import (
    StringProperty,
)

from .utils.utils import bytes_conversion


class Main(FloatLayout):
    pass


class FileBrowser(FloatLayout):
    pass


class FileHeader(FloatLayout):
    current_dir = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = str(Path().home())


class Files(StackLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()
        self.prev_dir = str(Path.home().parent)

    def generate(self, widget):
        self.add_widget(NewFile(self, str(widget), text=''))


class Column(Widget):
    pass


class NewFile(Button):

    def __init__(self, ctx, txt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.txt = txt
        self.ctx = ctx

        if self.txt != '<-':
            path = Path(txt)
            stats = path.stat()

            self.ids.name.text = path.name
            self.ids.date.text = datetime.fromtimestamp(
                stats.st_mtime
            ).strftime('%d-%m-%Y')

            if path.is_dir():
                t = 'DIR'

                # self.ids.size.text = ' '.join(
                #    bytes_conversion(
                #        sum(
                #            f.stat().st_size for f in path.glob('**/*') if f.is_file()
                #        )
                #    )
                # )

            elif str(path).startswith('.') or path.suffix == '':
                t = str(path.parts[-1])

            else:
                t = path.suffix[1:].upper()
                self.ids.size.text = ' '.join(
                    bytes_conversion(
                        int(stats.st_size)
                    )
                )

            self.ids.type.text = t

        else:
            self.ids.name.text = '<-'
            self.ids.type.text = 'PARENT'

    def on_release(self):
        Logger.info(f'FileBrowser: Pressed "{self.txt}"')

        if self.txt == '<-':
            path = Path(self.ctx.prev_dir)
        else:
            path = Path(self.txt)

        if path.is_dir():
            self.ctx.clear_widgets()
            self.ctx.dirs = path.iterdir()

            if len(path.parts) > 1:
                self.ctx.prev_dir = str(path.parent)
                self.ctx.generate('<-')

            for d in self.ctx.dirs:
                self.ctx.generate(d)

            self.ctx.parent.parent.ids.header.current_dir = str(path)

        else:
            Logger.info('FileBrowser: Not a directory!')


class Footer(BoxLayout):
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == '1':
            print('1')
        if keycode[1] == '2':
            print('2')
        if keycode[1] == '3':
            print('3')
        if keycode[1] == '4':
            print('4')
        if keycode[1] == '5':
            print('5')
        if keycode[1] == '6':
            print('6')
        if keycode[1] == '7':
            print('7')
        if keycode[1] == '8':
            print('8')
        if keycode[1] == '9':
            print('9')
        if keycode[1] == '0':
            self.quit()
        return True

    def quit(self):
        popup = QuitPopup(size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()


class QuitPopup(Popup):

    def check(self, value: bool):
        if not value:
            self.dismiss()
        if value:
            quit(0)


class AncientTechApp(App):
    def build(self):
        return Main()
