from preload import input
# print(input)

#1st problem
inpList=input.split('\n')
inpList=inpList[:-1]
# inpList=[]
# with open('ex.txt','r') as f:
#     for line in f.read().split('\n'):
#         inpList.append(line)
# for inp in inpList:
#     print(inp)

class directory:
    def __init__(self,name,parent,listOfInterest):
        self.subDirs=[]
        self.files=[]
        self.parent=parent
        self.name=name
        self.subDirNames=[]
        self.sizeTot=0
        self.listOfInterest=listOfInterest
    def addFile(self,file,size):
        self.files.append((file,int(size)))
        self.incrementSize(int(size))
    def incrementSize(self,addSize):
        self.sizeTot+=addSize
        if self.parent!=None:
            self.parent.incrementSize(addSize)
        if self.sizeTot>100000:
            # self.listOfInterest.remove(self)
            self.removeSelfFromLOI()
        else:
            if self not in self.listOfInterest:
                self.listOfInterest.append(self)  
        1      
    def removeSelfFromLOI(self):
        # del self.listOfInterest[self.listOfInterest.index(self)]
        if self in self.listOfInterest:
            self.listOfInterest.remove(self)
        if self.parent!=None:
            self.parent.removeSelfFromLOI()
    def addSubDir(self,subDirName):
        subDir=directory(subDirName,self,self.listOfInterest)
        self.subDirs.append(subDir)
        self.subDirNames.append(subDirName)
        return subDir

listOfInterest=[]
allDirs=[]
currentDir=None
iter=0
iterMAX=len(inpList)
while iter<iterMAX:
    inp=inpList[iter]
    cdIn=inp.find('cd')
    if cdIn!=-1:
        cdName=inp[cdIn+3:]
        if currentDir is None:
            topDir=directory(cdName,None,listOfInterest)
            currentDir=topDir
            allDirs.append(topDir)
        else:
            if cdName.find('..')!=-1:
                currentDir=currentDir.parent
            elif cdName.find('/')!=-1:
                currentDir=topDir
            else:
                if cdName not in currentDir.subDirNames:
                    newSubDir=currentDir.addSubDir(cdName)
                    currentDir=newSubDir                    
                else:
                    currentDir=currentDir.subDirs[currentDir.subDirNames.index(cdName)]
        if currentDir not in allDirs:
            allDirs.append(currentDir)

    elif inp.find('ls')!=-1:
        iter+=1
        dirContent=inpList[iter]
        while dirContent.find('$')==-1:
            sizeOrDir,content=dirContent.split(' ')
            if sizeOrDir.find('dir')!=-1:
                currentDir.addSubDir(content)
            else:
                currentDir.addFile(content,sizeOrDir)            
            iter+=1
            if iter<iterMAX:
                dirContent=inpList[iter]
            else:
                break
        iter-=1
    iter+=1
totSize=0
for dir in set(listOfInterest):
    totSize+=dir.sizeTot
print('1st: ',totSize)

#2nd problem
# print(70000000-topDir.sizeTot)
okSpaceToHave=70000000-30000000
neededSpace=topDir.sizeTot-okSpaceToHave
sizesOfInterest=[]
for dir in allDirs:
    dirSize=dir.sizeTot
    if dirSize>=neededSpace:
        sizesOfInterest.append(dirSize)
# print(neededSpace)
print('2nd: ',min(sizesOfInterest))