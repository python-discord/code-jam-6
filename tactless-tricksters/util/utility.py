from third_party.py_morse_code.morse import Morse, DotDash
from threading import Thread

class Utility(object):
    def __init__(self):
        self.morse = Morse()

    def morse_transmit_thread(self):
        morse_thread = Thread(target=self.morse.transmit)
        morse_thread.daemon = True
        morse_thread.start()

