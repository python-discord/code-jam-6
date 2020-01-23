from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader


class FullWindowImage(Image):
    def __init__(self, **kwargs):
        super(FullWindowImage, self).__init__(**kwargs)
        self.size = self.texture_size  # make the image fill to it's length


class ComputingTriviaLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ComputingTriviaLayout, self).__init__(**kwargs)
        self.cols = 4
        self.test_label = Label(text='Test for content in computing')
        self.add_widget(self.test_label)


class MedicineTriviaLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MedicineTriviaLayout, self).__init__(**kwargs)
        self.cols = 4
        self.add_widget(Label(text='Test for content in medicine'))


class ButtonWithSound(Button):
    def __init__(self, sound_file, **kwargs):
        super(ButtonWithSound, self).__init__(**kwargs)
        self.button_press_sound = SoundLoader.load(sound_file)
        self.category = self.text
        self.category_map = {
            "Computing": ComputingTriviaLayout(),
            "Medicine": MedicineTriviaLayout()
        }

    def on_press(self):
        self.button_press_sound.play()
        # switch window to the category clicked
        print(f"Selected category {self.category}")
        category_widget = self.category_map.get(self.category)
        self.parent.add_widget(category_widget)


class Background(Widget):
    def __init__(self, source, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.image = FullWindowImage(source=source)
        self.add_widget(self.image)
        self.size = self.image.size


class FirstGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(FirstGridRow, self).__init__(**kwargs)
        self.padding = (0, 0, 0, 50)
        self.file_menu = Button(font_size=40, text="File", size_hint=(.2, .2))
        self.add_widget(self.file_menu)
        self.help_menu = Button(font_size=40, text="Help", size_hint=(.2, .2))
        self.add_widget(self.help_menu)
        self.file_fullscreen = Button(font_size=40,
                                      text="Fullscreen",
                                      size_hint=(.2, .2))
        self.add_widget(self.file_fullscreen)


class SecondGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(SecondGridRow, self).__init__(**kwargs)
        self.intro_holder = BoxLayout()
        self.intro_holder.add_widget(
            Image(source='sample-logo.png', size_hint=(.3, 1)))
        self.intro_holder.add_widget(
            Label(text="Welcome to the Ancient Trivia Tech.",
                  font_size=30,
                  size_hint=(.7, 1)))
        self.add_widget(self.intro_holder)
        self.category_one = ButtonWithSound(
            text="Computing",
            size_hint=(.3, 1),
            sound_file='sounds/button-press-whoosh.wav',
        )
        self.add_widget(self.category_one)


class ThirdGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(ThirdGridRow, self).__init__(**kwargs)
        self.category_two = ButtonWithSound(
            text="Medicine", sound_file="sounds/button-press-whoosh.wav")
        self.category_three = ButtonWithSound(
            text="Automobiles", sound_file='sounds/tech-whoosh.wav')
        self.category_four = Button(text="Music")
        self.add_widget(self.category_three)
        self.add_widget(self.category_two)
        self.add_widget(self.category_four)


class FourthGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(FourthGridRow, self).__init__(**kwargs)
        self.category_five = Button(text="Food")
        self.category_six = Button(text="Construction")
        self.category_seven = Button(text="Telecommunications")
        self.add_widget(self.category_five)
        self.add_widget(self.category_six)
        self.add_widget(self.category_seven)


class StartTriviaHomeLayout(GridLayout):
    def __init__(self, **kwargs):
        super(StartTriviaHomeLayout, self).__init__(**kwargs)
        self.rows = 4
        self.padding = (200, 0, 200, 100)
        self.spacing = [20, 10]
        # add the background TODO: for some reason distorts the grid
        # self.background = Background(source='background.jpg')
        # self.add_widget(self.background)
        # first row
        self.first_grid = FirstGridRow()
        self.add_widget(self.first_grid)
        # second row
        self.second_grid = SecondGridRow()
        self.add_widget(self.second_grid)
        # third row
        self.third_grid = ThirdGridRow()
        self.add_widget(self.third_grid)
        # fourth row
        self.fourth_grid = FourthGridRow()
        self.add_widget(self.fourth_grid)


class AncientTriviaApp(App):
    def build(self):
        return StartTriviaHomeLayout()


if __name__ == '__main__':
    AncientTriviaApp().run()
