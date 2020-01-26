# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound

# project imports
from ui.widgets.conversation_bubble import ConversationBubble
from ui.widgets.long_press_button import LongpressButton


class ConversationScreen(Screen):
    def __init__(self, **kwargs):
        super(ConversationScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.contact = ''
        self.ui_layout('')

    def ui_layout(self, contact):
        self.contact = contact
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView(do_scroll_x=False,
                            size_hint=(1, None),
                            size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical',
                               size_hint_y=None,
                               padding=(dp(12), dp(60)),
                               spacing=dp(5))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' ', size_hint=(1, 5)))

        if contact != '' and contact in self.util.user_data['message_dict'].keys():
            for message in self.util.user_data['message_dict'][contact]:
                if self.util.username != message['sender']:
                    pos_hint = {'center_x': 0.3}
                    md_bg_color = [0.698, 0.875, 0.859, 1]
                    text_color = [0, 0, 0, 1]
                else:
                    pos_hint = {'center_x': 0.7}
                    md_bg_color = [1, 1, 1, 0.6]
                    text_color = [0, 0, 0, 1]
                message_label = MDLabel(text=message['message'], font_style='Caption', size_hint=(1, None))
                if '_' not in message_label.text:
                    self.util.morse.read(words=str(message_label.text))
                    message_label.text = self.util.morse.morse
                message_card = ConversationBubble(util=self.util,
                                                  size=message_label.size,
                                                  message=message_label,
                                                  pos_hint=pos_hint,
                                                  md_bg_color=md_bg_color,
                                                  text_color=text_color)
                scroll_box.add_widget(message_card)

        # This is disgusting but its late and I'm running out of time
        # keeps the text off of the text input
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))

        scroll.add_widget(scroll_box)
        layout.add_widget(scroll)


        self.text_input = MDTextFieldRound()
        # Hides left icon
        self.text_input.children[2].children[2].size = (0, 0)
        self.text_input.icon_right = 'send'
        self.text_input.children[2].children[0].bind(
            on_press=lambda x: self.send_message(self.text_input.text))

        self.long_press_btn = LongpressButton(text_input_cb=self.text_input_cb, size=(dp(50), dp(1)), size_hint=(3, None))

        input_box_horz = BoxLayout(orientation='horizontal')
        input_box_horz.add_widget(MDLabel(text='', size_hint=(0.05, None)))
        input_box_horz.add_widget(self.long_press_btn)
        input_box_horz.add_widget(MDLabel(text='', size_hint=(0.05, None)))

        text_input_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=dp(65))
        text_input_anchor.add_widget(self.text_input)

        tap_input_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(1, 0.1), padding=dp(15))
        tap_input_anchor.add_widget(input_box_horz)

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title=contact, anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.return_screen()]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(layout)
        self.add_widget(text_input_anchor)
        self.add_widget(tap_input_anchor)
        self.add_widget(toolbar_anchor)
        self.do_layout()
        scroll.scroll_y = 0

    def text_input_cb(self, morse_char):
        for char in morse_char:
            self.text_input.text = self.text_input.text + char

    def send_message(self, msg):
        print("Sending message:%s" % msg)
        self.util.morse_app_api.send_message_req(self.send_message_cb,
                                                 self.util.username,
                                                 self.contact,
                                                 self.text_input.text)

    def send_message_cb(self, request, result):
        if request.resp_status == 200:
            if result['receiver'] in self.util.message_dict.keys():
                self.util.message_dict[result['receiver']].append(result)
            else:
                self.util.message_dict[result['receiver']] = [result]
            self.util.save_message_dict('receiver', self.util.message_dict)
            self.ui_layout(result['receiver'])
            self.util.reload_screen_layout('message')
            self.text_input.text = ''
        else:
            self.text_input.text = 'Error Sending Message'

    def return_screen(self):
        self.manager.current = 'message'
