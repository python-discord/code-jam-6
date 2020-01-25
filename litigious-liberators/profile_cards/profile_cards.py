from kivymd.toast import toast
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.config import Config
from kivy.app import App
import os
from os import listdir
from random import shuffle
from copy import deepcopy
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, DictProperty
from yaml import safe_load
from kivy.core.window import Window
from collections import Counter

Config.set("input", "mouse", "mouse,multitouch_on_demand")


class ScrollableLabel(ScrollView):
    text = StringProperty("")


class Content(BoxLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.story = ScrollableLabel()
        self.button = Button(text="Close")
        self.add_widget(self.story)
        self.add_widget(self.button)


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.popup = Popup(content=Content(), size_hint=(0.4, 0.7))
        self.popup.content.button.bind(on_press=self.popup.dismiss)

    def on_press(self):
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()


class SelectionScreen(Screen):
    pass
    # def on_pre_enter(self, *args):
    #     # print(self.manager.get_screen("create_profile").__dict__)#.profile_data)
    #     return super().on_pre_enter(*args)
    #
    # def on_enter(self, *args):
    #     print(self.ids)
    #     print(self.manager.get_screen("create_profile").profile_data["attributes"])
    #     print(self.ids["profile_list"])
    #     self.ids["profile_list"]._attributes = self.manager.get_screen(
    #         "create_profile"
    #     ).profile_data["attributes"]
    #     return super().on_enter(*args)


class LossScreen(Screen):
    pass


class WinScreen(Screen):
    pass


class ProfileCard(Screen):
    def __init__(self, profile, **kwargs):
        super(ProfileCard, self).__init__(**kwargs)
        pic_addr = f"../profiles/pictures/{profile['Picture']}"
        self.ids.picture.source = os.path.join(os.path.dirname(os.path.abspath(__file__)), pic_addr)
        self.deltas = Counter(profile["Deltas"])
        self.ids.name.text = profile["Name"]
        self.ids.right_choice.text += profile["Choices"]["right"]
        self.ids.left_choice.text += profile["Choices"]["left"]
        self.results = profile["Results"]
        self.ids.picture.popup.content.story.text = profile["Biography"]
        # self.ids.name.font_name = "../fonts/Oldenburg/Oldenburg-Regular.ttf"
        # #When launching it from terminal using main.py the relative path to font changes.
        # To test this part as isolated app uncomment the line above and comment the line bellow
        self.ids.name.font_name = "fonts/Oldenburg/Oldenburg-Regular.ttf"


class ProfileList(ScreenManager):
    _attributes = DictProperty(None)

    def __init__(self, **kwargs):
        super(ProfileList, self).__init__(**kwargs)
        self.profile_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../profiles/write-ups"
        )
        self.static_profile_list = listdir(self.profile_dir)
        self.profile_list = deepcopy(self.static_profile_list)
        self.cycler = self.r_cycle(self.profile_list)
        #  should be initialisable in main app
        self._attributes = Counter({"Knowledge": 5, "Welfare": 5, "Energy": 5})
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

    def card_swipe(self, direction):
        next_profile = next(self.cycler)
        with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
            profile = safe_load(profile_file.read())
        current = self.current_screen
        trans = SlideTransition()
        totals = Counter()
        totals.update(self.attributes)
        next_card = ProfileCard(profile)
        delta = current.deltas[direction]
        totals.update(delta)
        self.attributes = totals
        message = direction.upper() + "\n" + current.results[direction]
        for k, v in delta.items():
            message += f"{k}: {v if v < 0 else '+' + str(v)}\n"
        toast(message.rstrip())
        self.switch_to(next_card, direction=direction, transition=trans)
        current.ids.picture.close_popup()
        self.remove_widget(current)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "right":
            self.card_swipe("right")

        elif keycode[1] == "left":
            self.card_swipe("left")
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
