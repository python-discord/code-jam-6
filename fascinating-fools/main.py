from functools import partial

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from question import Question, connection

error_sound = SoundLoader.load('sounds/error.wav')
correct_sound = SoundLoader.load('sounds/correct.wav')


class FullWindowImage(Image):
    def __init__(self, **kwargs):
        super(FullWindowImage, self).__init__(**kwargs)
        self.size = self.texture_size  # make the image fill to it's length


class ButtonWithSound(Button):
    def __init__(self, sound_file='sounds/tech-whoosh.wav', **kwargs):
        super(ButtonWithSound, self).__init__(**kwargs)
        self.button_press_sound = SoundLoader.load(sound_file)
        self.category = self.text


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
        # print(f"Inside Second Grid :: Pressed button :> {pressed.text}")
        pressed.button_press_sound.play()
        self.parent.parent.manager.current = 'home_screen'
        self.parent.parent.manager.get_screen(
            'home_screen').category = pressed.text


class ThirdGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(ThirdGridRow, self).__init__(**kwargs)
        self.category_two = ButtonWithSound(text="Medicine", )
        self.category_three = ButtonWithSound(text="Automobiles", )
        self.category_four = ButtonWithSound(text="Music", )
        self.add_widget(self.category_three)
        self.add_widget(self.category_two)
        self.add_widget(self.category_four)
        # Bind the buttons actions to move screens
        self.category_two.bind(on_press=self.handle_category_selection)
        self.category_three.bind(on_press=self.handle_category_selection)
        self.category_four.bind(on_press=self.handle_category_selection)

    def handle_category_selection(self, pressed):
        # print(f"Inside Third Grid :: Pressed button :> {pressed.text}")
        pressed.button_press_sound.play()
        self.parent.parent.manager.current = 'home_screen'
        self.parent.parent.manager.get_screen(
            'home_screen').category = pressed.text


class FourthGridRow(BoxLayout):
    def __init__(self, **kwargs):
        super(FourthGridRow, self).__init__(**kwargs)
        self.category_five = ButtonWithSound(
            text="Food", sound_file='sounds/button-press-whoosh.wav')
        self.category_six = ButtonWithSound(
            text="Aviation", sound_file='sounds/button-press-whoosh.wav')
        self.category_seven = ButtonWithSound(
            text="Telecommunications",
            sound_file='sounds/button-press-whoosh.wav')
        self.add_widget(self.category_five)
        self.add_widget(self.category_six)
        self.add_widget(self.category_seven)
        # Bind the buttons actions to move screens
        self.category_five.bind(on_press=self.handle_category_selection)
        self.category_six.bind(on_press=self.handle_category_selection)
        self.category_seven.bind(on_press=self.handle_category_selection)

    def handle_category_selection(self, pressed):
        # print(f"Inside Fourth Grid :: Pressed button :> {pressed.text}")
        pressed.button_press_sound.play()
        self.parent.parent.manager.current = 'home_screen'
        self.parent.parent.manager.get_screen(
            'home_screen').category = pressed.text


