from datetime import datetime, timedelta
import kivy
import re

from geopy import Point
from geopy.geocoders import Nominatim
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import Metrics
from kivy.properties import ConfigParserProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

import datahelpers
from dials import (
    DialWidget,
    NowMarker
)

kivy.require('1.11.1')


# Screens in the App #
class MainScreen(Screen):
    config_latlon = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_LATLON, 'app', val_type=str)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # hacky config file validation for bad or missing coords

        # we have to store or it would draw under the dials
        settings_modal = None

        try:
            pt = Point(self.config_latlon)
        except ValueError:

            pt = Point()
            settings_modal = SettingsScreen()
            settings_modal.config_friendlyname = ''

            if self.config_latlon != '':
                settings_modal.feedback.text =\
                    "Invalid location detected in config, please select a new location"
                self.config_latlon = ''

        self.dial_widget = DialWidget(latlon_point=pt)
        self.now_marker = NowMarker()

        self.add_widget(self.dial_widget)
        self.add_widget(self.now_marker)

        # workaround for kivy's LIFO draw order
        if settings_modal is not None:
            Clock.schedule_once(lambda dt: settings_modal.open(), 0.5)

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
        SettingsScreen().open()


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
            # Good thing flake8 isn't 78 chars huh?
            self.dial.midnight_delta = (datetime(year=midnight.year,
                                                 month=midnight.month,
                                                 day=midnight.day,
                                                 hour=0,
                                                 minute=0,
                                                 second=0) - datetime.now()).seconds
            self.dial.redraw()
            # self.parent.speedy_time = False

    def revert_date(self):
        print('called revert_date')
        self.dial.date = datetime.now()
        self.update_date()
        self.dial.redraw()


# Settings panel #
class UpdateLocationButton(Button):
    """
    Button for updating location.
    """
    settingsscreen = ObjectProperty()

    latlon = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_LATLON, 'app', val_type=str)
    friendlyname = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_FRIENDLY, 'app', val_type=str)

    latlong_regex = re.compile(r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$')

    def on_press(self):
        input_location = self.settingsscreen.location_field.text
        feedback = self.settingsscreen.feedback

        # Use a regex to check if they entered a lat and long manually
        latlong_re = self.latlong_regex.match(input_location)

        if latlong_re:
            lat, _, long, _ = latlong_re.groups()
            self.latlon = f'{lat},{long}'
            self.friendlyname = f'{lat},{long}'
            feedback.text = 'Successfully set Latitude and Longitude'
            return

        geolocator = Nominatim(user_agent="interactive_python_session_client")
        resp = geolocator.geocode(input_location)

        # Possible that location isn't found
        if not resp:
            feedback.text = 'Failed to find location, try again!'
            return

        self.friendlyname = resp.address
        self.latlon = f'{resp.latitude},{resp.longitude}'
        feedback.text = f'Successfully set location to {resp.address}'


class GuessLocationButton(Button):
    """
    Holds IP guessing logic for now.

    Putting all of it in screen caused weakref errors.
    """
    settingsscreen = ObjectProperty()
    latlon = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_LATLON, 'app', val_type=str)
    friendlyname = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_FRIENDLY, 'app', val_type=str)

    def on_press(self):

        response = datahelpers.guess_location_by_ip()

        location_field = self.settingsscreen.location_field
        feedback = self.settingsscreen.feedback

        if response is None:
            feedback.text = "Error when connecting to geoip server"
            return

        self.disabled = True

        self.latlon = response[datahelpers.LOCATION_LATLON]

        if datahelpers.LOCATION_FRIENDLY in response:
            location_field.text = response[datahelpers.LOCATION_FRIENDLY]
            self.friendlyname = response[datahelpers.LOCATION_FRIENDLY]
        else:
            location_field.text = self.latlon
            self.friendlyname = self.latlon

        feedback.text = "Successfully got location!"
        Clock.schedule_once(lambda dt: setattr(self, 'disabled', False), timeout=45 / 60)
        Clock.schedule_once(lambda dt: setattr(feedback, 'text', ""), timeout=5)


class SettingsScreen(Popup):

    sundial = ObjectProperty()  # passed in if needed?

    location_field = ObjectProperty()
    close_button = ObjectProperty()
    feedback = ObjectProperty()

    config_latlon = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_LATLON, 'app', val_type=str)
    config_friendlyname = ConfigParserProperty(
        '', 'global', datahelpers.LOCATION_FRIENDLY, 'app', val_type=str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close_button.disabled = self.config_latlon == ''
        self.location_field.text = self.config_friendlyname

    def on_config_latlon(self, instance, value):
        """Assumes this will only ever be set on a valid key"""
        self.close_button.disabled = False


class SunClock(App):
    """
    Core class.
    """

    # properties because we can't use on_config_change as it's tied into the
    # mobile oriented settings system

    def build_config(self, config):
        config.setdefaults('global', {
            'location_friendly': '',
            'location_latlon': '',
        })

    def build(self):
        Builder.load_file('main.kv')
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))

        sm.current = 'main'

        return sm


if __name__ == '__main__':
    SunClock().run()
