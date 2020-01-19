# py-morse
## A morse code class object for translation between morse and alphanumeric encodings, which supports both text and audio message representation.
[![Build Status](https://travis-ci.org/CNuge/py-morse-code.svg?branch=master)](https://travis-ci.org/CNuge/py-morse-code)

## The Morse class does the following:
- Reads in string of words or morse code and allows for translation between the two.
- Provides a transmit function to play the audio morse code version of the message.
- Lets you easily print the words and corresponding morse side by side.
- mac/linux only: Uses the unix `say` command to read the message out loud.

## Limitations:
- If the message is input as a word, all punctuation will be removed.
- The 'stop' to indicate the end of a sentence is not yet coded in.
	- This could be a useful addition if made to be optional.
- The speak command is performed using the mac/linux 'say' command so not usable on windows.

## Morse syntax
- For use in this class, letters in a given word are separated by a space, and words are separated by a forward slash `/` character. Dots are `.` periods and dashes are `-` hyphens.
- so the string for `'sos'` would be `'... --- ...'` and the string for `'sos cam'` would be `... --- ... / -.-. .- --'`

## How to use it
The `Morse` class can be used in several different ways after it is first imported into the current session via
`from morse import Morse`. An empty class instance can initiated, or the data can be read in during initiation using the `morse=` or `words=` arguments (only one of the two can be passed in at a time). `example_code.py` provides some additional example uses cases.

```
morse_test = Morse() # an empty class message that can be passed data later

#OR

morse_test = Morse(words = 'This is a test')

morse_test = Morse(morse = '- .... .. ... / .. ... / .- / - . ... -')

```

Once the Morse class is instantiated, words or morse can be read in using the following function. Note if there is already a message stored in the class then the read function will overwrite it!
```
morse_test.read(morse = '- .... .. ... / .. ... / .- / - . ... -')

morse_test.read(words = 'This is a test')

```

Once you have read a message in to the class the morse and alphanumeric encodings of the message can respectively be called using the .morse and .words properties.
```
morse_test.morse

morse_test.words
```

When print is called on the object, it will return both encodings of the message
```
print(morse_test)
```
which will return:
```
message: this is a test
- .... .. ... / .. ... / .- / - . ... -
```
The class also contains methods for returning the corresponding audio for the morse (all platforms) and alphanumeric encodings (mac/linux).
```
morse_test.transmit() # returns the tones corresponding to the morse code

morse_test.speak() # this uses the unix say command to read the message 
#.speak() is mac/linux only... and you need to follow the instructions below to get it running on linux
```


# Audio dependencies setup
The following must be installed in order to use the transmit function which plays back the morse code.
### mac 
```
brew install portaudio 
pip install pyaudio
```
### windows 
```
python -m pip install pyaudio
```

### Linux
```
sudo apt-get install python-pyaudio python3-pyaudio
```
optional - to make the .speak() function work:
```
sudo apt-get install gnustep-gui-runtime
```
## Other dependencies
You will need to have `numpy` installed as well (all platforms).
`pip install numpy`
