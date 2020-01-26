from kivy.uix.widget import Widget
from kivy.core.window import Window


class InvalidGameScreen(Exception):
    def __init__(self, *args, **kwargs):
        pass


class ScreenManager(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = {}
        self.current = None

        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, _, width: int, height: int):
        if self.current is not None:
            self.current.width = width
            self.current.height = height
            self.current.on_resize(width, height)

    def add_screen(self, screen_class):
        if screen_class in self.screens:
            raise InvalidGameScreen(f'Game screen already in screen manager {str(screen_class)}')

        screen_instance = screen_class()
        self.screens[screen_class] = screen_instance
        screen_instance.on_create()

    def remove_screen(self, screen_class):
        if screen_class not in self.screens:
            raise InvalidGameScreen(f'Invalid game screen class {str(screen_class)}')

        instance = self.screens[screen_class]
        del self.screens[screen_class]

        instance.on_destroy()

    def set_current_screen(self, screen_class):
        if screen_class not in self.screens:
            raise InvalidGameScreen(f'Invalid game screen class {str(screen_class)}')

        if self.current is not None:
            self.remove_widget(self.current)
            self.current.on_close()

        self.current = self.screens[screen_class]
        self.current.on_open()
        self.add_widget(self.current)
