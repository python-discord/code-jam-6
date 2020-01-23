from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

KV_RULES = """
<FileExplorerDisplay>:
    id: my_widget
    FileChooserListView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)

BoxLayout:
    FileExplorerDisplay:
    ScatterLayout:
        ImageDisplay:
            id: image
            source: 'python_discord_logo.png'
"""


class FileExplorerDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(FileExplorerDisplay, self).__init__(**kwargs)

    def selected(self, filename):
        """
        Display selected image.

        If an image is selected it will be displayed.
        An error is thrown if you go up a directory so it is ignored.
        """
        try:
            self.ids.image.source = filename[0]
        except Exception as e:
            print(e)
            pass


class ImageDisplay(Image):
    """Display Image."""

    def __init__(self, **kwargs):
        """
        Initilize Image Display.

        Binds the keyboard down event to a custom on_keyboard_down function.
        """
        super(ImageDisplay, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(None, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Moves the image around."""
        if keycode[1] == 'left':
            self.x -= 100
        elif keycode[1] == 'right':
            self.x += 100
        elif keycode[1] == 'up':
            self.y += 50
        elif keycode[1] == 'down':
            self.y -= 50
        return True


class Application(App):
    """The application class manages the lifecycle of your program, it
    has events like on_start, on_stop, etc.

    see https://kivy.org/doc/stable/api-kivy.app.html for more information.
    """

    def build(self):
        """whatever is returned by `build` will be the root of the
        widget tree of the application, and be accessible through the
        `root` attribute of the Application object.

        You can also delete this method and rely on the default behavior
        of loading a kv file in the same directory, named like the
        application class, but lower case. here, it would be
        application.kv.
        """
        return Builder.load_string(KV_RULES)


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    Application(title="Image Viewer").run()
