from typing import Any, List

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty
)

from .controller import Controller

class BrowserScreen(Screen):
    pass


class Browser(FloatLayout, Controller):
    left_browser = ObjectProperty()
    right_browser = ObjectProperty()
    terminal = ObjectProperty()
    footer = ObjectProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Browser, self).__init__(*args, **kwargs)

    def on_update(
        self, browser: str, 
        state: int, files: List[str]
        ) -> None:
        if browser == 'left':
            browser = self.left_browser
        else:
            browser = self.right_browser

        browser.recycle_view.update(state, files)

    def on_edit(self) -> None:
        pass
