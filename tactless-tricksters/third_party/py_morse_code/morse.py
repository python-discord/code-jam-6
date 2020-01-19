import numpy as np
import re
import time
import pyaudio 

class DotDash:
	""" This class initiates a pyaudio session and can be used to produce the
		morse code output sounds. 
		Example:
		sound = DotDash()
		sound.dot()
		sound.dash() 
	"""
	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.volume = 0.4	 # range [0.0, 1.0]
		self.fs = 44000	   # sampling rate, Hz, must be integer
		self.dash_duration = 1.5
		self.dot_duration = 0.75   # in seconds, may be float
		self.f = 400.0		# sine frequency, Hz, may be float
		# generate samples, note conversion to float32 array
		self.dot_samples = (np.sin(2 * np.pi * np.arange(self.fs * self.dot_duration) * self.f / self.fs)).astype(np.float32)
		self.dash_samples = (np.sin(2 * np.pi * np.arange(self.fs * self.dash_duration) * self.f / self.fs)).astype(np.float32)

		# for paFloat32 sample values must be in range [-1.0, 1.0]
		self.stream = self.p.open(format = pyaudio.paFloat32,
									channels = 1,
									rate=self.fs,
									output=True)
	
	def dot(self):
		self.stream.write(self.volume * self.dot_samples)
	
	def dash(self):
		self.stream.write(self.volume * self.dash_samples)

	def close(self):
		# play. May repeat with different volume values (if done interactively) 
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()



def morse_kwarg_validate(func):
	""" This decorator passes a more descriptive error message when the user
		fails to pass the message in using a keyword argument """	
	def validated(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			return result
		except TypeError:
			raise TypeError('you must specify whether the message you are passing in is in words or morse format!\n'+\
							'example: words="message" or morse="... --- ..."')				
	return validated


class Morse:
	""" The Morse class can be used to translate messages between morse code and alphanumeric encodings.
		The class can also be used to play the morse code sounds associated with the message (all platforms)
		and read the message out loud (mac/linux only).

		A message can be read in when the class is initiated, or afterwards using the .read() function.
		The message must be passed in using one of the two keyword arguments: morse or words

		example:
		x = Morse(words = "this is a message")

		x.morse # get the morse for the message
		x.words # get the words for the message
		x # calling the variable will return both the morse and alphanumeric encodings

		x.transmit() # have the morse code DotDash representation of the message play
		x.speak() #MAC/Linux have the message spoken

		x.read(morse = "... --- ...") #overwrite the stored message by passing in morse
		x.read(words = "sos help me!") #overwrite the stored message by passing in words

	"""
	@morse_kwarg_validate
	def __init__(self, *, morse = None, words = None):
		self.__letter_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.',
			  'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---',
			  'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---',
			  'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
			  'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--',
			  'z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
			  '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
			  '9': '----.', ' ': '/' } #has a -> z, 1 -> 9 , and / for spaces
		#dict comprehension to reverse the key, value hash
		self.__morse_to_letter = {v : k for k, v in self.__letter_to_morse.items()}		

		self.read(morse = morse, words = words)

	@morse_kwarg_validate
	def read(self, *, morse = None, words = None):
		""" Take in a message in morse or alphanumeric encoding,
			store it within the object.
			The message type must be explicity declared as either morse or words:
			
			x = Morse()
			x.read(morse = "... --- ...") 
			x.read(words = "sos help me!")
			
			Morse code is read into the class as a string.
			format should be spaces between letters,
			and a forward slash / between words:
			'... --- ... ' #is equivalent to: 'sos'
			'-.-. .- -- / -. ..- --. . ' #is equivalent to: cam nuge 

			words are read into the class as a string.
			The message is converted to lower case.
			"""
		if morse is not None and words is not None:
			raise ValueError('can only pass in words or morse, not both!')
		if morse is not None:
			self.__read_morse(morse)
		if words is not None:
			self.__read_words(words)

	def __read_morse(self, morse):
		#split morse into words
		morse_words = morse.split('/')
		self.__morse = [x.split() for x in morse_words]
		# pass the list of words to the converter and store words
		words_from_morse = [[self.__morse_to_letter[letter] for letter in word] 
								for word in self.__morse]
		self.__words = words_from_morse

	def __read_words(self, words):
		# remove the punctuation, convert to lower case
		words = re.sub(r'[^\w\s]','', words.lower())
		# split on whitespace
		word_list = words.split()
		# store words as a list (words) of lists (letters)
		self.__words = [list(word) for word in word_list]
		# pass list of words to the converter and store morse
		morse_from_words = [[self.__letter_to_morse[letter] for letter in word] 
								for word in self.__words]
		self.__morse = morse_from_words

	@property
	def morse(self):
		""" the morse code message attribute """
		try:
			return ' / '.join([' '.join(x) for x in self.__morse])
		except:
			raise ValueError('no message stored in the object')
	@property
	def words(self):
		""" the alphanumeric message attribute """
		try:
			return ' '.join([''.join(x) for x in self.__words])
		except:
			raise ValueError('no message stored in the object')

	@morse.setter
	def morse(self, value):
		raise AttributeError('To overwrite the stored message, use the Morse.read() function!')

	@words.setter
	def words(self, value):
		raise AttributeError('To overwrite the stored message, use the Morse.read() function!')

	def transmit(self):
		""" when called, this function makes the sound for the morse code message"""
		sound = DotDash()

		for i in self.morse:
			if i == '.':
				sound.dot()
			elif i == '-':
				sound.dash()
			elif i == ' ' or i == '/':
				""" make total of .4 second pause for letter breaks
					and .6 seconds for word breaks """
				time.sleep(.2)

			time.sleep(.2) #wait a fifth of a second between each command

	def speak(self):
		""" for mac os only (or linux if say installation followed), 
			this function speaks the alphanumeric encoding of the message """
		from os import system
		system(f'say {self.words}')

	def __repr__(self):
		""" when print is called, show the morse code underneath the words """
		return f'message: {self.words}\n{self.morse}'
