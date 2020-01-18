#testrender.py

###IMPORT###

from PIL import Image,ImageFont,ImageDraw
import classes

###VARIABLES###

base = Image.new("RGBA",(100,100),(200,200,200,1)) #background. TODO: make it so that background color shows up
txt = Image.new('RGBA', base.size, (255,255,255,0)) #Text layer.
#head is like, printer head. it moves aroudn and dictates where to print text.
head = {"x":0,"y":0} #make this a class to I can do head.x, head.y
render = [] #list of objects to render.
draw = ImageDraw.Draw(txt) #draw object.

###DUMMY DATA###

#render test list; in practice, list "render" will be created with key presses n whatnot
testcharlist = ['l','o','r','e','m',' ','i','p','s','u','m']
for i in testcharlist:
    render.append(classes.Letter(i,15,"1942.ttf"))

###MAIN LOOP###

#Render loop 
for r in render: #for each letter
    draw.text((head["x"],head["y"]),r.char,font=r.font) #Draw the text. TODO: Coloring, formatting.
    head["x"] = head["x"] + r.getKerning()[0] #move print head over by kern
    if head["x"] + r.getKerning()[0] >= base.size[0]: #if hits edge of screen, wrap.
        #TODO: add margins
        head["x"] = 0 #reset x to 0
        head["y"] = head["y"] + r.font.getsize("l")[1] #assuming l is the tallest character, move down by that.
outimg = Image.alpha_composite(base, txt) #put text on background.

###OUTPUT###

#debug draw

outimg.show()
        
