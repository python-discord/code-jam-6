from kivy.uix.widget import Widget
from kivy.uix.image import Image


class OperationsLayout(Widget):
    def button_image(self, operation: str) -> str:
        return f'assets/graphics/{operation}.png'

    def send_operation(self, operation: str) -> None:
        img_source = self.button_image(operation)
        self.parent.children[2].add_middle(Image(source=img_source))
