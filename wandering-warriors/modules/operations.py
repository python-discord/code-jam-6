from kivy.uix.widget import Widget
from kivy.uix.image import Image
from .ledger import LedgerLayout


class OperationsLayout(Widget):
    def button_image(self, operation: str) -> str:
        return f'assets/graphics/{operation}.png'

    def send_operation(self, operation: Image) -> None:
        LedgerLayout.add_middle(operation)
