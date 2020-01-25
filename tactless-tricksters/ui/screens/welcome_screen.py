from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
# KivyMD imports
from kivymd.button import MDRectangleFlatIconButton
# Project imports
from ui.widgets.nav_drawer import MyNavigationLayout


Builder.load_string("""
#:kivy 1.11.1
#:import MDCard kivymd.cards
#:import MDToolbar kivymd.toolbar
#:import MDRectangleFlatIconButton kivymd.button
#:import MDLabel kivymd.label

<WelcomeButton>
    elevation_normal: 10
    md_bg_color: app.theme_cls.primary_color
    md_border_color: app.theme_cls.primary_color
    pos_hint: {'center_y': 1.5, 'center_x': 0.5}


<BlankLabel@MDLabel>
    text: ''
#    font_style: 'H6'

<WelcomeScreen>
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'ui/img/welcome_2.png'

    MDCard:
        padding: dp(24)
        spacing: dp(24)
        orientation: 'vertical'
        size_hint: .65, .35
        pos_hint: {'center_x': 0.5, 'top': 0.8}
        md_bg_color: app.theme_cls.accent_color

        MDLabel:
            text: 'Welcome!'
            font_style: 'H4'
            halign: 'center'
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]
            size_hint: 1, .3

        GridLayout:
            spacing: dp(24)
            cols: 5
            pos_hint: {'center_x': 0.5}

            BlankLabel:

            WelcomeButton:
                text: 'Decode'
                icon: 'database-export'
                on_press:
                    root.manager.current = 'decode'

            BlankLabel:

            WelcomeButton:
                text: 'Encode'
                icon: 'database-import'
                on_press:
                    root.manager.current = 'encode'

            BlankLabel:
            BlankLabel:

            WelcomeButton:
                text: 'Sign In'
                icon: 'login-variant'
                on_press:
                    root.manager.current = ''

            BlankLabel:

            WelcomeButton:
                text: 'Calibrate'
                icon: 'cogs'
                # TODO: create calibration screen
""")


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
        self.nav_bar = MyNavigationLayout()
        self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.nav_bar_anchor.add_widget(self.nav_bar)
        self.add_widget(self.nav_bar_anchor)
