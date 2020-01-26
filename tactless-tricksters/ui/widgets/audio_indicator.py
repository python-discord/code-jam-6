from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.card import MDCard


class AudioIndicator(BoxLayout):
    def __init__(self, stack_width=10, stack_height=10, **kwargs):
        super(AudioIndicator, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.stack_width = stack_width
        self.stack_height = stack_height
        self.padding = dp(2)
        self.spacing = dp(2)
        self.stack_array = []

        # Creates columns of stacks
        for i in range(self.stack_width):
            stack = AudioIndicatorStack()
            self.stack_array.append(stack)
            self.add_widget(stack)

    def set_levels(self, level_array):
        # step through each element of the array
        # and turn the background color on or off
        for column in range(self.stack_width):
            for rect in range(self.stack_height):
                temp_stack = self.stack_array[column]
                current_card = temp_stack.rect_array[rect]
                if level_array[column] < rect:
                    # Set color to primary color theme
                    current_card.md_bg_color = App.get_running_app().theme_cls.primary_color
                else:
                    # Set color to none
                    current_card.md_bg_color = [0, 0, 0, 0]


class AudioIndicatorStack(BoxLayout):
    def __init__(self, stack_height=10):
        super(AudioIndicatorStack, self).__init__()
        self.orientation = 'vertical'
        self.padding = dp(2)
        self.spacing = dp(2)
        self.rect_array = []
        self.stack_height = stack_height
        self.color_tuple = [App.get_running_app().theme_cls.primary_color, [0, 0, 0, 0]]

        # Builds a stack of rectangle box layouts
        for i in range(self.stack_height):
            rect = MDCard(size_hint=(1, 1))
            rect.md_bg_color = App.get_running_app().theme_cls.primary_color
            self.rect_array.append(rect)
            self.add_widget(rect)
