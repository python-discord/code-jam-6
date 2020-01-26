from TLOA.core.constants import IMAGES_PATH, FONT_PATH

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class PauseMenuView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.cols = 1
        self.padding = [0, 20]
        self.spacing = [0, 5]
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

        self.add_widget(self.button_resume)
        self.add_widget(self.button_main_menu)
        self.add_widget(self.button_exit)
