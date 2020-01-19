#classes.py
from PIL import ImageFont
#letter class- each letter is one of these objects, and is rendered in order.
class Letter:
    def __init__(self,char,size,font,color = (255,255,255,255),b=False,i=False,u=False):
        self.char = char
        self.size = size
        self.font = ImageFont.truetype(font, size)
        self.color = color
        self.b = b
        self.i = i
        self.u = u
        #Map:
        #char: character.
        #size: size of letter.
        #font: PIL truetype font object. TODO: add handling for other types
        #color: color of letter, RGBA tuple, range 0-1.
        #b: Bold flag.
        #i: Italics flag.
        #u: Underlined flag.
    def getKerning(self):
        #gets dimensions as tuple(w,h) that it will be when rendered.
        return self.font.getsize(self.char)
        

#Witeout class- the little squiggle you have to do to erase words.
class WiteOut:
    def __init__(self):
        pass
