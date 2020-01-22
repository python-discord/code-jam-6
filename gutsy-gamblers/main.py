from datetime import datetime, timedelta, date
import pickle

from geopy.geocoders import Nominatim

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

from config import GEOLOCATION_KEY

kivy.require('1.11.1')


# Widget element things #
class DialWidget(FloatLayout):
    """
    Speed will become a fixed value of 86400 once completed.
    Image should, i suppose, be a fixed image?
    At some point we'll need to add a tuple(?) for sunrise / sunset times.
    """
    angle = NumericProperty(0)

    def __init__(self, day_length, dial_size, **kwargs):
        super(DialWidget, self).__init__(**kwargs)

        self.dial_size = dial_size

        # Split suntime tuple into named variables
        self.sun_angles = self.suntimes()
        self.sunrise = self.sun_angles[0]
        self.sunset = self.sun_angles[1]

        self.test_date = 0

        # Duration is how long it takes to perform the overall animation
        anim = Animation(angle=360, duration=day_length)
        anim += Animation(angle=360, duration=day_length)
        anim.repeat = True
        anim.start(self)

        # Shading widget
        self.dial_widget = DialEffectWidget((self.sunrise, self.sunset))

        # Add icons that can be arbitrarily rotated on canvas.
        self.sun_rise_marker = SunRiseMarker(self.sunrise)
        self.sun_set_marker = SunSetMarker(self.sunset)

        # Add widgets
        self.add_widget(self.dial_widget)
        self.add_widget(self.sun_rise_marker)
        self.add_widget(self.sun_set_marker)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

            self.remove_widget(self.dial_widget)
            self.remove_widget(self.sun_rise_marker)
            self.remove_widget(self.sun_set_marker)

            self.test_date += 30
            sun_angles = self.suntimes(self.test_date)

            # Split suntime tuple into named variables
            self.sunrise = sun_angles[0]
            self.sunset = sun_angles[1]

            # Shading widget
            self.dial_widget = DialEffectWidget((self.sunrise, self.sunset))

            # Add icons that can be arbitrarily rotated on canvas.
            self.sun_rise_marker = SunRiseMarker(self.sunrise)
            self.sun_set_marker = SunSetMarker(self.sunset)

            # Add widgets
            self.add_widget(self.dial_widget)
            self.add_widget(self.sun_rise_marker)
            self.add_widget(self.sun_set_marker)

    def suntimes(self, test_date=0):
        # lat_long = self.ipgeolocate()

        # pickled object for testing purposes
        with open('latlong.tmp', 'rb') as f:
            lat_long = pickle.load(f)

        sun_time = Sun(lat_long[0], lat_long[1])
        current_date = datetime.now()

        # For testing date roll over
        date_testing = datetime.now() + timedelta(days=test_date)
        print(f"New Date: {date_testing}")

        try:
            today_sunrise = sun_time.get_sunrise_time(date_testing)
        except SunTimeException:
            raise ValueError("AINT NO SUNSHINE WHEN SHE'S GONE")

        try:
            today_sunset = sun_time.get_sunset_time(date_testing)
        except SunTimeException:
            raise ValueError("HOLY SHIT TOO MUCH SUNSHINE WHEN SHE'S HERE")

        # This is *super* ugly, I'm sure we can find a more elegant way to do this
        now = datetime.utcnow() - timedelta(hours=0)
        today_sunrise = today_sunrise.replace(tzinfo=None)
        today_sunset = today_sunset.replace(tzinfo=None)

        # After Sunrise, after Sunset
        if now > today_sunrise and today_sunset:
            # Get timedelta for each
            today_sunrise = now - today_sunrise
            today_sunset = now - today_sunset

            # Convert timedelta into minutes and round
            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            # Convert minutes into angles
            today_sunrise = today_sunrise * 0.25
            today_sunset = today_sunset * 0.25

        # Before Sunrise, after Sunset
        elif now < today_sunrise and today_sunset:
            today_sunrise = today_sunrise - now
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            today_sunrise = 360 - (today_sunrise * 0.25)
            today_sunset = 360 - (today_sunset * 0.25)

        # After Sunrise, before Sunset
        else:
            today_sunrise = now - today_sunrise
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            today_sunrise = today_sunrise * 0.25
            today_sunset = 360 - (today_sunset * 0.25)

        return today_sunrise, today_sunset


class DialEffectWidget(EffectWidget):
    def __init__(self, angles, **kwargs):
        super(DialEffectWidget, self).__init__(**kwargs)

        self.shade_size = Window.height * 0.8, Window.height * 0.8
        self.add_widget(SunShading(angles))
        self.effects = [HorizontalBlurEffect(size=50.0), VerticalBlurEffect(size=50.0)]
        self.opacity = 0.25

    def _pos_check(self):
        if Window.width > Window.height:
            self.shade_size = Window.height * 0.8, Window.height * 0.8
        else:
            self.shade_size = Window.width * 0.8, Window.width * 0.8


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

    def _size_check(self):
        if Window.width > Window.height:
            self.shade_size = Window.height * 0.8, Window.height * 0.8
        else:
            self.shade_size = Window.width * 0.8, Window.width * 0.8


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
        self.window_width = Window.width

        self.add_widget(DialWidget(60, (0.8, 0.8)))
        self.add_widget(NowMarker())

    def on_size(self, a, b):
        # Redefine window_width for use in kv file
        self.window_width = Window.width

        # Maintains a constant aspect ratio of 0.75 (4:3)
        if (Window.height / Window.width) != 0.5625 and Window.fullscreen is False:
            Window.size = Window.width, Window.width * 0.5625

    def time_control_button(self):
        time_control_popup = TimeWizard()
        time_control_popup.open()

    def settings_button(self):
        SettingsScreen()

    def ipgeolocate(self):
        r = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_KEY}')
        resp = r.json()
        city = resp['city']
        state_prov = resp['state_prov']

        geolocate = Nominatim(user_agent="Code Jam 6: SunClock")
        location = geolocate.geocode(f"{city} {state_prov}")

        # pickle the object for testing purposes
        temp_latlong = [location.latitude, location.longitude]
        with open('latlong.tmp', 'wb') as f:
            pickle.dump(temp_latlong, f)

        return location.latitude, location.longitude


# Time control panel
class TimeWizard(Popup):
    def __init__(self, **kwargs):
        super(TimeWizard, self).__init__(**kwargs)


# Settings panel #
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

        # Don't forget to change this shit back.
        sm.current = 'main'

        return sm


if __name__ == '__main__':
    SunClock().run()
