from pathlib import Path

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty


class Main(FloatLayout):
    pass


class FileMain(BoxLayout):
    pass


class FileBrowser(StackLayout):
    dirs = ObjectProperty()
    prev_dir = StringProperty(str(Path(*Path().home().parts[:-1])))
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()

    def generate(self, widget):
        self.add_widget(File(self, text=str(widget)))


class SubBrowser(StackLayout):
    pass


class File(Button):
    ctx = ObjectProperty()

    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

    def on_release(self):
        Logger.info(f'FileBrowser: Pressed "{self.text}"')

        if self.text == '../':
            path = Path(self.ctx.prev_dir)
        else:
            path = Path(self.text)

        self.ctx.prev_dir = str(Path(*Path(path).parts[:-1]))

        if path.is_dir():
            self.ctx.clear_widgets()
            self.ctx.dirs = path.iterdir()

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


if __name__ == '__main__':
    AncientTechApp().run()
