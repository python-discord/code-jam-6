from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.toolbar import MDToolbar
from kivymd.textfields import MDTextFieldRound
from kivymd.label import MDLabel
from kivymd.cards import MDCard

# Project imports
from ui.widgets.audio_indicator import AudioIndicator

# TODO remove after debug
import random

# Speech to text imports
import speech_recognition as sr

class EncoderScreen(Screen):
    def __init__(self, **kwargs):
        super(EncoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        play_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(25), dp(25), dp(25), dp(25)])

        play_button = MDFloatingActionButton(icon='play', size=[dp(56), dp(56)])
        play_button.md_bg_color = App.get_running_app().theme_cls.primary_color# [76/255, 175/255, 80/255, 1]
        play_button.text_color = [1, 1, 1, 1]
        play_button.bind(on_press=lambda x: self.play_audio())
        play_button_anchor.add_widget(play_button)

        self.encode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.85, 0.5))
        self.encode_input.icon_right = 'login'
        self.encode_input.children[2].children[0].bind(on_press=lambda x: self.encode_audio(self.encode_input.text))
        self.encode_input.icon_left = 'microphone'
        self.encode_input.children[2].children[2].disabled = False
        self.encode_input.children[2].children[2].bind(on_press=lambda x: self.speech_to_text())

        encode_card = MDCard(padding=dp(24), spacing=dp(24), orientation='vertical',
                             size_hint_x=0.85, size_hint_y=0.7, pos_hint={'top': 0.85, 'center_x': 0.5})
        encode_label = MDLabel(text='Encode Morse Code Audio', font_style='Body1', halign='center', size_hint=(1, 0.5))
        encode_label.theme_text_color = 'Custom'
        encode_label.text_color = [1, 1, 1, 1]

        self.encode_output_label = MDLabel(text='Enter text to convert to morse code', halign='center', size_hint=(1, 0.5))
        self.encode_output_label.theme_text_color = 'Custom'
        self.encode_output_label.text_color = [1, 1, 1, 1]

        self.audio_indicator = AudioIndicator()
        self.audio_indicator.size_hint = (1, 2)
        Clock.schedule_interval(self.update_audio_indicator, 0.1)

        encode_card.add_widget(encode_label)
        encode_card.add_widget(self.audio_indicator)
        encode_card.add_widget(self.encode_output_label)
        encode_card.add_widget(self.encode_input)
        encode_card.md_bg_color = App.get_running_app().theme_cls.accent_color
        encode_card.elevation = 15

        self.add_widget(encode_card)
        self.add_widget(play_button_anchor)

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = []
            for columns in range(self.audio_indicator.stack_width):
                level_array.append(random.randrange(0, self.audio_indicator.stack_height))
            self.audio_indicator.set_levels(level_array)

    def encode_audio(self, text):
        # TODO insert encoding audio function
        self.util.morse.read(words=text)
        print(self.util.morse.words)
        print(self.util.morse.morse)
        self.encode_output_label.text = 'Morse Code: %s' % self.util.morse.morse
        self.encode_input.text = ''

    def play_audio(self):
        if "Morse Code" in self.encode_output_label.text:
            self.util.morse_transmit_thread()
        else:
            self.encode_output_label.text = 'Enter Text to Encode before playing'

    def speech_to_text(self):
        recognizedSpeech= ""

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
          "type": "service_account",
          "project_id": "helpful-kit-265623",
          "private_key_id": "2530a9a08f7c5318cbde3c2eee8ef5653e258097",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcyl1gbQBSQTZt\ntG7Uk21Pi67keQc/PrZ5q50CafTpG5nihu+ee/nDdN9u1HAOwB0CB4qr1zOrhyyC\n7kaNI79XO9oPPLB4ypuu6z95HVoAJ4J/JlpzEFwHunC/WomH8xMrvvt+zpt76nB2\nKp2iBfAFuck1ww+YoP4hsPx2fn+7rRn+yYraRYV38Ec0Z86Zx5QFbDhd8YoKF1o4\n7wnJUHRwZgPAlaIluOwTioYOHqDTtzCjTllpB5VzXxg9UPHPqbG3Dn2+rlOooSqH\n9x4VZbPrmGbsPtpHYVfsK4dyhpfjo85KAp8jTTV/rAQdRTlBBu+2MlRX+5W065r5\nQYeEuSE1AgMBAAECggEAFa4Nt1WbI8SMqCK46H/yL3ubFVB+5gnf5XcLYNgR22HL\np30NCRcPdC1m78ZEMGX0HOG6FQTOyjsItpoH+2AkBwXpow27QRiS6l7xCeg7F6Ze\n7wH4o8xxTUhEatE0Dy5XSkdAM0qSSVIjdtNxtIOpqsEDx4FPWMV6HmKApknbk7Gm\nXoMN5w4o9qEgaSEohrJmzSreq09hPSYOJgCegnQuYmjIB9Ydcn5q+mheSaiSTkVa\nEPCbLt1M2ZHJdWmejumfHs6S0nBb+ayJUsPEs5jbIA0T+25mj3E6Gz+PtG+o0Ic+\nYipXXzECFQO/EfFsKu1bWx2E9lR0kItqF0Zcc2lPwQKBgQDRgkHAt7U+7AfjSypt\nu0mK8OtufrX6VlgQkvbfpL4mo6hTJGafbUR0UyDgNPclmm2LtUCcF3XqUVVzCaG0\nhCeauYOAFkrua80H+Jf70xGTuqk14ciqFVt5k0STFnSUi4wx3yMOf7VY6QM4S1sO\ngRqKAf3BxcbPfpzsX6cxmgBjPQKBgQC/lUsnWzshSnqGicR6lJ79K7vV2EglL3Hn\nKvKrcLaqf8FoDAyCcvbT0p/BP/WX2GaBjYiChHYpRavFNAyw0l4ns8NU3VoBO3VM\n5eX1BVJMH0z65lj6aYL4uB0N5ccsEzetU9uClXUiiNJgph0R77xO3V5vxYY4tW6k\nlIFQYuc1WQKBgQDOIgvRsq54T0DfiJghSPFt6+aoW7Fusj+JZx/RIUUZvVIjI6B4\n4chFb3jcQCCe9dcsa1Q7f/W7avTY77QTaSeSW06f2s800An1+siGs8AKitBrvE9z\n0Pmkn5oL4j8n3Dk+5F2YqVxjMzfAzpuzpKDZAmaKna4jf16kTuSwr+YLvQKBgCeT\nTX0JyYMtAXZ9SwsPXHBr8ldQYEbeMCdSpeJoXDOIRImbw5HG8dn77mhbL/54A2TL\nueFMP6Ry8fLAt8ZnDnAhID6NoyQSBj8mVoRw3vk+lgZWQxcnaJi8X7QZPTWLmrrB\nUdz9xr6liN/SMLsdzMZ10CZCpWFdiUeSLcxPQfexAoGAWGlK/rpIrr+MPsjoXnQB\nem2HnSOaC78IDAcTEmmBb1bznmirZ37Ychhkt7r7HO3PDywzaDvrJ6wRHW9f7c6M\n9kbn0eWVomlJkCXtQK2oPbhJpAO4rBrDmclRvatb5UFVIPjr2hkpmXZje5pZcIDi\nv73KKiw30SPKiVCQSoimigM=\n-----END PRIVATE KEY-----\n",
          "client_email": "starting-account-hnv2jlbh0h0@helpful-kit-265623.iam.gserviceaccount.com",
          "client_id": "110322539966439067530",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/starting-account-hnv2jlbh0h0%40helpful-kit-265623.iam.gserviceaccount.com"
        }"""
        try:
            recognizedSpeech= r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            print("Google Cloud:",recognizedSpeech)
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
        except:
            print("Google Cloud: Another Exception occurred. Trying with Sphinx.")

        #If google cloud fails, try with Sphinx
        if recognizedSpeech="":
            try:
                recognizedSpeech = r.recognize_sphinx(audio)
                print("Sphinx:",recognizedSpeech)
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

        self.encode_input.text = recognizedSpeech

    def return_home(self):
        self.manager.current = 'welcome'
