from datetime import datetime, date
import pickle

import kivy
import requests
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.effectwidget import EffectWidget, HorizontalBlurEffect, VerticalBlurEffect
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from suntime import Sun, SunTimeException

kivy.require('1.11.1')


# Widget element things #
class DialWidget(FloatLayout):
    """
    Speed will become a fixed value of 86400 once completed.
    Image should, i suppose, be a fixed image?
    At some point we'll need to add a tuple(?) for sunrise / sunset times.
    """
    angle = NumericProperty(0)

    def __init__(self, day_length, dial_image, dial_size, sun_angles, **kwargs):
        super(DialWidget, self).__init__(**kwargs)

        self.dial_file = dial_image
        self.dial_size = dial_size
        self.sun_angles = sun_angles

        # Duration is how long it takes to perform the overall animation
        anim = Animation(angle=360, duration=day_length)
        anim += Animation(angle=360, duration=day_length)
        anim.repeat = True
        anim.start(self)

        # Split suntime tuple into named variables
        sunrise = self.sun_angles[0]
        sunset = self.sun_angles[1]

        self.add_widget(DialEffectWidget((sunrise, sunset)))

        # Add icons that can be arbitrarily rotated on canvas.
        self.add_widget(SunRiseMarker(sunrise))
        self.add_widget(SunSetMarker(sunset))

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class SunShading(FloatLayout):
    def __init__(self, angles, **kwargs):
        super(SunShading, self).__init__(**kwargs)

        rise_angle = angles[0]
        set_angle = angles[1]

        sun_colour = (0.9, 0.9, 0.08, 1)
        shade_colour = (0.0, 0.2, 0.4, 1)

        # More of bisks brutally ugly work
        if rise_angle < set_angle:
            self.shade_one_angle_start = 360 - set_angle
            self.shade_one_angle_stop = 360 - rise_angle
            self.shade_one_color = shade_colour

            self.sun_one_angle_start = 0
            self.sun_one_angle_stop = 360 - set_angle
            self.sun_one_color = sun_colour
            self.sun_two_angle_start = 360 - rise_angle
            self.sun_two_angle_stop = 360
            self.sun_two_color = sun_colour

        elif rise_angle > set_angle:
            self.shade_one_angle_start = 360 - set_angle
            self.shade_one_angle_stop = 360
            self.shade_one_color = shade_colour
            self.shade_two_angle_start = 360 - rise_angle
            self.shade_two_angle_stop = 0
            self.shade_two_color = shade_colour

            self.sun_one_angle_start = 360 - rise_angle
            self.sun_one_angle_stop = 360 - set_angle
            self.sun_one_color = sun_colour

        self.shade_size = Window.height * 0.8, Window.height * 0.8
        # self.shade_angle_start = angles[1] - 360
        # self.shade_angle_stop = 360

    def _size_check(self):
        self.shade_size = Window.height * 0.8, Window.height * 0.8


class DialEffectWidget(EffectWidget):
    def __init__(self, angles, **kwargs):
        super(DialEffectWidget, self).__init__(**kwargs)

        self.shade_size = Window.height * 0.8, Window.height * 0.8
        self.add_widget(SunShading(angles))
        self.effects = [HorizontalBlurEffect(size=50.0), VerticalBlurEffect(size=50.0)]
        self.opacity = 0.25

    def _pos_check(self):
        self.shade_size = Window.height * 0.8, Window.height * 0.8


class SunRiseMarker(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunRiseMarker, self).__init__(**kwargs)
        self.rot_angle = rot_angle


class SunSetMarker(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunSetMarker, self).__init__(**kwargs)
        self.rot_angle = rot_angle


class NowMarker(FloatLayout):
    pass


# Screens in the App #
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.add_widget(DialWidget(86400, 'assets/dial.png', (0.8, 0.8), self.suntimes()))
        self.add_widget(NowMarker())
        self.suntimes()

    def on_size(self, a, b):
        # Maintains a constant aspect ratio of 0.75 (4:3)
        if (Window.height / Window.width) != 0.75:
            Window.size = Window.width, Window.width * 0.75

    def settings_button(self):
        SettingsScreen()

    def ipgeolocate(self):
        resp = requests.get('http://ip-api.com/json/').json()

        # pickle the object for testing purposes
        temp_latlong = [resp['lat'], resp['lon']]
        with open('latlong.tmp', 'wb') as f:
            pickle.dump(temp_latlong, f)

        return resp['lat'], resp['lon']

    def suntimes(self):
        lat_long = self.ipgeolocate()

        # pickled object for testing purposes
        # with open('latlong.tmp', 'rb') as f:
        #     lat_long = pickle.load(f)

        sun_time = Sun(lat_long[0], lat_long[1])

        test_date = date(year=2020, month=12, day=20)

        try:
            today_sunrise = sun_time.get_sunrise_time(test_date)
        except SunTimeException:
            raise ValueError("AINT NO SUNSHINE WHEN SHE'S GONE")

        try:
            today_sunset = sun_time.get_sunset_time(test_date)
        except SunTimeException:
            raise ValueError("HOLY SHIT TOO MUCH SUNSHINE WHEN SHE'S HERE")

        # This is *super* ugly, I'm sure we can find a more elegant way to do this
        now = datetime.utcnow()
        today_sunrise = today_sunrise.replace(tzinfo=None)
        today_sunset = today_sunset.replace(tzinfo=None)

        if now > today_sunrise and today_sunset:
            # Don't need TZInfo to perform this operation
            today_sunrise = now - today_sunrise
            today_sunset = now - today_sunset

            # Convert timedelta into minutes and round
            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            # Since icons are in the "past" (to the left) keep the angles positive
            # After Sunrise, after Sunset
            today_sunrise = today_sunrise * 0.25
            today_sunset = today_sunset * 0.25

        elif now < today_sunrise and today_sunset:
            today_sunrise = today_sunrise - now
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            # Since icons are in the "future" (to the right) keep angles negative
            # Before Sunrise, after Sunset
            today_sunrise = 360 - (today_sunrise * 0.25)
            today_sunset = 360 - (today_sunset * 0.25)

        else:
            today_sunrise = now - today_sunrise
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            # After Sunrise, before Sunset
            today_sunrise = today_sunrise * 0.25
            today_sunset = 360 - (today_sunset * 0.25)

        return today_sunrise, today_sunset


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
