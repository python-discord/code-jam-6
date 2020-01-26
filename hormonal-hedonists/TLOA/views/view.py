import math

from random import randint

from TLOA.core.game import Game
from TLOA.core.constants import (ATLAS_PATH, IMAGES_PATH, KEY_MAPPING, WINDOW_WIDTH, FONT_PATH,
                                 WINDOW_HEIGHT, LANE_BOUNDS)
from TLOA.entities import BrownShip
from TLOA.views import ShipView, PauseMenuView

from kivy import Logger
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore


class GameView(Widget):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)

        self.store = JsonStore('Hi-Score.json')
        if not self.store.exists('hi-score'):
            self.store.put('hi-score', score=0)

        self._game = game
        self.pause_menu_content = PauseMenuView()

        game.mirror.bind(state=self.on_mirror_state_change)
        game.bind(running=lambda _, value: self.show_game(value))
        game.bind(score=self.on_score_change)
        game.bind(health=self.on_island_health_change)
        game.bind(on_add_ship=self.on_add_ship)
        game.bind(on_remove_ship=self.on_remove_ship)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.pause_menu_content.button_resume.bind(on_release=self.close_pause_menu)
        self.pause_menu_content.button_main_menu.bind(on_release=self.show_main_menu)
        self.pause_menu_content.button_exit.bind(on_release=self.exit_game)

        self._background = Image(
            source=IMAGES_PATH.format('background.zip'),
            anim_delay=1
        )
        self._background.size = self._background.texture_size

        self._hp_bar = Image(pos=(10, WINDOW_HEIGHT - 80), source=ATLAS_PATH.format('100'))
        self._hp_bar.size = self._hp_bar.texture_size

        self._score = Label(pos=(950, 700), text=f'Score:   0', font_size=75)

        self.pause_menu_opened = False

        self.pause_menu = Popup(
            title='Pirate ships are on hold...',
            title_size='20sp',
            title_align='center',
            title_color=(1, 0.1, 0.1, 1),
            title_font=FONT_PATH.format('Pacifico-Regular.ttf'),
            content=self.pause_menu_content,
            separator_color=(0, 0, 0, 0),
            separator_height=0,
            size_hint=(None, None),
            size=(300, 280),
            auto_dismiss=False,
            background=IMAGES_PATH.format('yellow_panel.png')
        )

        self.pause_btn = Button(
            background_normal=IMAGES_PATH.format('ui_pause.png'),
            background_down=IMAGES_PATH.format('ui_pause_click.png'),
            border=(0, 0, 0, 0),
            pos=((WINDOW_WIDTH / 3) + 85, WINDOW_HEIGHT - 65),
            width=35,
            height=35,
            on_release=self.open_pause_menu
        )

    def show_main_menu(self, *args):
        self.pause_menu.dismiss()
        self.pause_menu_opened = True
        self.canvas.clear()
        self.clear_widgets()
        self._game = Game()
        self.__init__(self._game)
        self._game.start()

    @staticmethod
    def exit_game(*args):
        App.get_running_app().stop()

    def open_pause_menu(self, *args):
        self.pause_menu.open()
        self.pause_menu_opened = True
        self._game.pause_game = True

    def close_pause_menu(self, *args):
        self.pause_menu.dismiss()
        self.pause_menu_opened = False
        self._game.pause_game = False

    def show_game(self, running):
        Animation.cancel_all(self)
        self.canvas.clear()

        if not running:
            return

        self.add_widget(self._background)
        with self.canvas:
            # Load & configure the flock of bird animation frames
            birds = Image(
                source=IMAGES_PATH.format('birds.zip'),
                pos=(Window.width, 400),
                anim_delay=1
            )
            birds.size = birds.texture_size

            # Setup the flock of birds to move in wave pattern
            up_down = (Animation(y=375, d=5, t=self._sin_transition) +
                       Animation(y=425, d=5, t=self._sin_transition))
            up_down.repeat = True
            bird_animation = Animation(x=-birds.width, d=30) & up_down
            bird_animation.start(birds)
            bird_animation.bind(on_complete=self.on_birds_complete)

            # Initialize and draw the Mirror Cannon onto the canvas based on its state
            self._game.mirror.shape = Image(
                pos=(150, 260),
                source=ATLAS_PATH.format(f'{self._game.mirror.id}-{self._game.mirror.state}')
            )
            self._game.mirror.shape.size = self._game.mirror.shape.texture_size

            # Change the color and display the incident
            # sun rays on the canvas
            self.canvas.add(self._game.sun_rays.color)
            self.canvas.add(self._game.sun_rays)

            # Change the color and display the death sun rays on the canvas
            self.canvas.add(self._game.death_rays.color)
            self.canvas.add(self._game.death_rays)

        # Add the Health Bar for the Castle/Island
        self.add_widget(self._hp_bar)

        # Add the Score display
        self.add_widget(self._score)
        self.add_widget(self.pause_btn)

    def on_island_health_change(self, _game: Game, health: int):
        health = math.ceil(health / 10) * 10
        self._hp_bar.source = ATLAS_PATH.format(health)

    def on_add_ship(self, _game: Game, ship: BrownShip):
        ship.shape = ShipView(
            ship,
            source=ATLAS_PATH.format(ship.id),
            pos=(WINDOW_WIDTH, LANE_BOUNDS[ship.lane_id][1])
        )
        ship.bind(on_launch_cannon_ball=self.on_launch_cannon_ball)
        self.add_widget(ship.shape)
        self.redraw_ships(redraw_to=ship.lane_id)

    def on_remove_ship(self, game: Game, ship: BrownShip):
        ship.shape.clear_widgets()
        self.remove_widget(ship.shape)
        game.score += 1
        if self.store.get('hi-score')['score'] < game.score:
            self.store.put('hi-score', score=game.score)

    def redraw_ships(self, redraw_to=0):
        for lane in self._game.ship_lanes[:redraw_to]:
            for ship in lane:
                self.remove_widget(ship.shape)

        for lane in self._game.ship_lanes[:redraw_to][::-1]:
            for ship in lane:
                self.add_widget(ship.shape)

        #self.canvas.add(self._game.death_rays.color)
        #self.canvas.add(self._game.death_rays)

    @staticmethod
    def _sin_transition(progress: float):
        return math.sin(progress * math.pi)

    @staticmethod
    def on_birds_complete(animation, birds):
        birds.pos = (Window.width, 500)
        delay = randint(10, 30)
        Clock.schedule_once(lambda dt: animation.start(birds), delay)

    @staticmethod
    def on_mirror_state_change(mirror, value: int):
        mirror.shape.source = ATLAS_PATH.format(f'{mirror.id}-{value}')

    def on_launch_cannon_ball(self, ship):
        x, y = ship.shape.pos
        cannon_ball = Image(source=IMAGES_PATH.format('fire.zip'), pos=(x + 50, y + 50))
        cannon_ball.size = cannon_ball.texture_size

        self.add_widget(cannon_ball)
        arc_animation = Animation(x=10, y=475, d=3)
        arc_animation.bind(on_complete=self.on_cannon_ball_complete)
        arc_animation.start(cannon_ball)

        return True

    def on_cannon_ball_complete(self, animation, image):
        self.remove_widget(image)
        self._game.health -= 10
        if self._game.health <= 0:
            self.pause_menu.title = 'Is the mirror working right?'
            self.pause_menu_content.game_over = True
            self.pause_menu_content.remove_widget(self.pause_menu_content.button_resume)
            self.open_pause_menu()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, _keyboard, key_code, _text, _modifiers):
        action = KEY_MAPPING.get(key_code[1])
        if key_code[1] == 'escape' and not self.pause_menu_opened:
            self.open_pause_menu()
        elif key_code[1] == 'escape' \
                and self.pause_menu_opened \
                and self.pause_menu_content.game_over is False:
            self.close_pause_menu()

        if action is None:
            return True

        return self._game.process_action(action)

    def on_score_change(self, _game: Game, score: int):
        Logger.debug(f'New score: {score}')
        self._score.text = f'Score: {score:3}'
