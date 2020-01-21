from PIL import ImageFont
class Letter:
    """ letter class- each letter is one of these objects, and is rendered in order. """
    def __init__(self,char,size,font,color = (255,255,255,255),b=False,i=False,u=False):
        """
        char: character.
        size: size of letter.
        font: PIL truetype font object. TODO: add handling for other types
        color: color of letter, RGBA tuple, range 0-1.
        b: Bold flag.
        i: Italics flag.
        u: Underlined flag.
        """
        self.char = char
        self.size = size
        self.font = ImageFont.truetype(font, size)
        self.color = color
        self.b = b
        self.i = i
        self.u = u

    def get_kerning(self):
        """ gets dimensions as tuple(w,h) that it will be when rendered. """
        return self.font.getsize(self.char)
        
class WiteOut:
    """ Witeout class- the little squiggle you have to do to erase words. """
    def __init__(self):
        pass
