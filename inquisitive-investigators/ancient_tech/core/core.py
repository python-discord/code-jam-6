# This file was planned for use, but we ran out of time

from typing import Any, Dict, List, Union

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from .controller import Controller
from .exceptions import InvalidBrowser


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
        self, browser_side: str,
        state: int, files: List[str]
    ) -> None:
        if browser == 'left':
            browser = self.left_browser

        elif browser == 'right':
            browser = self.right_browser

        else:
            raise InvalidBrowser(
                'Browser position should be either "left" or "right"'
            )

        browser.recycle_view.update(state, files)

    def on_edit(self) -> None:
        pass

    def get_headers(self) -> Dict[
        str, Union[str, None]
    ]:
        """
        Returns current directory headers
        from each browser.
        """
        return {
            'left': self.left_browser.header.directory.text,
            'right': self.right_browser.header.directory.text,
        }
