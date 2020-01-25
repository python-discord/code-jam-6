# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.toolbar import MDToolbar
from kivymd.cards import MDCard
from kivymd.label import MDLabel
from kivymd.slider import Slider


class CalibrationScreen(Screen):
    def __init__(self, **kwargs):
        super(CalibrationScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        calibration_card = MDCard(padding=dp(24),
                                  spacing=dp(24),
                                  orientation='vertical',
                                  size_hint=(0.75, 0.45),
                                  pos_hint={'top': 0.75, 'center_x': 0.5}
                                  )

        calibration_label = MDLabel(text='Calibrate Audio Input', font_style='H4', halign='center')
        calibration_label.theme_text_color = 'Custom'
        calibration_label.text_color = [1, 1, 1, 1]

        self.slider = Slider(size_hint=(0.75, None), pos_hint={'center_x': 0.5})
        self.slider.bind(value=self.on_value_change)

        helper_box = BoxLayout(orientation='horizontal')
        left_label = MDLabel(text='Less Sensitive', font_style='Caption')
        left_label.theme_text_color = 'Custom'
        left_label.text_color = [1, 1, 1, 1]
        right_label = MDLabel(text='More Sensitive', font_style='Caption')
        right_label.theme_text_color = 'Custom'
        right_label.text_color = [1, 1, 1, 1]

        helper_box.add_widget(Widget())
        helper_box.add_widget(left_label)
        helper_box.add_widget(Widget())
        helper_box.add_widget(Widget())
        helper_box.add_widget(Widget())
        helper_box.add_widget(right_label)
        helper_box.add_widget(Widget())

        calibration_card.add_widget(calibration_label)
        calibration_card.add_widget(Widget())
        calibration_card.add_widget(Widget())
        calibration_card.add_widget(self.slider)
        calibration_card.add_widget(helper_box)
        calibration_card.add_widget(Widget())

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title='Add Contact', anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.change_screen('welcome')]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(calibration_card)
        self.add_widget(toolbar_anchor)

    def on_value_change(self, instance, value):
        self.util.calibration = value
        print(value)

    def change_screen(self, screen):
        self.manager.current = screen
