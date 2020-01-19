from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


class NameScreen(Screen):
    def prev_page(self):
        # TODO: send to welcome page
        pass

    def next_page(self):
        # TODO: validations?
        self.manager.transition.direction = "left"
        self.manager.current = "gender_screen"


class GenderScreen(Screen):
    def prev_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "name_screen"

    def next_page(self):
        # TODO: validations?
        self.manager.transition.direction = "left"
        self.manager.current = "sexual_orientation_screen"


class AgeScreen(Screen):
    # TODO: bithdate widget in kivy?
    pass


class SexualOrientationScreen(Screen):
    def prev_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "gender_screen"

    def next_page(self):
        # TODO: validation?
        self.manager.transition.direction = "left"
        self.manager.current = "preference_screen"


class PreferenceScreen(Screen):
    def prev_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "sexual_orientation_screen"

    def next_page(self):
        # TODO: validation?
        self.manager.transition.direction = "left"
        self.manager.current = "profession_screen"


class ProfessionScreen(Screen):
    def prev_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "preference_screen"

    def next_page(self):
        # TODO: validation?
        self.manager.transition.direction = "left"
        self.manager.current = "bio_screen"


class BioScreen(Screen):
    def prev_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "profession_screen"

    def next_page(self):
        # TODO: validation?
        print("hello")


class CreateProfileApp(App):
    def build(self):
        # Create the manager
        sm = ScreenManager()
        sm.add_widget(NameScreen(name="name_screen"))
        sm.add_widget(GenderScreen(name="gender_screen"))
        sm.add_widget(SexualOrientationScreen(name="sexual_orientation_screen"))
        sm.add_widget(PreferenceScreen(name="preference_screen"))
        sm.add_widget(ProfessionScreen(name="profession_screen"))
        sm.add_widget(BioScreen(name="bio_screen"))
        # sm.current = "name_screen"
        return sm


if __name__ == "__main__":
    CreateProfileApp().run()
