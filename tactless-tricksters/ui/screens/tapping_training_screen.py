# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDRectangleFlatIconButton kivymd.uix.button
#:import MDFloatingActionButton kivymd.uix.button
#:import MDLabel kivymd.uix.label
#:import AudioIndicator ui.widgets.audio_indicator.AudioIndicator
#:import WelcomeButton ui.widgets.welcome_button

<TappingScreen>
    decode_input: decode_input

    MDCard:
        id: decode_card
        padding: dp(24)
        spacing: dp(24)
        orientation: 'vertical'
        size_hint: 0.85, 0.7
        pos_hint: {'top': 0.85, 'center_x': 0.5}
        elevation: 15
        md_bg_color: app.theme_cls.accent_color

        MDLabel:
            id: decode_label
            text: 'Decode Morse Code Audio'
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]

        Image: 
            size_hint: 1, 1
            source: 'ui\img\morse_code_alphabet.png' 
            
        MDTextFieldRound:
            id: decode_input
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'key-variant'
            icon_left_dasabled: True
            icon_right: 'database-export'
            icon_callback: root.clear_input()
        
        MDTextFieldRound:
            id: decode_input
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'key-variant'
            icon_left_dasabled: True
            icon_right: 'database-export'
            icon_callback: root.clear_input()
            
        MDLabel:
            id: decode_output_label
            text: ''
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]
        
        BoxLayout:
            anchor_x:'center'
            anchor_y:'bottom'
            padding: [dp(25), dp(25), dp(25), dp(25)]
        
            Button:
                id: record_button
                valign: 'center'
                icon: 'record'
                text: 'Tap Here'
                size: [dp(56), dp(56)]
                bg_color: app.theme_cls.primary_color
                text_color: [1, 1, 1, 1]
                on_press: root.decode_audio()
''')

training_difficulty_dict = {
    'letter': list('abcdefghijklmnopqrstuvwxyz'),
    'word': ['almost', 'already', 'benefit', 'between', 'book', 'born', 'capital', 'cause',
             'central', 'certain', 'church', 'cold', 'color', 'current', 'current', 'death',
             'deep', 'develop', 'develop', 'develop', 'door', 'dream', 'drive', 'drive', 'during',
             'east', 'easy', 'exist', 'fact', 'fast', 'focus', 'good', 'hair', 'herself', 'improve',
             'level', 'light', 'lose', 'lose', 'loss', 'matter', 'member', 'middle', 'middle',
             'middle', 'moment', 'move', 'music', 'music', 'music', 'nature', 'nice', 'north',
             'note', 'note', 'office', 'only', 'onto', 'other', 'perhaps', 'player', 'police',
             'problem', 'process', 'program', 'rather', 'really', 'really', 'recent', 'relate',
             'remain', 'rich', 'rise', 'risk', 'section', 'sense', 'shake', 'sister', 'society',
             'soldier', 'some', 'space', 'spring', 'stage', 'start', 'street', 'surface', 'system',
             'talk', 'throw', 'treat', 'trouble', 'various', 'walk', 'water', 'well', 'whether',
             'wish', 'woman', 'worker'],
    'sentence': ['a bullet she answered',
                 'a sleepy voice answered',
                 'come home right away',
                 'have you got our keys handy',
                 'he will allow a rare lie',
                 'hey come back he shouted',
                 'how do oysters make pearls',
                 'it sounded silly why go on',
                 'nobody likes snakes',
                 'none should ask less',
                 'now forget all this other',
                 'perfect he thought',
                 'shall we teach him some',
                 'stoneware clay for tiles',
                 'the hotel owner shrugged',
                 'the oasis was a mirage',
                 'turn shaker upside down']
}


class TappingScreen(Screen):
    training_difficulty = StringProperty("")
    decode_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TappingScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.amr = self.util.auto_morse_recognizer
        self.decode_output_label = self.ids.decode_output_label
        self.record_button = None  # self.ids.record_button
        self.audio_indicator = None  # self.ids.audio_indicator

    def update_text(self, morse_code):
        self.decode_input.text = self.decode_input.text + ''.join(morse_code)

    def clear_input(self):
        self.decode_input.text = ''

    def tapped(self):

        if self.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
            self.decode_output_label.text = 'Recording Started'
            print("Start audio recording thread")
            self.amr.start()
            Clock.schedule_interval(self.update_amr, self.amr.frame_rate)
        else:
            self.decode_output_label.text = 'Recording Stopped'
            print("Stopped audio recording thread")
            self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
            Clock.unschedule(self.update_amr)
            self.amr.stop()
            self.clear_input()

    def update_amr(self, kargs):
        print(kargs)
        morse_code, bit_signal = self.amr.update()
        self.update_text(morse_code)

    def return_home(self):
        self.manager.current = 'welcome'
