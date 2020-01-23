from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.button import MDRectangleFlatIconButton
from kivymd.label import MDLabel


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.app = App.get_running_app()
        self.ui_layout()

    def ui_layout(self):
        with self.canvas:
            Rectangle(source="ui/img/welcome_2.png", size=(Window.width, Window.height))

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title="Enigma", anchor_title='center')
        toolbar.md_bg_color = self.app.get_running_app().theme_cls.primary_color
        toolbar_anchor.add_widget(toolbar)

        welcome_label = MDLabel(text='Welcome!', font_style='H4', halign='center')
        welcome_label.theme_text_color = 'Custom'
        welcome_label.text_color = [1, 1, 1, 1]



class WelcomeButton(MDRectangleFlatIconButton):
    """Simple buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._change_color)

    def _change_color(self, _):
        """Workaround to access children in this kivymd widget"""
        # Set Label to White
        self.children[0].children[0].text_color = [1, 1, 1, 1]
        self.children[0].children[0].font_size = 20
        # Set Icon to white
        self.children[0].children[1].text_color = [1, 1, 1, 1]
        self.children[0].children[1].font_size = 30


class WelcomeScreen(Screen):

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
