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
            self.parent.parent.manager.current = "after"

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            while True:
                next_profile = next(self.cycler)
                if next_profile not in self.selected:
                    break
            if touch.button == "scrolldown":
                self.direction = "right"
                popup = SwipePopup(caller=self)
                popup.open()
                with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
                    profile = safe_load(profile_file.read())
                    self.selected |= {
                        os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            f"../profiles/pictures/{profile['Picture']}",
                        )
                    }
                    self.add_widget(Slide(profile))
                self.load_next()

            elif touch.button == "scrollup":
                self.direction = "left"
                with open(f"{self.profile_dir}/{next_profile}", "r") as profile_file:
                    profile = safe_load(profile_file.read())
                    self.add_widget(Slide(profile))
                self.load_next()

        if touch.is_double_tap:
            popup = SwipePopup(caller=self)
            self.selected |= {self.current_slide.ids["picture"].source.split("/")[1]}
            popup.open()

    @staticmethod
    def r_cycle(x):
        while True:
            shuffle(x)
            for element in x:
                yield element


class SwipePopup(Popup):
    def __init__(self, *, caller, **kwargs):
        self.caller = caller
        super(SwipePopup, self).__init__(**kwargs)

    def change_screen(self):
        App.get_running_app().root.current = "after"
        self.dismiss()


class SwipingScreen(Screen):
    pass


class AfterSwipeScreen(Screen):
    pass


class CarouselApp(App):
    def build(self):
        Window.clearcolor = (188 / 255, 170 / 255, 164 / 255, 1)
        sm = ScreenManager()
        sm.add_widget(SwipingScreen(name="swipe_cards"))
        sm.add_widget(AfterSwipeScreen(name="after"))
        return sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    CarouselApp().run()
