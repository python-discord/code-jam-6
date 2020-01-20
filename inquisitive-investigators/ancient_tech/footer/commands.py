from typing import Any
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class BasePopup(Popup):
    
    def __init__(
            self, ctx: 'Footer', *args: Any, **kwargs: Any
        ) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx

    def on_dismiss(self, *args: Any, **kwargs: Any):
        self.ctx._open = False
        return super(BasePopup, self).on_dismiss(
            *args, **kwargs
        )


class AboutPopup(BasePopup):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ids.AboutInfo.text = '''
        Scroll Effect! Hopefully it works!
        
        Features:
                  yeah there here, we got like a file thing
                  Oh yeah and were adding a text editor too!
                  is this scrolling yet?
        '''


class Mkdir(BasePopup):

    def mkdir(self) -> None:
        print(self.ids.create.text)


class QuitPopup(BasePopup):
    pass
