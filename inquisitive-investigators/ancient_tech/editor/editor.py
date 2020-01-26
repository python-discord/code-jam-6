from typing import Any

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    ListProperty
)

from .editorIO import EditorIO

Builder.load_file('./ancient_tech/editor/editor.kv')


class TextEditor(Screen):
    editor = ObjectProperty()
    recycler = ObjectProperty()

    foreground_color = ListProperty((1, 1, 1, 1))
    background_color = ListProperty((0, 0, 0, 1))

    font_name = StringProperty(
        './ancient_tech/static/retro_font.ttf'
    )
    font_size = NumericProperty(14)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TextEditor, self).__init__(*args, **kwargs)


class F(FloatLayout):
    pass
