# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp

# kivymd imports
from kivymd.toolbar import MDToolbar
from kivymd.label import MDLabel
from kivymd.textfields import MDTextFieldRound

# project imports
from ui.widgets.conversation_bubble import ConversationBubble


class ConversationScreen(Screen):
    def __init__(self, **kwargs):
        super(ConversationScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout('Bob')

    def ui_layout(self, contact):
        self.clear_widgets()
        self.update_nav_bar(contact)

        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView(do_scroll_x=False, size_hint=(1, None), size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=(dp(12), dp(60)), spacing=dp(5))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' ', size_hint=(1, 5)))

        for message in self.util.message_dict[contact]['messages']:
            if self.util.user_name == message['author']:
                pos_hint = {'center_x': 0.3}
                md_bg_color = [0.698, 0.875, 0.859, 1]
                text_color = [0, 0, 0, 1]
            else:
                pos_hint = {'center_x': 0.7}
                md_bg_color = [1, 1, 1, 0.6]
                text_color = [0, 0, 0, 1]
            message_label = MDLabel(text=message['text'], font_style='Caption', size_hint=(1, None))

            message_card = ConversationBubble(util=self.util,
                                              size=message_label.size,
                                              message=message_label,
                                              pos_hint=pos_hint,
                                              md_bg_color=md_bg_color,
                                              text_color=text_color)
            scroll_box.add_widget(message_card)

        scroll.add_widget(scroll_box)
        layout.add_widget(scroll)

        text_input_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        self.text_input = MDTextFieldRound()
        # Hides left icon
        self.text_input.children[2].children[2].size = (0, 0)
        self.text_input.icon_right = 'send'
        self.text_input.children[2].children[0].bind(on_press=lambda x: self.send_message(self.text_input.text))
        text_input_anchor.add_widget(self.text_input)

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title=contact, anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.return_screen()]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(layout)
        self.add_widget(text_input_anchor)
        self.add_widget(toolbar_anchor)

        self.do_layout()

    def send_message(self, msg):
        print("Sending message:%s" % msg)
        self.text_input.text = ''

    def update_nav_bar(self, contact):
        app = App.get_running_app().root
        if hasattr(app, 'nav_bar'):
            toolbar = app.nav_bar.toolbar
            toolbar.title = contact
            toolbar.left_action_items = [['arrow-left', lambda x: self.return_screen()]]

    def return_screen(self):
        self.manager.current = 'message'

