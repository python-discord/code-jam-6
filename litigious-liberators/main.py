from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from onboarding.onboarding import OnboardingScreen
from profile_cards.profile_cards import SelectionScreen, PostSelectionScreen
from profile_creation.createprofile import CreateProfile
from kivy.lang import Builder


class TindosaurApp(App):
    def build(self):
        Builder.load_file("onboarding/onboarding.kv")
        Builder.load_file("profile_creation/createprofile.kv")
        Builder.load_file("profile_cards/profiles.kv")
        sm = ScreenManager()
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(CreateProfile(name="create_profile"))
        sm.add_widget(SelectionScreen(name="profile_selection"))
        sm.add_widget(PostSelectionScreen(name="post_selection_screen"))
        return sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    TindosaurApp().run()
