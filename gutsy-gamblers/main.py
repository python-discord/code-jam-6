from datetime import datetime, timedelta
import pickle

import kivy
import requests
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import Metrics
from kivy.properties import NumericProperty
from kivy.uix.effectwidget import EffectWidget, EffectBase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from suntime import Sun, SunTimeException

kivy.require('1.11.1')


from dials import (
    DialEffectWidget,
    DialWidget,
    DoubleVision,
    SunShading,
    SunRiseMarker,
    SunSetMarker,
    NowMarker
)

# Screens in the App #
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.dial_widget = DialWidget()
        self.now_marker = NowMarker()

        self.add_widget(self.dial_widget)
        self.add_widget(self.now_marker)

    def on_size(self, a, b):
        # Maintains a constant aspect ratio of 0.5625 (16:9)
        width, height = Window.size

        if not Window.fullscreen and (height / width) != 0.5625:
            height = width * 0.5625

        width /= Metrics.density
        height /= Metrics.density

        Window.size = (width, height)

    def time_control_button(self):
        time_control_popup = TimeWizard(self.dial_widget, self)
        time_control_popup.open()

    def settings_button(self):
        SettingsScreen()

    def ipgeolocate(self):
        resp = requests.get('http://ip-api.com/json/').json()

        # pickle the object for testing purposes
        temp_latlong = [resp['lat'], resp['lon']]
        with open('latlong.tmp', 'wb') as f:
            pickle.dump(temp_latlong, f)

        return resp['lat'], resp['lon']


# Time control panel #
class TimeWizard(Popup):
    def __init__(self, dial, parent, **kwargs):
        self.dial = dial
        super(TimeWizard, self).__init__(**kwargs)
        self.redraw_checkbox.bind(active=self.delta_override)

        self.current_date.text = self.dial.date.strftime("%d/%m/%Y")
        self.clock = Clock.schedule_interval(self.update_date, self.dial.midnight_delta)

    def update_date(self, *args):
        print('called update_date')
        self.clock.cancel()
        self.current_date.text = self.dial.date.strftime("%d/%m/%Y")
        self.clock = Clock.schedule_interval(self.update_date, self.dial.midnight_delta)

    def delta_override(self, *args):
        print('called delta_override')
        if self.redraw_checkbox.active is True:
            self.dial.midnight_delta = 0.1
            self.update_date()
            self.dial.redraw()
            # self.parent.speedy_time = True
        else:
            midnight = datetime.now() + timedelta(days=1)
            self.dial.midnight_delta = (datetime(year=midnight.year, month=midnight.month,
                                                 day=midnight.day,
                                                 hour=0, minute=0, second=0) - datetime.now()).seconds
            self.dial.redraw()
            # self.parent.speedy_time = False

    def revert_date(self):
        print('called revert_date')
        self.dial.date = datetime.now()
        self.update_date()
        self.dial.redraw()


# Settings panel #
class SettingsScreen(Popup):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        resp = requests.get('http://ip-api.com/json/').json()
        city = resp['city']
        region = resp['regionName']
        country = resp['country']

        settings_popup = Popup(title="Settings",
                               content=Label(
                                   text=f'Currently in {city}, {region}, {country}'
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
