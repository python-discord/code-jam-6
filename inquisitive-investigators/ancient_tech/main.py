from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout


# Float Layout Documentation
# https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html
class Main(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Grabs reference of ID and calls text element
        print(self.test.text)


# App Documentation
# https://kivy.org/doc/stable/api-kivy.app.html?highlight=app#module-kivy.app
class AncientTechApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
