class Morse:
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
        self.__morse_to_letter = {morse: letter for letter, morse in self.__letter_to_morse.items}

    def morse_to_text(self, morse_code):
        text = ''
        morse_letters = morse_code.split(' ')
        for morse_letter in morse_letters:
            if morse_letter in self.__morse_to_letter:
                text += self.__morse_to_letter[morse_letter]
            else:
                text += '?'
        return text

    def text_to_morse(self, text):
        morse_code = []
        for letter in text:
            if letter in self.__letter_to_morse:
                text += self.__morse_to_letter[letter] + ' '
            else:
                text += '? '
        return morse_code

    def signal_to_morse(self, signal):
        pass

