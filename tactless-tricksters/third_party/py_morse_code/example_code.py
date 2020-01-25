# here is some example code!
# assuming you are working in the same directory as the morse.py file (or it is on the search path)
from .morse import Morse, DotDash

test = 'sos, we are going down!'
test
morse_test = Morse()
# morse_test.words #this throws a value error, no message yet
morse_test.read(words=test)  # read in the string test
print(morse_test.words)  # show the words
print(morse_test.morse)  # show the morse code
print(morse_test)  # show the pretty print version of the message
morse_test.transmit()  # play message in morse code
# morse_test.speak() #say the message


test2 = '... --- ... / .----'
morse_test2 = Morse(morse=test2)  # read in to start
print(morse_test2.morse)
print(morse_test2.words)
morse_test2.transmit()
print(morse_test2)

test3 = 'not cam'
morse_test3 = Morse(words=test3, morse='... --- ...')  # ValueError - can only do one at a time!
print(morse_test3.words)
morse_test3 = Morse()
morse_test3.read(words='cam')  # the read method
# this throws an attribute error so you don't overwrite your message unless you really want to!
morse_test3.words = 'dave'
morse_test3.read(words='dave')  # change the message
print(morse_test3.words)
print(morse_test3.morse)
print(morse_test3)
morse_test3.transmit()

test4 = 'a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 '
morse_test4 = Morse()
morse_test4.read(words=test4)
print(morse_test4)

# just make the dot and dash sounds
sound = DotDash()
sound.dot()
sound.dash()
