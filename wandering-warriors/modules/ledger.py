from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import functools

BLANK_ROW = functools.partial(Widget)
ROWS_IN_LEDGER = 10  # TODO: make this dependent on height


class LedgerLayout(BoxLayout):
    child_widgets: list

    def __init__(self, *args, **kwargs):
        super(LedgerLayout, self).__init__(
                *args,
                orientation='vertical',
                **kwargs
        )

        self.child_widgets = []

        # initialize with blank rows
        for _ in range(ROWS_IN_LEDGER):
            self.add_widget(BLANK_ROW())

    def add_widget(self, widget, *args, **kwargs):
        if ROWS_IN_LEDGER == len(self.child_widgets):
            super(LedgerLayout, self).remove_widget(self.child_widgets[0])
            self.child_widgets = self.child_widgets[1:]

        super(LedgerLayout, self).add_widget(widget, *args, **kwargs)
        self.child_widgets.append(widget)

    def click(self):
        print('click')

    def buttonImage(self):
        return 'assets/graphics/clay.png'
