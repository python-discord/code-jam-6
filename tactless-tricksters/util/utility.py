from third_party.py_morse_code.morse import Morse, DotDash
from threading import Thread

class Utility(object):
    def __init__(self):
        self.morse = Morse()
        # Temp debug data
        self.message_dict ={'Bob': {
                                'messages': ['hello', 'world', 'foo'],
                                'date': '01/15/19',
                                'img_source': 'ui/img/default_avatar.png',
                                }
                             ,
                             'Rob': {
                             'messages': ['foo', 'bar', 'goodbye'],
                             'date': '01/14/19',
                             'img_source': 'ui/img/default_avatar.png',
                                },
                            'Rod': {
                             'messages': ['good', 'bad', 'ugly'],
                             'date': '01/12/19',
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
