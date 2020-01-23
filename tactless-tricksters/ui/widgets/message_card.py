from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.factory import Factory

from kivymd.cards import MDCardPost
from kivymd.label import MDLabel


class LongpressButton(ButtonBehavior):
    __events__ = ('on_long_press',)

    long_press_time = Factory.NumericProperty(0.5)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass


class MessageCard(LongpressButton, MDCardPost):
    def __init__(self, **kwargs):
        super(MessageCard, self).__init__(orientation='horizontal',
                                          size_hint=(1.1, None),
                                          height=dp(90),
                                          pos_hint={'center_x': 0.5},
                                          text_post=kwargs.get('text_post'),
                                          name_data=kwargs.get('name_data'),
                                          swipe=kwargs.get('swipe'),
                                          path_to_avatar=kwargs.get('source'),
                                          )

        self.util = kwargs.get('util')
        self.long_press = False
        self.children[0].children[0].children[0].bind(on_press=lambda x: self.delete_message())
        self.name = kwargs.get('name')

    def delete_message(self):
        print("Delete message")

    def on_release(self):
        if self.long_press:
            self.shift_post_left()
            self.long_press = False
        else:
            for screen in App.get_running_app().root.content.screens:
                if screen.name == 'conversation':
                    screen.ui_layout(self.name)
            App.get_running_app().root.content.current = 'conversation'

    def on_long_press(self):
        print('long press!')
        self.long_press = True

