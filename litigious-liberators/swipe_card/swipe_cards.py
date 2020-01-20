from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
import os
from os import listdir
from random import shuffle
from copy import deepcopy
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from yaml import safe_load

Config.set("input", "mouse", "mouse,multitouch_on_demand")


class Slide(BoxLayout):
    def __init__(self, profile, **kwargs):
        super(Slide, self).__init__(**kwargs)
        self.ids.picture.source = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), f"../profiles/pictures/{profile['Picture']}"
        )
        self.ids.name.text += profile["Name"]
        self.ids.species.text += profile["Species"]
        self.ids.age.text += str(profile["Age"])
        self.ids.job.text += profile["What I do"]


class Root(BoxLayout):
    swiper_obj = ObjectProperty(None)


class Swiper(Carousel):
    def __init__(self, **kwargs):
        super(Swiper, self).__init__(**kwargs)
        self.profile_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../profiles/write-ups"
        )
        self.static_profile_list = listdir(self.profile_dir)
        self.profile_list = deepcopy(self.static_profile_list)
        self.cycler = self.r_cycle(self.profile_list)
        self._selected = set()
        self.limit = 3
        with open(f"{self.profile_dir}/{next(self.cycler)}", "r") as profile_file:
            profile = safe_load(profile_file.read())
            self.add_widget(Slide(profile))

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if len(self._selected) >= self.limit:
            App.get_running_app().root.current = "After"

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            while True:
                next_profile = next(self.cycler)
                print(next_profile)
                if next_profile not in self.selected:
                    break
            if touch.button == "scrolldown":
                self.direction = "right"
                popup = SwipePopup()
                popup.open()
                with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
                    profile = safe_load(profile_file.read())
                    current = self.current_slide.ids.picture.source
                    current = current.split("/")[-1].split(".")[0] + ".yml"
                    self.selected |= {current}
                    self.add_widget(Slide(profile))
                self.load_next()

            elif touch.button == "scrollup":
                self.direction = "left"
                with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
                    profile = safe_load(profile_file.read())
                    self.add_widget(Slide(profile))
                self.load_next()

        if touch.is_double_tap:
            popup = SwipePopup()
            self.selected |= {self.current_slide.ids["picture"].source.split("/")[1]}
            popup.open()

    @staticmethod
    def r_cycle(x):
        while True:
            shuffle(x)
            for element in x:
                yield element


class SwipePopup(Popup):
    def change_screen(self):
        App.get_running_app().root.current = "After"
        self.dismiss()


class SwipingScreen(Screen):
    pass


class AfterSwipeScreen(Screen):
    pass


class CarouselApp(App):
    def build(self):
        Window.clearcolor = (188 / 255, 170 / 255, 164 / 255, 1)
        self.sm = ScreenManager()
        self.start_screen = SwipingScreen()
        self.second_screen = AfterSwipeScreen()
        self.sm.add_widget(self.start_screen)
        self.sm.add_widget(self.second_screen)
        return self.sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    CarouselApp().run()
