from project.core.game import Game

from kivy.app import App


class HormonalHedonistsApp(App):
    def build(self):
        return Game()
