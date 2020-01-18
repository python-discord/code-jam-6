from kivy.app import App
from kivy.core.window import Window


class Application(App):
    """Main application class."""

    def build(self) -> None:
        """Return the root widget."""
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'


if __name__ == "__main__":
    Application().run()
