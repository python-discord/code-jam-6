from typing import Any

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from .image import DynamicImage
from ..utils.paths import PHOTO_VIEWER_KV

Builder.load_file(PHOTO_VIEWER_KV)

class PhotoViewer(Screen):
    dynimg = ObjectProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PhotoViewer, self).__init__(*args, **kwargs)


class ImageInterface(Widget):
    pass


class Foot(FloatLayout):
    pass
