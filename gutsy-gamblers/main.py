from datetime import datetime, timedelta

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
        # anim.start(self)

        # Add icons that can be arbitrarily rotated on canvas.
        # Plus a time test
        now = datetime.now()

        sunrise = now - timedelta(hours=6)
        sunset = now + timedelta(hours=3)

        sunrise = now - sunrise
        sunrise = sunrise.seconds / 3600 * 15

        sunset = now - sunset
        sunset = sunset.seconds / 3600 * -15

        self.add_widget(SunRise(sunrise))
        self.add_widget(SunSet(sunset))

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class NowMarker(FloatLayout):
    pass


class SunRise(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunRise, self).__init__(**kwargs)
        self.rot_angle = rot_angle


class SunSet(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunSet, self).__init__(**kwargs)
        self.rot_angle = rot_angle


# Screens in the App #
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(RotatingWidget(50, 'assets/dial.png', (0.8, 0.8)))
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
                               content=Label(
                                   text=f'Currently in {city}, {state_prov}, {country} {zipcode}'
                               ),
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
