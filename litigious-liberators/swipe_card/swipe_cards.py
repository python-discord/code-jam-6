from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
import os
from os import listdir
from random import shuffle
from copy import deepcopy


class Root(BoxLayout):
    swiper_obj = ObjectProperty(None)


class Swiper(Carousel):
    def __init__(self, **kwargs):
        super(Swiper, self).__init__(**kwargs)
        self.static_pic_list = listdir(os.path.dirname(os.path.abspath(__file__)) + "/pictures")
        self.pic_list = deepcopy(self.static_pic_list)
        shuffle(self.pic_list)

    def shuffle_cards(self, pic_id):
        self.current_slide.source = f"pictures/{self.pic_list.pop(pic_id)}"
        if len(self.pic_list) == 0:
            self.pic_list = deepcopy(self.static_pic_list)
        shuffle(self.pic_list)
        self.previous_slide.source = f"pictures/{self.pic_list[0]}"
        self.previous_slide.pic_id = 0
        self.next_slide.source = f"pictures/{self.pic_list[-1]}"
        self.next_slide.pic_id = -1

    def on_index(self, *args):
        super(Swiper, self).on_index(self, *args)
        self.shuffle_cards(self.current_slide.pic_id)


class CarouselApp(App):
    def build(self):
        card_swiper = Root()
        card_swiper.swiper_obj.shuffle_cards(-1)
        return card_swiper


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    CarouselApp().run()
