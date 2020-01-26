from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from collections import Counter
from kivy.properties import DictProperty

import json
import os


class CreateProfile(Screen):
    profile_data = DictProperty({})

    def on_pre_leave(self, *args):
        # load the answer to score mapping for each question from db
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "quetoscore.json")
        with open(filepath) as f:
            que_to_score = json.load(f)

        # store the initial state of player based on selected profile creation quetions
        self.profile_data["attributes"] = Counter({"Knowledge": 0, "Welfare": 0, "Energy": 0})

        # calculate initial state based on selected answers
        for idx, slide in enumerate(self.ids.profile_carousel.slides):
            if idx == 0:
                # first slide is for name
                self.profile_data["name"] = slide.children[1].children[0].text

            else:
                # iterate over toggle buttons and get their state and update
                # the attributes based on selected toggle button
                for idx, toggle_btn in enumerate(slide.children[1].children):
                    if toggle_btn.state == "down":
                        attributes = que_to_score[toggle_btn.group][f"A{idx+1}"]
                        self.profile_data["attributes"].update(attributes)

        # self.manager.get_screen("profile_selection").ids["profile_list"]._attributes = self.manager.get_screen("create_profile").profile_data["attributes"]
        print(self.manager.get_screen("profile_selection").ids["profile_list"]._attributes)
        print(self.profile_data["attributes"])
        self.manager.get_screen("profile_selection").ids[
            "profile_list"
        ]._attributes = self.profile_data["attributes"]
        return super().on_pre_leave(*args)


class ProfileSwiper(Carousel):
    def on_touch_down(self, touch):
        return super().on_touch_down(touch)


class AfterSwipeScreen(Screen):
    def on_enter(self, *args):
        print(self.manager.get_screen("create_profile").profile_data)
        return super().on_enter(*args)


class CreateProfileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CreateProfile(name="create_profile"))
        sm.add_widget(AfterSwipeScreen(name="profile_selection"))
        return sm


if __name__ == "__main__":
    CreateProfileApp().run()
