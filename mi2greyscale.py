#author: duri Bradshaw
#date: 15/05/2020

#https://regex101.com/r/PA2UHW/1

import os, re

workspace = "D:\\Projects\\Python\\mi2greyscale\\wor\\map.WOR"
output = "D:\\Projects\\Python\\mi2greyscale\\wor\\map_grey.WOR"

# object to store RBV values
class RGB:
    def __init__(self,r = 0,g = 0,b = 0):
        self.red = r
        self.green = g
        self.blue = b

# Takes a colour workspace and produces a greyscale version
def wor2grey(colourwor,greywor):
    print('Colour WOR: ' +colourwor)
    colourset = set(getColours(colourwor))
    print('Colour set: ')
    print(colourset)
    clist = colourlist(colourset)
    print('Colour list: ')
    print(clist)
    
    f = open(colourwor)
    lines = f.readlines()
    f.close()

    with open(greywor, 'w') as worfile:
        out = []
        for row in lines:
            print('Old row: ' + row)

            for colour in clist:
                c = str(colour[0])
                b1 = r'(Brush\s[(]+[0-9]+,)(' + c + ')'
                b2 = r'(Brush\s[(]+[0-9]+[,][0-9]+[,])(' + c + ')'
                p = r'(Pen\s[(]+[0-9]+,[0-9]+,)(' + c + ')'
                l = r'(Line\s[(]+[0-9]+,[0-9]+,)(' + c + ')'
                s = r'(Symbol\s[(]+[0-9]+,)(' + c + ')'
                f = r'(Font\s[(]+"[a-zA-Z]+",[0-9]+,[0-9]+,)(' + c + ')'

                x = (re.compile(b1),re.compile(b2),re.compile(p),re.compile(l),re.compile(s),re.compile(f))

                for regex in x:
                    row = regex.sub(r"\1 "+str(colour[1]),row)
            print('New row: ' + row)            

            out.append(row)

        for l in out:
            worfile.write(l) 
          
# gets list of colours from workspace
def getColours(file):
    print('Gettnig RGB for: '+file)
    f = open(file)
    lines = f.readlines()
    f.close()

    colours = []

    for row in lines:
        
        brush = re.search(r'Brush\s[(][0-9]+[,]([0-9]+)[,]([0-9]+)', row)
        if (brush):
            mi_f = int(brush.group(1))
            colours.append(mi_f)

            mi_b = int(brush.group(2))
            colours.append(mi_b)

        pen = re.search(r'Pen\s[(][0-9]+,[0-9]+,([0-9]+)', row)
        if (pen):
            mi = int(pen.group(1))
            colours.append(mi)
        
        line = re.search(r'Line\s[(][0-9]+,[0-9]+,([0-9]+)', row)
        if (line):
            mi = int(line.group(1))
            colours.append(mi)

        sym = re.search(r'Symbol\s[(][0-9]+,([0-9]+)', row)
        if (sym):
            mi = int(sym.group(1))
            colours.append(mi)

        font = re.search(r'Font\s[(]"[a-zA-Z]+",[0-9]+,[0-9]+,([0-9]+)', row)
        if (font):
            mi_f = int(font.group(1))
            colours.append(mi_f)

    return colours

# adds greyscale to colour list
def colourlist(colours):
    cl = []
    for c in colours:
        cl.append([c,mi2grey(c)])
    return(cl)

# converts an MapInfo colour to greyscale
def mi2grey(mi):
    return grey2mi(rgb2grey(mi2rgb(mi)))

# converts an RGB to greyscale
def rgb2grey(rgb):
    return int((0.3 * rgb.red) + (0.59 * rgb.green) + (0.11 * rgb.blue))

# converts MapInfo colour to rgb
def mi2rgb(mi):
    r = mi // 65536
    g = (mi - r * 65536) // 256
    b = mi - r * 65536 - g * 256
    return RGB(r,g,b)

# converts a grey value to MapInfo colour
def grey2mi(grey):
    return ((grey*256*256)+(grey*256)+grey)

# converts a rgb to MapInfo colour
def rgb2mi(rgb):
    return ((rgb.red*256*256)+(rgb.green*256)+rgb.blue)

wor2grey(workspace,output)