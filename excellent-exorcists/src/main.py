from src.core.game import Game
from src.core.game_loop import GameLoop
from src.core.screen_manager import ScreenManager

from src.screens.game_screen import GameScreen

if __name__ == '__main__':
    loop = GameLoop()
    screen_manager = ScreenManager()
    screen_manager.add_screen(GameScreen)
    screen_manager.set_current_screen(GameScreen)

    loop.start(60)
    game = Game(loop, screen_manager)

    game.run()
