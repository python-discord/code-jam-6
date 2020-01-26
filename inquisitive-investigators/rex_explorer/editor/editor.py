from typing import Any

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    ColorProperty
)

from .editorIO import EditorIO
from ..utils.paths import EDITOR_KV, FONT

Builder.load_file(EDITOR_KV)


class TextEditor(Screen):
    editor = ObjectProperty()
    recycler = ObjectProperty()

    foreground_color = ColorProperty((1, 1, 1, 1))
    background_color = ColorProperty((0, 0, 0, 1))

    font_name = StringProperty(FONT)
    font_size = NumericProperty(12.5)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TextEditor, self).__init__(*args, **kwargs)


class F(FloatLayout):
    pass
