from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class MainWidget(Widget):
    pass


class CardWidget(FloatLayout):
    text = StringProperty()
    source = StringProperty()


class myApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    myApp().run()
