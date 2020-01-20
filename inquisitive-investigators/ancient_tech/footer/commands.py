from typing import Any
from kivy.uix.popup import Popup


class AboutPopup(Popup):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.ids.AboutInfo.text = '''
        Scroll Effect! Hopefully it works!
        
        Features:
                  yeah there here, we got like a file thing
                  Oh yeah and were adding a text editor too!
                  is this scrolling yet?
        '''


class Mkdir(Popup):

    def mkdir(self) -> None:
        print(self.ids.create.text)


class QuitPopup(Popup):
    pass
