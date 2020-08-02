
import re
class MaterialParser:

    def __init__(self, file):
        self.file = file
        self.MaterialDict = {}
        self.CLRLIST_FLAG = 0
        self.scanFile(self.file)
        #print(self.MaterialDict.values())


    def getMaterialDict(self):
        return self.MaterialDict



    # def createFile(self, filename):
    #     MtlFile = open(str(filename)+'.mtl','w')

    def scanFile(self, file):
        print("SCAN FILE :)")
        scanFile = open(file)
        for line in scanFile:
            #print(line)
            if(line[:2] == "};"):
                self.CLRLIST_FLAG = 0
            if(line[:len("static Lights1")] == "static Lights1"):
                MaterialName = re.search('(?<=1).+?(?=\[)', line).group().lstrip()
                #print("Object colors found for -", MaterialName)
                self.CLRLIST_FLAG = 1
                #self.colorIndex = 1
                self.MaterialDict[MaterialName] = []
                continue
            
            if(line.lstrip()[:len("gs_Tani_LoadTextureImage2")] == "gs_Tani_LoadTextureImage2"):
                TextureName = re.search('(?<=\().+?(?=\,)', line).group()
                #print("Found texture used -", TextureName)
                self.MaterialDict[TextureName] = TextureName 
            elif(line.lstrip()[:len('gsDPSetTextureImage')] == 'gsDPSetTextureImage'):
                TextureName = re.search(r'\b\w+(?=\))', line).group()
                #print("Found texture used -", TextureName)
                self.MaterialDict[TextureName] = TextureName 

            if(self.CLRLIST_FLAG == 1):
                r,g,b = (((re.search('(?<=\()[^,]*,[^,]*,[^,]*(?=\))',line)).group(0)).replace(' ', '')).split(',')
                
                #print(r,g,b)
                self.MaterialDict[MaterialName].append(
                    "newmtl "+MaterialName+" "+(str(len(self.MaterialDict[MaterialName])))+' '+"""
                    Ns 225.000000
                    Ka 1.000000 1.000000 1.000000
                    Kd"""+" "+str((int(r)/255))+" "+str((int(g)/255))+" "+str((int(b)/255))+"""
                    Ks 0.500000 0.500000 0.500000
                    Ke 0.000000 0.000000 0.000000
                    Ni 1.450000
                    d 1.000000
                    illum 2\n\n""")

    def createFile(self, filename):
        #print(self.MaterialDict[0])
        MtlFile = open(str(filename)+".mtl", 'w')
        for key in self.MaterialDict.keys():
            for mat in self.MaterialDict[key]:
                MtlFile.write(mat)
        MtlFile.close()

                
        
        
        
        #print(self.MaterialDict.keys())
        #print(self.MaterialDict.values())
        # return self.MaterialDict



    # def createFiles(self):


#### TEsting
#mtl = MaterialParser('luigi_near_poly.sou,v')




