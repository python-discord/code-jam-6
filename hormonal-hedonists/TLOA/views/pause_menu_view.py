from TLOA.core.constants import IMAGES_PATH, FONT_PATH

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore


class PauseMenuView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.store = JsonStore('Hi-Score.json')
        self.cols = 1
        self.padding = [0, 20]
        self.spacing = [0, 8]

        self.hi_score = Label(
            text="[color=ffffff]High Score: [/color][color=faff00]" +
                 str(self.store.get('hi-score')['score']) + "[/color]",
            font_size='20sp',
            font_name=FONT_PATH.format('Pacifico-Regular.ttf'),
            markup=True,
            size_hint=[1, None],
            height=40
        )
        self.button_resume = Button(
            background_normal=IMAGES_PATH.format('btn.png'),
            background_down=IMAGES_PATH.format('btn_pressed.png'),
            text="Resume",
            size_hint=[1, None],
            font_name=FONT_PATH.format('Pacifico-Regular.ttf'),
            font_size='18sp',
            height=40
        )

        self.button_main_menu = Button(
            background_normal=IMAGES_PATH.format('btn.png'),
            background_down=IMAGES_PATH.format('btn_pressed.png'),
            text="Restart Game",
            size_hint=[1, None],
            font_name=FONT_PATH.format('Pacifico-Regular.ttf'),
            font_size='18sp',
            height=40
        )

        self.button_exit = Button(
            background_normal=IMAGES_PATH.format('btn_g.png'),
            background_down=IMAGES_PATH.format('btn_g_pressed.png'),
            text="Exit From Burning",
            size_hint=[1, None],
            font_name=FONT_PATH.format('Pacifico-Regular.ttf'),
            font_size='18sp',
            height=40
        )
        self.add_widget(self.hi_score)
        self.add_widget(self.button_resume)
        self.add_widget(self.button_main_menu)
        self.add_widget(self.button_exit)
