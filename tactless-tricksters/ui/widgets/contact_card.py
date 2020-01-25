from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel


class ContactCard(ButtonBehavior, MDCard):
    def __init__(self, **kwargs):
        super(ContactCard, self).__init__(orientation='horizontal',
                                          size_hint=(1, None),
                                          height=dp(90),
                                          pos_hint={'center_x': 0.5},
                                          padding=(dp(5), dp(1))
                                          )

        self.contact = kwargs.get('contact')
        # Gather first character of contact to get icon cef
        first_char = self.contact[0]
        if first_char.isdigit():
            icon_name = 'numeric-%s-circle-outline' % first_char
        else:
            icon_name = 'alpha-%s-circle' % first_char.lower()
        icon = MDIcon(icon=icon_name)
        icon.theme_text_color = 'Custom'
        icon.text_color = [1, 1, 1, 1]
        icon.font_size = 60
        self.add_widget(icon)

        # Create name Label
        contact_label = MDLabel(text=self.contact, font_style='H3')
        contact_label.theme_text_color = 'Custom'
        contact_label.text_color = [1, 1, 1, 1]
        self.add_widget(contact_label)
        self.add_widget(Widget())
        self.add_widget(Widget())
        self.add_widget(Widget())

        # Create message Icon
        message_icon = MDIcon(icon='message')
        message_icon.theme_text_color = 'Custom'
        message_icon.text_color = [1, 1, 1, 1]
        message_icon.font_size = 60
        self.add_widget(message_icon)

    def on_press(self):
        for screen in App.get_running_app().root.content.screens:
            if screen.name == 'conversation':
                screen.ui_layout(self.contact)
        App.get_running_app().root.content.current = 'conversation'







