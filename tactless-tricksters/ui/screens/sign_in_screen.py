# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from ui.widgets.welcome_button import WelcomeButton


class SignInScreen(Screen):
    def __init__(self, **kwargs):
        super(SignInScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        if self.util.username != '':
            self.status = 'signed_in'
        else:
            self.status = ''
        self.ui_layout()

    def ui_layout(self):
        self.clear_widgets()
        signin_card = MDCard(padding=dp(24),
                             spacing=dp(24),
                             orientation='vertical',
                             size_hint=(0.75, 0.65),
                             pos_hint={'top': 0.8, 'center_x': 0.5}
                             )

        sign_in_label = MDLabel(text='Sign in or Create an Account',
                                font_style='H4', halign='center')
        sign_in_label.theme_text_color = 'Custom'
        sign_in_label.text_color = [1, 1, 1, 1]

        self.helper_label = MDLabel(text='', font_style='Caption', halign='center')
        self.helper_label.theme_text_color = 'Custom'
        self.helper_label.text_color = [1, 1, 1, 1]

        self.username_field = MDTextField()
        self.username_field.hint_text = "User Name"

        # Password
        self.password_field = MDTextField(password=True)
        self.password_field.hint_text = "Password"
        self.password_field.helper_text = "Password must be at least 8 characters"
        self.password_field.helper_text_mode = "on_focus"
        self.proceedButton = WelcomeButton(icon='account-alert', text='  Enter',
                                           size_hint=(None, None), size=(4 * dp(48), dp(48)))

        signin_card.add_widget(sign_in_label)
        if self.status == 'signed_in':
            sign_in_label.text = '%s already signed in!' % self.util.username
            signin_card.add_widget(self.helper_label)
            signin_card.add_widget(Widget())
            signin_card.add_widget(Widget())
            self.proceedButton.text = 'Logout'
            self.proceedButton.icon = 'logout'
            self.proceedButton.bind(on_press=lambda x: self.remove_user_data())
            signin_card.add_widget(self.proceedButton)
        elif self.status == 'sign_in':
            sign_in_label.text = 'Sign In'
            self.proceedButton.bind(on_press=lambda x: self.auth_token())
            signin_card.add_widget(self.helper_label)
            signin_card.add_widget(self.username_field)
            signin_card.add_widget(self.password_field)
            signin_card.add_widget(self.proceedButton)
            signin_card.add_widget(Widget())
        elif self.status == 'create':
            sign_in_label.text = 'Create Account'
            signin_card.add_widget(self.helper_label)
            signin_card.add_widget(self.username_field)
            signin_card.add_widget(self.password_field)
            signin_card.add_widget(self.proceedButton)
            signin_card.add_widget(Widget())
            self.proceedButton.bind(on_press=lambda x: self.create_account())
        else:
            sign_in_button = WelcomeButton(icon='login', text='Sign-in')
            sign_in_button.bind(on_press=lambda x: self.up_date_layout('sign_in'))
            create_account_button = WelcomeButton(icon='creation', text='Sign-up')
            create_account_button.bind(on_press=lambda x: self.up_date_layout('create'))

            choice_box = BoxLayout(orientation='horizontal')
            choice_box.add_widget(Widget())
            choice_box.add_widget(sign_in_button)
            choice_box.add_widget(Widget())
            choice_box.add_widget(Widget())
            choice_box.add_widget(create_account_button)
            choice_box.add_widget(Widget())

            signin_card.add_widget(Widget())
            signin_card.add_widget(Widget())
            signin_card.add_widget(choice_box)
            signin_card.add_widget(Widget())

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title='Add Contact', anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.change_screen('welcome')]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(signin_card)
        self.add_widget(toolbar_anchor)
        self.do_layout()

    def create_account(self):
        username = self.username_field.text
        password = self.password_field.text
        if username != '' and len(password) > 7:
            self.util.morse_app_api.create_user_req(self.create_account_cb, username, password)
        else:
            self.helper_label.text = 'Invalid password and/or username'

    def create_account_cb(self, request, result):
        if request.resp_status != 200:
            self.helper_label = 'Error Making Account'
            self.password_field.text = ''
            self.username_field.text = ''
        else:
            self.helper_label = 'Account Created'
            print('need to check if the response is ok')
            self.auth_token()

    def auth_token(self):
        username = self.username_field.text
        password = self.password_field.text
        self.util.morse_app_api.retrieve_token_req(self.auth_token_cb, username, password)

    def auth_token_cb(self, request, result):
        if request.resp_status == 200:
            self.util.morse_app_api.update_header(result['token'])
            self.status = 'signed_in'
            self.util.save_token(result['token'])
            self.util.save_username(self.username_field.text)
            self.ui_layout()
            self.change_screen('welcome')
        else:
            self.helper_label = 'Error Authenticating Account'
        self.password_field.text = ''
        self.username_field.text = ''

    def remove_user_data(self):
        self.util.remove_user_data()
        self.status = ''
        self.ui_layout()

    def up_date_layout(self, mode):
        self.status = mode
        self.ui_layout()

    def on_value_change(self, instance, value):
        self.util.calibration = value
        print(value)

    def change_screen(self, screen):
        self.manager.current = screen
