from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from onboarding.onboarding import OnboardingScreen
from swipe_card.swipe_cards import SwipingScreen, AfterSwipeScreen
from profile_creation.createprofile import CreateProfile
from kivy.lang import Builder
from kivy.core.window import Window


class TindosaurApp(App):
    def build(self):
        Builder.load_file("onboarding/onboarding.kv")
        Builder.load_file("profile_creation/createprofile.kv")
        Builder.load_file("swipe_card/carousel.kv")
        Window.clearcolor = (188 / 255, 170 / 255, 164 / 255, 1)
        sm = ScreenManager()
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(CreateProfile(name="create_profile"))
        sm.add_widget(SwipingScreen(name="swipe_cards"))
        sm.add_widget(AfterSwipeScreen(name="after"))
        return sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    TindosaurApp().run()
