import re
import sys
import texture2mtl
class InputParser:

    def __init__(self, file):
        self.VertexListDict = {}
        self.ObjectListDict = {}
        self.file = file
        self.ObjectCount = 0
        self.VTXLIST_FLAG = 0
        self.OBJLIST_FLAG = 0
        self.matParser = texture2mtl.MaterialParser(self.file)
        self.MaterialDict = self.matParser.getMaterialDict()
        self.ReadFile(self.file)


    def ReadFile(self,file):
        souv = open(file, "r")
        VertexListBuffer = []
        ObjectListBuffer = []
        VertexDictName = None
        ObjectDictName = None
        for line in souv:

            if(line[:10] == "static Vtx"):
                VertexDictName = re.search('.+?(?=\[)', line[11:]).group()
                self.VTXLIST_FLAG = 1
                continue
            if(line[:len("static Gfx")] == "static Gfx" or line[:len("Gfx")] == "Gfx" ):

                self.ObjectCount = self.ObjectCount + 1
                self.OBJLIST_FLAG = 1
                ObjectDictName = re.search('(?<=x).+?(?=\[)', line).group().lstrip()
                continue
            elif(line[:2] == "};"):
                if(self.VTXLIST_FLAG==1):
                    self.VTXLIST_FLAG = 0
                    self.VertexListDict[VertexDictName] = VertexListBuffer
                    VertexListBuffer = []
                if self.OBJLIST_FLAG == 1:
                    self.OBJLIST_FLAG = 0
                    self.ObjectListDict[ObjectDictName] = ObjectListBuffer
                    ObjectListBuffer = []
                    ObjectDictName = None
                continue
            if(self.VTXLIST_FLAG == 1):
                VertexListBuffer.append((((re.search('(?<={)[^,]*,[^,]*,[^,]*', line)).group(0)).replace(' ','')).split(','))
            if(self.OBJLIST_FLAG == 1):
                ObjectListBuffer.append(line)
        print("Amount of potential objects found is",self.ObjectCount)


    def GetVertexRange(self, obj):
        startCount = -1
        finalCount = -1
        for line in obj:
            if(line.lstrip()[:len('gsSPVertex')] == 'gsSPVertex'):
                if(startCount == -1):
                    try:
                        startCount = int((re.search('\[\s*(.*?)\s*\]', line.lstrip())).group(1))
                    except:
                        startCount = int((re.search('\[\s*(.*)\s*\-', line.lstrip())).group(1))
                    finalCount = startCount
                finalCount = finalCount + int(line.split(',')[1])
        return(startCount, finalCount)

    def CalculateFaces(self, obj, faceamt):
        ObjFaceList = []
        initalFaceOffset = None
        faceOffset = 0
        for line in obj:
            if(line.lstrip()[:len('gsSPVertex')] == 'gsSPVertex'):
                try:
                    if(faceOffset == 0):
                        initalFaceOffset = int((re.search('\[\s*(.*?)\s*\]', line.lstrip())).group(1))
                    faceOffset = int((re.search('\[\s*(.*?)\s*\]', line.lstrip())).group(1)) +1    
                except:
                    if(faceOffset == 0):
                        initalFaceOffset = int((re.search('\[\s*(.*?)\s*\]', line.lstrip())).group(1)) 
                    faceOffset = int((re.search('\[\s*(.*)\s*\-', line.lstrip())).group(1)) +1
            if(line.lstrip()[:len("gsSPLight")]=='gsSPLight'):
                materialName = re.search('(?<=&).+?(?=\[)', line.lstrip()).group()
                materialIndex = int(re.findall('\[\s*(.*?)\s*\]',line)[0])
                ObjFaceList.append('usemtl {} {}\n'.format(materialName,materialIndex))
            if(line.lstrip()[:len('gsSP1Triangle')] == 'gsSP1Triangle'):
                v1,v2,v3 = (re.search('(?<=\()[^,]*,[^,]*,[^,]*(?=\,)', line)).group().split(',')
                ObjFaceList.append('f '+str(int(v1)+(faceOffset-initalFaceOffset))+' '+str(int(v2)+(faceOffset-initalFaceOffset))+' '+str(int(v3)+(faceOffset-initalFaceOffset))+' '+'\n')
        return ObjFaceList

    def GetObjectVertexList(self, obj):
        for line in obj:
            if(line.lstrip()[:len('gsSPVertex')] == 'gsSPVertex'):
                ObjectName = re.search('(?<=&).+?(?=\[)', line.lstrip()).group()
                print("GetObjectVertexList is returning -", ObjectName)
                return ObjectName

    def CreateObjects(self):
        print('Creating found vertex objects!')
        ObjectNumber=0
        ColorAmt =0
        for name,obj in self.ObjectListDict.items():

            StartVertexIndex, EndVertexIndex = self.GetVertexRange(obj)
            print("Starting Vertex index and ending vertex is ", StartVertexIndex, EndVertexIndex)
            if(self.GetObjectVertexList(obj)) == None:
                print("No vertex list loaded.. Skipping")
                continue
    

            ObjFile = open(str(name)+'.obj', 'w')

            self.matParser.createFile(name)
            



            print("Created - Convertedobj"+str(ObjectNumber)+'.obj!')

            try:
                for vertex in self.VertexListDict[self.GetObjectVertexList(obj)][StartVertexIndex : EndVertexIndex]:
                    ObjFile.write('v {} {} {}\n'.format(vertex[0],vertex[1], vertex[2]))
            except:
                print("SHOULDNT HAPPEN?")
                ObjFile.close()
                continue


            ObjectNumber = ObjectNumber+1
            FaceAmt = (EndVertexIndex - StartVertexIndex)
            ObjFaceList = self.CalculateFaces(obj, FaceAmt)
            for line in ObjFaceList:
                ObjFile.write(line)

            ColorAmt = 0
            ObjFile.close()
        
if __name__ == "__main__":  

    inputParser = InputParser(sys.argv[1])
    inputParser.CreateObjects()
    

                    




        