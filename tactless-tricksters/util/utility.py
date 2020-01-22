from third_party.py_morse_code.morse import Morse, DotDash
from auto_morse_recognizer.auto_morse_recognizer import AutoMorseRecognizer
from threading import Thread


class Utility(object):
    def __init__(self):
        self.user_name = 'user_name'
        self.morse = Morse()
        self.auto_morse_recognizer = AutoMorseRecognizer(active_threshold=9)
        # Temp debug test_data
        self.message_dict = {
            'Bob': {
            'messages': [
                {
                    'text': 'hello',
                    'author': 'user_name',
                    'date': '111111'
                },
                {
                    'text': 'world',
                    'author': 'Bob',
                    'date': '222222'
                },
                {
                    'text': 'foo',
                    'author': 'Bob',
                    'date': '333333'
                },
            ],
            'img_source': 'ui/img/default_avatar.png',
        },
            'Rob': {
                'messages': [
                    {
                        'text': 'hello',
                        'author': 'user_name',
                        'date': '111111'
                    },
                    {
                        'text': 'world',
                        'author': 'Rob',
                        'date': '222222'
                    },
                    {
                        'text': 'foo',
                        'author': 'Rob',
                        'date': '333333'
                    },
                ],
                'img_source': 'ui/img/default_avatar.png',
            },
            'Rod': {
                'messages': [
                    {
                        'text': 'hello',
                        'author': 'user_name',
                        'date': '111111'
                    },
                    {
                        'text': 'world',
                        'author': 'Rob',
                        'date': '222222'
                    },
                    {
                        'text': 'foo',
                        'author': 'Rob',
                        'date': '333333'
                    },
                ],
                'img_source': 'ui/img/default_avatar.png',
            }
        }

    def morse_transmit_thread(self):
        morse_thread = Thread(target=self.morse.transmit)
        morse_thread.daemon = True
        morse_thread.start()

    def morse_transmit_speak(self):
        morse_thread = Thread(target=self.morse.speak)
        morse_thread.daemon = True
        morse_thread.start()

    def load_messages(self):
        # TODO
        pass
