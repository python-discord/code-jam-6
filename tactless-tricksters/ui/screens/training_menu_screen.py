from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder


Builder.load_string('''
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDFloatingActionButton kivymd.uix.button
#:import MDLabel kivymd.uix.label
#:import AudioIndicator ui.widgets.audio_indicator.AudioIndicator
#:import WelcomeButton ui.widgets.welcome_button


<TrainingMenuScreen>
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'ui/img/morse_code_bg.jpg'
            tex_coords: root.tex_coords

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        
        MDToolbar:
            title: 'Training Menu'
            anchor_title: 'center'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: root.return_home()]]
            
    FloatLayout:
        size_hint: .8, .65
        pos_hint: {'center_x': 0.5, 'center_y': .45}
		canvas.before:
			Color:
				rgba: app.theme_cls.accent_color
			RoundedRectangle:
				size: self.size
				pos: self.pos
				radius: [dp(10)]
				
        BoxLayout:
        	size_hint: .8, .8
        	orientation: 'vertical'
        	spacing: dp(10)
        	pos_hint: {'center_x': 0.5, 'center_y': .5}

        	MDLabel:
            	text: 'Listening to Morse code'
            	font_style: 'H5'
            	halign: 'left'
            	theme_text_color: 'Custom'
            	text_color: [1, 1, 1, 1]
            	size_hint: 1, .3

        	GridLayout:
            	spacing: dp(20)
            	cols: 3
            	pos_hint: {'center_x': 0.5}

            	WelcomeButton:
                	text: 'letters'
                	icon: 'walk'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Easy"
                    	root.manager.current = 'listening'

            	WelcomeButton:
                	text: 'words'
                	icon: 'run'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Medium"
                    	root.manager.current = 'listening'

            	WelcomeButton:
                	text: 'sentences'
                	icon: 'bike'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Hard"
                    	root.manager.current = 'listening'

        	MDLabel:
            	text: 'Tapping Morse Code'
            	font_style: 'H5'
            	halign: 'left'
            	theme_text_color: 'Custom'
            	text_color: [1, 1, 1, 1]
            	size_hint: 1, .3

        	GridLayout:
            	spacing: dp(24)
            	cols: 3
            	pos_hint: {'center_x': 0.5}

            	WelcomeButton:
                	text: 'letters'
                	icon: 'walk'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Easy"
                    	root.manager.current = 'tapping'

            	WelcomeButton:
                	text: 'words'
                	icon: 'run'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Medium"
                    	root.manager.current = 'tapping'

            	WelcomeButton:
                	text: 'sentences'
                	icon: 'bike'
                	size_hint_x: 1
                	on_press:
                    	root.util.training_difficulty = "Hard"
                    	root.manager.current = 'tapping'
''')


class TrainingMenuScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(TrainingMenuScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')

        Clock.schedule_once(self.texture_init, 0)
        Clock.schedule_interval(self.scroll_texture, 1 / 60.)

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.

    def return_home(self):
        self.manager.current = 'welcome'