from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock

lorem = ""
sentences = [
    "It's the year 12020 CE.....",
    """Civilization has fallen, after humans caused their own demise as they tried to
    interfere with the natural order of things thousands of years ago """,
    """Experiments with prehistoric animals DNA, race to the ultimate doomsday's
    weapon and total neglect of the Global Warming...""",
    "Today, flora and fauna from all ages flourish, treading the ruins of an ancient civilization.",
    """Some humans survived against all odds, striving to rebuild what was lost,
    but without lost knowledge and wisdom it seems hopeless.""",
    """You are one of these humans. Will you be the one cunning and smart enough to tip
    the scales or will your ignorance careless attitude ruin everything?""",
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

        # self.add_widget(
        #     Label(
        #         text="Welcome to DinoTinder",
        #         pos_hint={"center_x": 0.40, "center_y": 0.8},
        #         color=[1, 0, 0, 1],
        #         halign="left",
        #         valign="middle",
        #         font_size="25sp",
        #         font_name="delinquent-black-font/DelinquentCapsSkewdBlack-q2wq.ttf"
        #     )
        # )

    def animate(self, obj_out, obj_in, opacity=0):
        appear = Animation(opacity=1, duration=1)
        disappear = Animation(opacity=opacity, duration=1)
        appear.start(obj_in)
        disappear.start(obj_out)

    def on_touch_down(self, touch):
        # print(self.parent.ids)
        Clock.schedule_once(
            lambda dt: self.animate(
                obj_out=self.parent.ids["bg_img"],
                obj_in=getattr(self, "description_0"),
                opacity=0.2,
            ),
            2,
        )
        for index, sentence in enumerate(sentences[1:], start=1):
            print(index, sentence)
            Clock.schedule_once(
                lambda dt: self.animate(
                    obj_out=getattr(self, f"description_{index-1}"),
                    obj_in=getattr(self, f"description_{index}"),
                ),
                2 + index * 10,
            )

        # Clock.schedule_once(lambda dt: self.animate(obj_out=self.parent.ids['bg_img'],
        # obj_in=self.description_0),2)
        # Clock.schedule_once(lambda dt:self.animate(obj_out=self.description_0, obj_
        # in=self.description_1), 10)
        # Clock.schedule_once(lambda dt:self.animate(obj_out=self.image_1, obj_in=self.image_2), 20)
        # Clock.schedule_once(lambda dt:self.animate(obj_out=self.description_1,
        # obj_in=self.description_2), 30)
        if touch.is_double_tap:
            self.parent.manager.current = "create_profile"
        # if self.steps == 0:
        #     self.animate(obj_out=self.image_0, obj_in=self.image_1)
        #     self.animate(obj_out=self.description_0, obj_in=self.description_1)
        # if self.steps == 1:
        #     self.animate(obj_out=self.image_1, obj_in=self.image_2)
        #     self.animate(obj_out=self.description_1, obj_in=self.description_2)

        self.steps += 1
        if self.steps > 2:
            self.parent.manager.current = "create_profile"
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
