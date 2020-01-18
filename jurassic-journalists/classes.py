#classes.py

#letter class- each letter is one of these objects, and is rendered in order.
class Letter:
    def __init__(char,size,font,color = (0,0,0,1),b=False,i=False,u=False):
        self.char = char
        self.size = size
        self.font = font
        self.color = color
        self.b = b
        self.i = i
        self.u = u
        #Map:
        #char: character.
        #size: size of letter.
        #font: reference to font.
        #color: color of letter, RGBA tuple, range 0-1.
        #b: Bold flag.
        #i: Italics flag.
        #u: Underlined flag.
        

#Witeout class- the little squiggle you have to do to erase words.
class WiteOut:
    def __init__():
        pass
