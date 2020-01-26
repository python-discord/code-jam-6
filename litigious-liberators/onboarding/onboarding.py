from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial

lorem = ""
sentences = [
    "It's the year 12020 CE...",
    """Civilization has fallen, after the humans caused their own demise as they tried to"""
    """ interfere with the natural order of things thousands of years ago """,
    """Experiments with the prehistoric animal DNA, race to the ultimate doomsday"""
    """ weapon and the total neglect of Global Warming...""",
    "Today, flora and fauna from all ages flourish, treading the ruins of an ancient civilization.",
    """Some humans survived against all odds, striving to rebuild what was lost,"""
    """ but without lost knowledge and wisdom it seems hopeless.""",
    """You are one of these humans. Will you be the one, cunning and smart enough to tip"""
    """ the scales or will your ignorant careless attitude ruin everything?""",
    "Only time will tell.",
]
# images = [
#     "https://placekitten.com/g/1080/1920",
#     "https://placekitten.com/g/200/300",
#     "https://placekitten.com/g/300/400",
# ]

images = ["onboarding/intro_img_crop.jpg"]


class MyOnboardWidget(FloatLayout):
    steps = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = 0
        # for index, image_url in enumerate(images):
        #     image_object = AsyncImage(source=image_url, size_hint=(1, 1))
        #     image_object.opacity = 1 if index == 0 else 0
        #     setattr(self, f"image_{index}", image_object)
        #     self.add_widget(image_object)

        for index, sentence in enumerate(sentences):
            label_object = Label(
                text=sentence,
                text_size=(self.width * 4, None),
                pos_hint={"center_x": 0.50, "center_y": 0.5},
                color=[1, 1, 1, 1],
                valign="center",
                # align="middle",
                font_size="35sp",
                font_name="delinquent-black-font/DelinquentExtract-V4we.ttf",
                # text_size=(400, 600),
            )
            # label_object.opacity = 1 if index == 0 else 0
            label_object.opacity = 0
            setattr(self, f"description_{index}", label_object)
            self.add_widget(label_object)

    def animate(self, obj_out, obj_in, opacity, *args):
        appear = Animation(opacity=1, duration=1)
        disappear = Animation(opacity=opacity, duration=1)
        appear.start(obj_in)
        disappear.start(obj_out)

    def on_touch_down(self, touch):
        if self.steps == 0:
            Clock.schedule_once(
                partial(
                    self.animate, self.parent.ids["bg_img"], getattr(self, f"description_0"), 0.2
                ),
                0.5 + 0 * 5,
            )
            speed = 15
            delay = len(sentences[0]) / speed + 1
            for index, sentence in enumerate(sentences[1:], start=1):
                # print(index, sentence)
                # print(getattr(self, f"description_{index - 1}"))
                # print(getattr(self, f"description_{index}"))

                Clock.schedule_once(
                    partial(
                        self.animate,
                        getattr(self, f"description_{index-1}"),
                        getattr(self, f"description_{index}"),
                        0,
                    ),
                    1 + delay,
                )
                delay += len(sentence) / speed
        if touch.is_double_tap:
            self.parent.manager.current = "create_profile"

        self.steps += 1

        return True


class OnboardingScreen(Screen):
    pass


class CreateProfileTest(Screen):
    pass


class OnboardingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(CreateProfileTest(name="create_profile"))
        return sm


if __name__ == "__main__":
    OnboardingApp().run()


# def ola():
#     print("HELLLOOO")
#
#
# class CarouselApp(App):
#     def build(self):
#        #  carousel = Carousel(direction="right", loop=True)
#        #  src = "https://placekitten.com/g/1080/1920"
#        #  src_1 = "https://placekitten.com/g/1080/1920"
#        #  image = AsyncImage(source=src)
#        #  image1 = AsyncImage(source=src_1)
#        #  carousel.add_widget(image)
#        #  carousel.add_widget(image1)
#        #  return carousel
#
#
# CarouselApp().run()
