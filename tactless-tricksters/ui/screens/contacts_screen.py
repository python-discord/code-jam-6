# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

# kivymd imports
from kivymd.toolbar import MDToolbar
from kivymd.label import MDLabel
from kivymd.button import MDFloatingActionButton

# project imports
from ui.widgets.contact_card import ContactCard


class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView(do_scroll_x=False, size_hint=(1, None), size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=(dp(12), dp(60)), spacing=dp(5))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' ', size_hint=(1, 5)))

        for contact in self.util.contact_list:
            contact_card = ContactCard(util=self.util,
                                       contact=contact
                                       )
            scroll_box.add_widget(contact_card)

        scroll.add_widget(scroll_box)
        layout.add_widget(scroll)

        # Add floating action button to write messages
        add_contact_anchor = AnchorLayout(anchor_x='right', anchor_y='bottom',
                                            padding=[dp(25), dp(25), dp(25), dp(25)])
        add_contact_btn = MDFloatingActionButton(icon='account-plus', size=[dp(56), dp(56)])
        add_contact_btn.md_bg_color = App.get_running_app().theme_cls.primary_color
        add_contact_btn.theme_text_color = "Custom"
        add_contact_btn.text_color = [1, 1, 1, 1]
        add_contact_btn.bind(on_press=lambda x: self.change_screen('add_contact'))
        add_contact_anchor.add_widget(add_contact_btn)
        self.add_widget(add_contact_anchor)

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title='Contacts', anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.change_screen('message')]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(layout)
        self.add_widget(toolbar_anchor)

        self.do_layout()

    def change_screen(self, screen):
        self.manager.current = screen

