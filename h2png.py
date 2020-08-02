from PIL import Image
import numpy as np
import re
import sys

class TextureParser:

    def __init__(self, file):
        self.file = file
        self.textureDict = {}
        self.READFLAG = 0
        self.getTextures(self.file)

    def getTextures(self, file):
        textureDictBuffer = ''
        textureFile = open(file, 'r')
        for line in textureFile:
            if(line[:len("static unsigned short")] == "static unsigned short"):
                self.READFLAG = 1
                textureDictBuffer = re.search('.+?(?=\[)',line[len("static unsigned short"):]).group()
                self.textureDict[textureDictBuffer] = []
                continue
            if(line[:2] == "};"):
                self.READFLAG = 0
                textureDictBuffer = ''
            if(self.READFLAG == 1):
                self.textureDict[textureDictBuffer].append(line[:len(line)-4].split(','))
        #print(self.textureDict)
        self.convertTextures()



    def convertTextures(self):

        for name, texture in self.textureDict.items():
            RGBAArray = []
            for row in texture:
                RGBARow = []
                for value in row:
                    RGBARow.append(hex2RGBA(value))
                RGBAArray.append(RGBARow)
            self.createTexturePNG(RGBAArray, name)
            
    def createTexturePNG(self, RGBAArray, name):
        array = np.array(RGBAArray, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(str(name)+'.png')
        print("Texture created")


def hex2RGBA(val):
    tempval = bin(int(val, 16))
    tempval = tempval[2:].zfill(16)
    r = (int(tempval[:5],2)/32)*255
    g = (int(tempval[5:10],2)/32)*255
    b = (int(tempval[10:15],2)/32)*255
    a = int(tempval[15:],2)
    print(r,g,b,a)
    return (r,g,b)



if __name__ == "__main__":
    texture = TextureParser(sys.argv[1])