class StartTriviaHomeLayout(Screen):
    def __init__(self, **kwargs):
        super(StartTriviaHomeLayout, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 5
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        # add the background TODO: for some reason distorts the grid
        self.background = Background(source='images/background.jpg',
                                     pos=self.pos,
                                     size=self.size)
        self.layout.add_widget(self.background)
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


class TriviaCategoryScreen(Screen):
    def __init__(self, **kwargs):
        super(TriviaCategoryScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 3
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        self.layout.add_widget(
            Label(text='Ready to go ? Hit start below.', size_hint_x=1))
        # start game for this category
        self.start_button = Button(text='Start', size_hint=[.5, .5])
        self.start_button.bind(on_press=self.press_start_button)
        self.layout.add_widget(self.start_button)
        # go back home
        self.go_back_home = Button(text='Home', size_hint=(.5, .5))
        self.go_back_home.bind(on_press=self.process_go_back_home)
        self.layout.add_widget(self.go_back_home)
        # Add the above layout to this screen
        self.add_widget(self.layout)
        # Initialize the category selected for trivia
        self.category = None
        self.category_questions = None

    def press_start_button(self, pressed):
        # print( f"Inside TriviaCategoryScreen :: Pressed button :> {pressed.text}")
        try:
            self.manager.current = 'play_screen'
            self.manager.get_screen('play_screen').category = self.category
            self.category_questions = Question(self.category).get_questions()
            # Set the question to start , the choices and the correct answer
            self.manager.get_screen(
                'play_screen').question = self.category_questions[0].get(
                    'question')
            self.manager.get_screen(
                'play_screen').category_questions = self.category_questions
            self.manager.get_screen(
                'play_screen').choices = self.category_questions[0].get(
                    'choices').split(',')
            self.manager.get_screen(
                'play_screen').answer = self.category_questions[0].get(
                    'answer')
        except IndexError as e:
            print(f" Error {e}")
            self.manager.current = 'start_page'

    def process_go_back_home(self, pressed):
        # print( f"Inside TriviaCategoryScreen :: Pressed button :> {pressed.text}")
        self.manager.current = 'start_page'

    def on_enter(self):
        pass


class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 5
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        # Initialize the category selected for trivia
        self.category = None
        self.category_questions = []
        self.question = None
        self.choices = []
        self.answer = ''
        self.question_number = 1
        self.runnig_score = 0
        # Question label
        self.question_label = Label(text='')
        self.layout.add_widget(self.question_label)
        # Create answer selections
        self.first_answer = Button(text='')
        self.second_answer = Button(text='')
        self.third_answer = Button(text='')
        self.fourth_answer = Button(text='')
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

    def change_screen(self, screen_to, *args, **kwargs):
        self.manager.current = screen_to

    def check_answer(self, pressed):
        if self.question_number == len(self.category_questions):
            # Also check answer for categories with 1 question or last question for others
            if pressed.text.split(' ', 1)[1].lower().replace(
                    ' ', '') == self.answer.lower().replace(' ', ''):
                # print("Correctly answered the question !")
                # pressed.background_color = (0, 1, 0, .5)
                self.runnig_score += 1
                correct_sound.play()
            else:
                # print("Wrongly answered the question !")
                # pressed.background_color = (1, 0.45, 0, .5)
                error_sound.play()
            # Move to the results screen, dela by 1 second
            Clock.schedule_once(partial(self.change_screen, 'results_screen'),
                                1)
            # Pass the score the results screen
            self.manager.get_screen('results_screen').score = self.runnig_score
            self.manager.get_screen('results_screen').quiz_length = len(
                self.category_questions)
            self.manager.get_screen('results_screen').category = self.category
            # Reset the question number , in case the user restarts the screen
            self.question_number = 1
            # Reset the score
            self.runnig_score = 0
        else:
            # Move to this screen again with refreshed data
            if pressed.text.split(' ', 1)[1].lower().replace(
                    ' ', '') == self.answer.lower().replace(' ', ''):
                # print("Correctly answered the question !")
                self.runnig_score += 1
                correct_sound.play()
            else:
                # print("Wrongly answered the question !")
                error_sound.play()

            # Move to the next question
            self.current_question = self.manager.get_screen(
                'home_screen').category_questions[self.question_number]
            self.question = self.current_question.get('question')
            self.choices = self.current_question.get('choices').split(',')
            self.answer = self.current_question.get('answer')

            self.question_label.text = self.question
            self.first_answer.text = self.choices[0].strip()
            self.second_answer.text = self.choices[1].strip()
            self.third_answer.text = self.choices[2].strip()
            self.fourth_answer.text = self.choices[3].strip()

            # Increment the nth question we are at
            self.question_number += 1

    def on_enter(self):
        self.question_label.text = self.question
        self.first_answer.text = self.choices[0].strip()
        self.second_answer.text = self.choices[1].strip()
        self.third_answer.text = self.choices[2].strip()
        self.fourth_answer.text = self.choices[3].strip()


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = GridLayout()
        self.layout.rows = 5
        self.cols = 1
        self.layout.padding = (200, 0, 200, 100)
        self.layout.spacing = [20, 10]
        # Initiliaze scores
        self.score = 0
        # Initilaise the current player
        self.playing_username = None
        self.rank = None
        self.total_players = None

        self.layout.add_widget(
            Label(text='Quiz complete', font_size=50, size_hint=(1, 1)))
        self.score_label = Label(text="", font_size=40)
        self.layout.add_widget(self.score_label)
        # self.layout.add_widget(
        # Label(text='Personal Best 345 points! Congrats !!', font_size=35))
        # self.layout.add_widget(
        # Label(text='Correct on first attempt is 9/10', font_size=25))
        self.user_name_input = TextInput(
            text="Enter your username (enter when done)!", multiline=False)
        self.layout.add_widget(self.user_name_input)
        self.leader_board_label = Label(font_size=25)
        # Add the leader_board label once the user hits enter on the user_name field
        self.user_name_input.bind(on_text_validate=self.user_name_entered)
        self.restart = Button(text='Restart')
        self.restart.bind(on_press=self.handle_restart)
        self.layout.add_widget(self.restart)
        # Add the above layout to this screen
        self.add_widget(self.layout)

    def handle_restart(self, press):
        # print(f"Press {press}")
        # Go back to the initial screen
        self.manager.current = 'home_screen'

    def on_enter(self, ):
        # print(f"The current score :> {self.score}")
        self.score_label.text = f"Score is {self.score}/ {self.quiz_length}"
        # Update the leaderboard stats
        self.total_players = self.get_total_players(self.category)
        self.rank = self.get_rank(self.playing_username, self.category)
        if self.rank == 0:
            self.rank = self.total_players
        self.leader_board_label.text = f"""
        Hey {self.playing_username} !
        Your rank on the leaderboard is {self.rank} out of {self.total_players}"""

    def get_rank(self, user_name, category):
        rank = 0
        cursor = connection.cursor()
        sql = """SELECT *, RANK() OVER (ORDER BY score DESC)
        output_rank FROM leaderboard WHERE Category = ? ;"""
        params = (category, )
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        for raw_rank in results:
            if raw_rank.get('username') == user_name:
                rank = raw_rank.get('output_rank')
        return rank

    def get_total_players(self, category):
        cursor = connection.cursor()
        sql = 'SELECT COUNT(*) AS total FROM leaderboard WHERE Category = ?;'
        params = (category, )
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        return results[0].get('total')

    def update_user_leaderboard_score(self, user_name, category, new_score):
        cursor = connection.cursor()
        sql = 'SELECT * FROM leaderboard WHERE username = ? AND Category = ?;'
        params = (user_name, category)
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]

        current_score = results[0].get('score')
        if new_score > current_score:
            sql = 'UPDATE leaderboard SET score = ? WHERE username = ? AND Category = ?;'
            params = (new_score, user_name, self.category)
            cursor.execute(sql, params)

    def user_name_entered(self, user_name_input_event):
        try:
            # print( f"{user_name_input_event}, Current player is {self.playing_username}")
            user_name = user_name_input_event.text
            rank = self.get_rank(user_name, self.category)
            self.total_players = self.get_total_players(self.category)
            if self.total_players == 0:
                self.total_players = 1  # First player on this category
            # print( f"Current rank is {rank}, and total players are {self.total_players}")

            if not rank:
                # First time for this user
                cursor = connection.cursor()
                sql = "INSERT INTO leaderboard (username, score, category) VALUES (?, ?, ?);"
                params = (user_name, self.score, self.category)
                cursor.execute(sql, params)
                self.rank = self.total_players
            else:
                # This is a returning player update the score
                # print(f"New score is {self.score}")
                self.update_user_leaderboard_score(user_name, self.category,
                                                   self.score)
                # refresh rank
                self.rank = self.get_rank(user_name, self.category)

            # Delete the current user_name input
            self.layout.remove_widget(self.user_name_input)
            # If the app is not stopped, continue using the current username
            self.playing_username = user_name
            # Add the leaderboard label
            self.leader_board_label.text = f"""
                Hey {self.playing_username} !
            Your rank on the leaderboard is {self.rank} out of {self.total_players}"""
            self.layout.add_widget(self.leader_board_label)
            # Commit current transactions
            connection.commit()
        except Exception as e:
            print(f"Error {e}")


class AncientTriviaApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=FadeTransition())
        screen_manager.add_widget(StartTriviaHomeLayout(name='start_page'))
        screen_manager.add_widget(TriviaCategoryScreen(name='home_screen'))
        screen_manager.add_widget(PlayScreen(name='play_screen'))
        screen_manager.add_widget(ResultsScreen(name='results_screen'))
        return screen_manager


if __name__ == '__main__':
    AncientTriviaApp().run()
