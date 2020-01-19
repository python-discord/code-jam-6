from pathlib import Path
from datetime import datetime

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock

from .utils.utils import bytes_conversion


class Main(FloatLayout):
    pass


class FileBrowser(FloatLayout):
    pass


class FileHeader(FloatLayout):
    pass


class Files(StackLayout):

    do_layout_event = ObjectProperty(None, allownone=True)

    layout_delay_s = NumericProperty(0.15)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()
        self.prev_dir = str(Path.home().parent)

    def generate(self, widget):
        self.add_widget(NewFile(self, str(widget), text=''))

    def do_layout(self, *args, **kwargs):
        if self.do_layout_event is not None:
            self.do_layout_event.cancel()
        real_do_layout = super().do_layout
        self.do_layout_event = Clock.schedule_once(
            lambda dt: real_do_layout(*args, **kwargs),
            self.layout_delay_s)


class Column(Widget):
    pass


class NewFile(Button):

    def __init__(self, ctx, txt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.txt = txt
        self.ctx = ctx

        path = Path(txt)
        stats = path.stat()
        self.ids.name.text = path.name

        if self.txt != '../':
            self.ids.size.text = ' '.join(bytes_conversion(int(stats.st_size)))

            self.ids.date.text = datetime.fromtimestamp(
                stats.st_mtime
            ).strftime('%d-%m-%Y')

            if path.is_dir():
                t = 'DIR'

            elif str(path).startswith('.') or path.suffix == '':
                t = str(path.parts[-1])

            else:
                t = path.suffix[1:].upper()

            self.ids.type.text = t

    def on_release(self):
        Logger.info(f'FileBrowser: Pressed "{self.txt}"')

        if self.txt == '../':
            path = Path(self.ctx.prev_dir)
        else:
            path = Path(self.txt)

        if path.is_dir():
            self.ctx.clear_widgets()
            self.ctx.dirs = path.iterdir()

            if len(path.parts) > 1:
                self.ctx.prev_dir = str(path.parent)
                self.ctx.generate('../')

            for d in self.ctx.dirs:
                self.ctx.generate(d)

        else:
            Logger.info('FileBrowser: Not a directory!')


class Footer(BoxLayout):
    pass


class AncientTechApp(App):
    def build(self):
        return Main()
