from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.carousel import Carousel
from os import listdir
from kivy.animation import Animation
from functools import partial
from kivy.clock import Clock
from random import shuffle
from copy import deepcopy


class Root(BoxLayout):
    swiper_obj = ObjectProperty(None)


class Swiper(Carousel):
    card_one = ObjectProperty()
    card_two = ObjectProperty()
    card_three = ObjectProperty()

    def __init__(self,**kwargs):
        super(Swiper,self).__init__(**kwargs)
        self.static_pic_list = listdir("pictures")
        self.pic_list = deepcopy(self.static_pic_list)
        shuffle(self.pic_list)

    def shuffle_cards(self,pic_id):
        self.current_slide.source = f"pictures/{self.pic_list.pop(pic_id)}"
        if len(self.pic_list) == 0:
            self.pic_list = deepcopy(self.static_pic_list)
        shuffle(self.pic_list)
        print(self.pic_list)
        self.previous_slide.source = f"pictures/{self.pic_list[0]}"
        self.previous_slide.pic_id = 0
        self.next_slide.source = f"pictures/{self.pic_list[-1]}"
        self.next_slide.pic_id = -1

    def on_index(self, *args):
        print("ON INDEX")
        print(self._offset)
        print("BEFORE", self.current_slide.source)
        super(Swiper,self).on_index(self,*args)
        print("AFTER", self.current_slide.source, self.current_slide.pic_id)
        self.shuffle_cards(self.current_slide.pic_id)
        print(self.previous_slide.source)
        print(self.next_slide.source)

class CarouselApp(App):
    def build(self):
        card_swiper = Root()
        card_swiper.swiper_obj.shuffle_cards(-1)
        return card_swiper


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    CarouselApp().run()