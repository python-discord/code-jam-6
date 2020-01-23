from TLOA.core.constants import WINDOW_WIDTH, WINDOW_HEIGHT

# Must be imported before all other kivy imports
from kivy.config import Config


Config.set('graphics', 'width', WINDOW_WIDTH)
Config.set('graphics', 'height', WINDOW_HEIGHT)
Config.set('graphics', 'resizable', False)


def main():
    from TLOA.app import HormonalHedonistsApp

    app = HormonalHedonistsApp()
    app.run()


if __name__ == '__main__':
    main()
