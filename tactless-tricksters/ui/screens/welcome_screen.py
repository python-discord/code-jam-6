from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
# Project imports
from ui.widgets.nav_drawer import MyNavigationLayout


Builder.load_string("""
#:kivy 1.11.1
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDRectangleFlatIconButton kivymd.uix.button
#:import MDLabel kivymd.uix.label

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
            pos: self.pos
            size: self.size
            source: 'ui/img/morse_code_bg.jpg'
            tex_coords: root.tex_coords
            
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
                    root.manager.current = 'sign_in'

            BlankLabel:

            WelcomeButton:
                text: 'Calibrate'
                icon: 'cogs'
                # TODO: create calibration screen

            BlankLabel:
            BlankLabel:

            WelcomeButton:
                text: 'Train'
                icon: 'dumbbell'
                on_press:
                    root.manager.current = 'training'

            BlankLabel:

            WelcomeButton:
                text: 'Message'
                icon: 'message'
                on_press:
                    # TODO: create exit function
                    root.manager.current = 'message'
""")


class WelcomeScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.nav_bar = MyNavigationLayout()
        self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.nav_bar_anchor.add_widget(self.nav_bar)
        self.add_widget(self.nav_bar_anchor)

        Clock.schedule_once(self.texture_init, 0)
        Clock.schedule_interval(self.scroll_texture, 1 / 60.)

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.
