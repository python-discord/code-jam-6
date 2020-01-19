from kivy.config import Config
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from os import listdir
from random import shuffle
from copy import deepcopy
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Config.set("input", "mouse", "mouse,multitouch_on_demand")


class Root(BoxLayout):
    swiper_obj = ObjectProperty(None)


class Swiper(Carousel):
    def __init__(self, **kwargs):
        super(Swiper, self).__init__(**kwargs)
        self.pic_dir = "pictures"
        self.static_pic_list = listdir(self.pic_dir)
        self.pic_list = deepcopy(self.static_pic_list)
        self.cycler = self.r_cycle(self.pic_list)
        self.selected = set()
        self.add_widget(Image(source=f"{self.pic_dir}/{next(self.cycler)}"))

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == "scrolldown":
                for i in range(len(self.pic_list)):
                    next_image = next(self.cycler)
                    if next_image not in self.selected:
                        break
                next_image = f"{self.pic_dir}/{next_image}"
                current_image = self.current_slide
                self.remove_widget(current_image)
                self.add_widget(Image(source=next_image))
                self.load_next()
            elif touch.button == "scrollup":
                self.load_previous()

        if touch.is_double_tap:
            pop_content = Label(text="I'm poppy")
            popup = Popup(content=pop_content, size_hint=(None, None), size=(400, 400))
            self.selected.add(self.current_slide.source.split("/")[1])
            popup.open()

    @staticmethod
    def r_cycle(x):
        while True:
            shuffle(x)
            for element in x:
                yield element


class CarouselApp(App):
    def build(self):
        card_swiper = Root()
        return card_swiper


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    CarouselApp().run()
