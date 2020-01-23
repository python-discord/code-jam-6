from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
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
        self.category_one.bind(on_press=self.handle_category_selection)
        self.add_widget(self.category_one)

    def handle_category_selection(self, pressed):
        print(f"{pressed}")
        pressed.button_press_sound.play()
        self.parent.parent.manager.current = 'home_screen'


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


class StartTriviaHomeLayout(Screen):
    def __init__(self, **kwargs):
        super(StartTriviaHomeLayout, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 4
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        # add the background TODO: for some reason distorts the grid
        # self.background = Background(source='background.jpg')
        # self.layout.add_widget(self.background)
        # first row
        self.first_grid = FirstGridRow()
        self.layout.add_widget(self.first_grid)
        # second row
        self.second_grid = SecondGridRow()
        self.layout.add_widget(self.second_grid)
        # third row
        self.third_grid = ThirdGridRow()
        self.layout.add_widget(self.third_grid)
        # fourth row
        self.fourth_grid = FourthGridRow()
        self.layout.add_widget(self.fourth_grid)

        # Add the above layout to this screen
        self.add_widget(self.layout)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 2
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        self.layout.add_widget(Label(text='Ready to go ? Hit start below.'))
        self.start_button = Button(text='Start')
        self.start_button.bind(on_press=self.press_start_button)
        self.layout.add_widget(self.start_button)
        # Add the above layout to this screen
        self.add_widget(self.layout)

    def press_start_button(self, touch):
        print(f"{touch.__dict__}")
        self.manager.current = 'play_screen'


class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 5
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        self.layout.add_widget(
            Label(text='Which of these is an East African country?'))
        # Create answer selections
        self.first_answer = Button(text='A: Kenya')
        self.second_answer = Button(text='B: Hawaii')
        self.third_answer = Button(text='C: USA')
        self.fourth_answer = Button(text='D: Mauritius')
        # Bind the actions
        self.first_answer.bind(on_press=self.check_answer)
        self.second_answer.bind(on_press=self.check_answer)
        self.third_answer.bind(on_press=self.check_answer)
        self.fourth_answer.bind(on_press=self.check_answer)

        # Add to the screen
        self.layout.add_widget(self.first_answer)
        self.layout.add_widget(self.second_answer)
        self.layout.add_widget(self.third_answer)
        self.layout.add_widget(self.fourth_answer)
        # Add the above layout to this screen
        self.add_widget(self.layout)

    def check_answer(self, press):
        print(f"{press}- Selected answer {press.text}")
        # If this is the last question then switch to the last
        self.manager.current = 'results_screen'


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 5
        self.cols = 1
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        self.layout.add_widget(
            Label(text='Quiz complete', font_size=50, size_hint=(1, 0)))
        self.layout.add_widget(Label(text='Score: 340', font_size=40))
        self.layout.add_widget(
            Label(text='Personal Best 345 points! Congrats !!', font_size=35))
        self.layout.add_widget(
            Label(text='Correct on first attempt is 9/10', font_size=25))
        self.layout.add_widget(
            Label(text='Your rank on the Leaderboard is 1 out of 100',
                  font_size=25))
        self.restart = Button(text='Restart')
        self.restart.bind(on_press=self.handle_restart)
        self.layout.add_widget(self.restart)
        # Add the above layout to this screen
        self.add_widget(self.layout)

    def handle_restart(self, press):
        print(f"Press {press}")
        # Go back to the initial screen
        self.manager.current = 'home_screen'


class AncientTriviaApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=FadeTransition())
        screen_manager.add_widget(StartTriviaHomeLayout(name='start_page'))
        screen_manager.add_widget(MenuScreen(name='home_screen'))
        screen_manager.add_widget(PlayScreen(name='play_screen'))
        screen_manager.add_widget(ResultsScreen(name='results_screen'))
        return screen_manager


if __name__ == '__main__':
    AncientTriviaApp().run()
