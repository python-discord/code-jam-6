import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget

class DinoMudGame(Widget):
    pass

class DinoMudApp(App):

    def build(self):
        return DinoMudGame()


if __name__ == '__main__':
    DinoMudApp().run()
