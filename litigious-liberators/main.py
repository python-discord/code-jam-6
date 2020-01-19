from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from swipe_card.swipe_cards import SwipingScreen
from kivy.lang import Builder
from kivy.core.window import Window

class TindosaurApp(App):
    def build(self):
        Builder.load_file("swipe_card/carousel.kv")
        Window.clearcolor = (188 / 255, 170 / 255, 164 / 255, 1)
        self.sm = ScreenManager()
        self.start_screen = SwipingScreen()
        #self.second_screen = AfterSwipeScreen()
        self.sm.add_widget(self.start_screen)
        #self.sm.add_widget(self.second_screen)
        return self.sm


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    TindosaurApp().run()