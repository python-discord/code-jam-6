import json

import kivy
import requests
from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from config import GEOLOCATION_KEY

kivy.require('1.11.1')


# Widget element things #
class RotatingWidget(FloatLayout):
    """
    Speed will become a fixed value of 86400 once completed.
    Image should, i suppose, be a fixed image?
    At some point we'll need to add a tuple(?) for sunrise / sunset times.
    """
    angle = NumericProperty(0)

    def __init__(self, day_length, dial_image, dial_size, **kwargs):
        super(RotatingWidget, self).__init__(**kwargs)

        self.dial_file = dial_image
        self.dial_size = dial_size      # X / Y tuple.

        # Duration is how long it takes to perform the overall animation
        anim = Animation(angle=360, duration=day_length)
        anim += Animation(angle=360, duration=day_length)
        anim.repeat = True
        anim.start(self)

        # Create new widget for icons that can be arbitrarily rotated on canvas.
        self.add_widget(SunRise())
        self.add_widget(SunSet())

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class NowMarker(FloatLayout):
    pass


class SunRise(FloatLayout):
    pass


class SunSet(FloatLayout):
    pass


# Screens in the App #
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(RotatingWidget(50, 'assets/dial.png', (500, 500)))
        self.add_widget(NowMarker())

    def settings_button(self):
        SettingsScreen()


class SettingsScreen(Popup):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        r = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_KEY}')
        resp = r.json()
        city = resp['city']
        state_prov = resp['state_prov']
        country = resp['country_name']
        zipcode = resp['zipcode']

        settings_popup = Popup(title="Settings",
                               content=Label(text=f'Currently in {city}, {state_prov}, {country} {zipcode}'),
                               size_hint=(None, None), size=(500, 200))
        settings_popup.open()


class WindowManager(ScreenManager):
    pass


class SunClock(App):
    """
    Core class.
    """
    def build(self):
        Builder.load_file('main.kv')
        sm = WindowManager()

        screens = [MainScreen(name='main')]
        for screen in screens:
            sm.add_widget(screen)

        sm.current = 'main'

        return sm


if __name__ == '__main__':
    SunClock().run()
