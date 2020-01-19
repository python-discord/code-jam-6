from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage


def ola():
    print("HELLLOOO")


class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction="right", loop=True)
        src = "https://placekitten.com/g/1080/1920"
        src_1 = "https://placekitten.com/g/1080/1920"
        image = AsyncImage(source=src)
        image1 = AsyncImage(source=src_1)
        carousel.add_widget(image)
        carousel.add_widget(image1)
        return carousel


CarouselApp().run()
