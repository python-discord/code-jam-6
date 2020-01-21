from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
import os
from os import listdir
from random import shuffle
from copy import deepcopy
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from yaml import safe_load
from kivy.core.window import Window
from collections import Counter

Config.set("input", "mouse", "mouse,multitouch_on_demand")


class SelectionScreen(Screen):
    pass


class LossScreen(Screen):
    pass


class SwipePopup(Popup):
    def __init__(self, **kwargs):
        super(SwipePopup, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        self.orientation = "vertical"
        Clock.schedule_once(self.dismiss_popup, 2)

    def dismiss_popup(self, dt):
        self.dismiss()


class WinScreen(Screen):
    pass


class ProfileCard(Screen):
    def __init__(self, profile, **kwargs):
        super(ProfileCard, self).__init__(**kwargs)
        pic_addr = f"../profiles/pictures/{profile['Picture']}"
        self.ids.picture.source = os.path.join(os.path.dirname(os.path.abspath(__file__)), pic_addr)
        about_text = f"I'm a {profile['Age']} year old {profile['Species']}"
        self.right_delta = Counter(profile["right_delta"])
        self.left_delta = Counter(profile["left_delta"])
        self.ids.r_a1.text += str(profile["right_delta"]["a1"])
        self.ids.r_a2.text += str(profile["right_delta"]["a2"])
        self.ids.r_a3.text += str(profile["right_delta"]["a3"])
        self.ids.l_a1.text += str(profile["left_delta"]["a1"])
        self.ids.l_a2.text += str(profile["left_delta"]["a2"])
        self.ids.l_a3.text += str(profile["left_delta"]["a3"])
        self.ids.name.text += profile["Name"]
        self.ids.about.text = about_text
        self.ids.job.text += profile["What I do"]
        self.ids.name.font_name = "../fonts/Oldenburg/Oldenburg-Regular.ttf"


class ProfileList(ScreenManager):
    def __init__(self, **kwargs):
        super(ProfileList, self).__init__(**kwargs)
        self.profile_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../profiles/write-ups"
        )
        self.static_profile_list = listdir(self.profile_dir)
        self.profile_list = deepcopy(self.static_profile_list)
        self.cycler = self.r_cycle(self.profile_list)
        #  should be initialisable in main app
        self._attributes = Counter({"a1": 1, "a2": 1, "a3": 1})
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        with open(f"{self.profile_dir}/{next(self.cycler)}", "r") as profile_file:
            profile = safe_load(profile_file.read())
            self.add_widget(ProfileCard(profile))

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value
        for k, v in self._attributes.items():
            self._attributes[k] = min(10, v)
        if any(x < 0 for x in self._attributes.values()):
            App.get_running_app().root.current = "loss_screen"
        elif all(x == 10 for x in self._attributes.values()):
            App.get_running_app().root.current = "win_screen"
        print(self.attributes)

    @staticmethod
    def r_cycle(x):
        while True:
            shuffle(x)
            for element in x:
                yield element

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        next_profile = next(self.cycler)
        with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
            profile = safe_load(profile_file.read())
        current = self.current_screen
        trans = SlideTransition()
        totals = Counter()
        totals.update(self.attributes)
        if keycode[1] == "right":
            #  popup = SwipePopup(size_hint=(0.2, 0.4))
            #  popup.open()
            next_card = ProfileCard(profile)
            totals.update(current.right_delta)
            self.attributes = totals
            self.switch_to(next_card, direction="right", transition=trans)

        elif keycode[1] == "left":
            #  popup = SwipePopup(size_hint=(0.2, 0.4))
            #  popup.open()
            next_card = ProfileCard(profile)
            totals.update(current.left_delta)
            self.attributes = totals
            self.switch_to(next_card, direction="left", transition=trans)
        self.remove_widget(current)
        return True


class ProfilesApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.selection_screen = SelectionScreen()
        self.loss_screen = LossScreen()
        self.win_screen = WinScreen()
        self.sm.add_widget(self.selection_screen)
        self.sm.add_widget(self.loss_screen)
        self.sm.add_widget(self.win_screen)
        return self.sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    ProfilesApp().run()
