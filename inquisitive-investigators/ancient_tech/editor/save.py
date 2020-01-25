from typing import Any
from kivy.uix.popup import Popup

class SavePopup(Popup):

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any) -> None:
        super().__init__(ctx, *args, **kwargs)
        self.ctx = ctx

    def save(self) -> None:
        text = self.ctx.text
        path = self.ctx.file_path

        with open(path, 'w') as f:
            f.write(text)

        with open(path, 'r') as f:
            self.ctx.text = f.read()
