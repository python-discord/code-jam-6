from .morse import Morse
import unittest


class MorseCodeTests(unittest.TestCase):
    """ unit tests for the reading, translation and representation of the
        Morse code class"""

    @classmethod
    def setUpClass(cls):
        """ this sets up a class through each of the initiation methods, making
            sure they all work """
        cls.morse_test1 = Morse(morse='... --- ... / .----')
        cls.morse_test2 = Morse(words='You... never did! - The Kenosha Kid')
        cls.morse_test3 = Morse()
        cls.morse_test3.read(words='cam was here')
        cls.morse_test4 = Morse()
        cls.morse_test4.read(morse='-.-. .- -- / -. ..- --. . -. -')
        cls.morse_test5 = Morse()
        cls.morse_test5.read(morse='... --- ...')

    def test_encoding(self):
        """ make sure the translation from morse to words,
            and words to morse have occured """
        self.assertEqual(self.morse_test1.words, 'sos 1')
        self.assertEqual(self.morse_test1.morse, '... --- ... / .----')

    def test_double_pass(self):
        with self.assertRaises(ValueError):
            self.morse_test5.read(words='we are passing two things ', morse='... --- ...')

    def test_no_kwargs(self):
        """ make sure a TypeError is raised if no keyword passed in with argument"""
        with self.assertRaises(TypeError):
            self.morse_test3.read('passing in a positional argument should fail')

    def test_properties(self):
        """ make sure we can't overwrite the stored strings """
        with self.assertRaises(AttributeError):
            self.morse_test1.words = 'change the words'

        with self.assertRaises(AttributeError):
            self.morse_test1.morse = '... --- ...'

    def test_repr(self):
        """ make sure that __repr__ is printing the expected message
            when print(object) is called. """
        self.assertEqual(self.morse_test2.__repr__(),
                         'message: you never did the kenosha kid\n'
                         '-.-- --- ..- / -. . ...- . .-. / -.. .. -.. / - '
                         '.... . / -.- . -. --- ... .... .- / -.- .. -..')


if __name__ == '__main__':
    unittest.main()
