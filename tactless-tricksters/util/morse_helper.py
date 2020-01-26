import os

from kivy.core.audio import SoundLoader

RATE = 16000
CHUNK = 4000  # number of audio samples per frame of test_data
DATA_RATE = 400  # sampling rate of signal activity in audio

# morse parameters
SMALLEST_TIME_UNIT = .1  # the unit of time in seconds that other duration will be multiple of
DOT_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT
DASH_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 5
LETTER_END_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 3
WORD_END_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 7

NUM_BITS_PER_SEC = int(RATE / DATA_RATE)
DOT_DURATION_THRESHOLD_BIT = int(DOT_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
DASH_DURATION_THRESHOLD_BIT = int(DASH_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
LETTER_END_DURATION_THRESHOLD_BIT = int(LETTER_END_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
WORD_END_DURATION_THRESHOLD_BIT = int(WORD_END_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)


class MorseHelper:
    def __init__(self):
        self.__letter_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.',
                                  'd': '-..', 'e': '.', 'f': '..-.',
                                  'g': '--.', 'h': '....', 'i': '..',
                                  'j': '.---', 'k': '-.-', 'l': '.-..',
                                  'm': '--', 'n': '-.', 'o': '---',
                                  'p': '.--.', 'q': '--.-', 'r': '.-.',
                                  's': '...', 't': '-', 'u': '..-',
                                  'v': '...-', 'w': '.--', 'x': '-..-',
                                  'y': '-.--', 'z': '--..', '0': '-----',
                                  '1': '.----', '2': '..---', '3': '...--',
                                  '4': '....-', '5': '.....', '6': '-....',
                                  '7': '--...', '8': '---..', '9': '----.',
                                  ' ': '/'}
        self.__morse_to_letter = {morse: letter for letter, morse in self.__letter_to_morse.items()}

    @property
    def long_press_dur(self):
        return DOT_DURATION_THRESHOLD_SEC

    @property
    def short_press_dur(self):
        return DASH_DURATION_THRESHOLD_SEC

    @property
    def long_pause_dur(self):
        return WORD_END_DURATION_THRESHOLD_SEC

    @property
    def short_pause_dur(self):
        return LETTER_END_DURATION_THRESHOLD_SEC

    def morse_to_text(self, morse_code):
        text = ''
        morse_words = [word for word in morse_code.split('/') if word != '']
        for morse_word in morse_words:
            for morse_letter in morse_word.split(' '):
                if morse_letter in self.__morse_to_letter:
                    text += self.__morse_to_letter[morse_letter]
                else:
                    text += '?'
            text += ' '
        return text.strip().strip('/')

    def text_to_morse(self, text):
        morse_code = ''
        text = text.lower()
        for letter in text:
            if letter in self.__letter_to_morse:
                morse_code += self.__letter_to_morse[letter] + ' '
            else:
                morse_code += '/?/ '
        return morse_code

    def get_letter_as_morse_sound(self, letter):
        sound_path = os.path.join('data', 'morse_alphabets', f'{letter}.wav')
        return SoundLoader.load(sound_path)


