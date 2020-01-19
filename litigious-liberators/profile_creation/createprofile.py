from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel


class CreateProfile(Screen):
    pass


class ProfileSwiper(Carousel):
    def on_touch_down(self, touch):
        return super(Carousel, self).on_touch_down(touch)


class AfterSwipeScreen(Screen):
    pass


class CreateProfileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CreateProfile(name="create_profile"))
        sm.add_widget(AfterSwipeScreen(name="swipe_cards"))
        return sm


if __name__ == "__main__":
    CreateProfileApp().run()
