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
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

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
        self.popup = Popup(title="Description", content=Content(), size_hint=(0.4, 0.7))
        self.popup.content.button.bind(on_press=self.popup.dismiss)

    def on_press(self):
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()


class SelectionScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids["profile_list"]._keyboard = Window.request_keyboard(
            self.ids["profile_list"]._keyboard_closed, self.ids["profile_list"]
        )
        self.ids["profile_list"]._keyboard.bind(
            on_key_down=self.ids["profile_list"]._on_keyboard_down
        )
        return super().on_pre_enter(*args)


class ReplayScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sourcefile = os.path.join(dir_path, "./winloss.jpg")
        self.children[0].children[-1].source = sourcefile

    def replay(self):
        profile_carousel = self.manager.get_screen("create_profile").ids.profile_carousel
        profile_carousel.index = 0
        self.manager.current = "create_profile"


class LossScreen(ReplayScreen):
    pass


class WinScreen(ReplayScreen):
    pass


class ProfileCard(Screen):
    def __init__(self, profile, **kwargs):
        super(ProfileCard, self).__init__(**kwargs)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pic_addr = f"../profiles/pictures/{profile['Picture']}"
        sound_addr = f"../profiles/sounds/{profile.get('Sound')}"
        self.ids.picture.source = os.path.join(dir_path, pic_addr)
        self.sound = SoundLoader.load(os.path.join(dir_path, sound_addr))
        self.deltas = Counter(profile["Deltas"])
        self.ids.name.text = profile["Name"]
        self.ids.right_choice.text += profile["Choices"]["right"]
        self.ids.left_choice.text += profile["Choices"]["left"]
        self.results = profile["Results"]
        self.ids.picture.popup.content.story.text = profile["Biography"]
        # self.ids.name.font_name = "../fonts/Oldenburg/Oldenburg-Regular.ttf"
        # #When launching it from terminal using main.py the relative path to font changes.
        # To test this part as isolated app uncomment the line above and comment the line bellow
        self.ids.name.font_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../fonts/Oldenburg/Oldenburg-Regular.ttf"
        )

    def on_enter(self, *args):
        if self.sound:
            self.sound.play()
        return super().on_enter(*args)


class ProfileList(ScreenManager):
    _attributes = DictProperty(None)

    def __init__(self, **kwargs):
        super(ProfileList, self).__init__(**kwargs)
        self.profile_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../profiles/write-ups"
        )
        help = Label(
            text="""Your goal is to maximize all three attributes: Knowledge, Welfare,Energy:
        Use left/right arrowkeys to swipe the cards: each decision will influence your attributes!
        Press on each card image if you want to learn more about it ;)""",
            text_size=(self.width * 3, None),
        )
        self.help = Popup(title="Help", content=help, size_hint=(0.5, 0.7))
        # self.help.content.button.bind(on_press=self.help.dismiss)
        self.static_profile_list = listdir(self.profile_dir)
        self.profile_list = deepcopy(self.static_profile_list)
        self.cycler = self.r_cycle(self.profile_list)
        #  should be initialisable in main app
        self._attributes = Counter({"Knowledge": 5, "Welfare": 5, "Energy": 5})
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
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
        elif keycode[1] == "h":
            self.help.open()
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
