from typing import Any
from ..footer.commands import BasePopup


class SavePopup(BasePopup):

    def __init__(self, ctx: 'EditorIO', *args: Any, **kwargs: Any) -> None:
        super(SavePopup, self).__init__(ctx, *args, **kwargs)
        self.ctx = ctx

    def save(self) -> None:
        text = self.ctx.text
        path = self.ctx.file_path

        with open(path, 'w') as f:
            f.write(text)

        with open(path, 'r') as f:
            self.ctx.text = f.read()

        self.dismiss()
