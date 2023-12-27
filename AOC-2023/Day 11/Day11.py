import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()

class galaxy:
    def __init__(self,position):
        self.otherGalaxies=[]
        self.distanceToOtherGalaxies=[]
        self.position=position
    def assignGalaxy(self,galaxy):
        if galaxy not in self.otherGalaxies and galaxy is not self:
            self.otherGalaxies.append(galaxy)
            self.distanceToOtherGalaxies.append(np.inf)
    def updateGalaxyDistace(self,galaxy,distance):
        galaxyIndex=self.otherGalaxies.index(galaxy)
        self.distanceToOtherGalaxies[galaxyIndex]=distance

def addEmptySpaceAndTranspose(spaceMap):
    mapList=spaceMap.split('\n')
    rowLength=len(mapList[0])
    newMapListList=[] 
    for row in mapList:
        emptySpaceSum=0
        for ch in row:
            if ch=='.':
                emptySpaceSum+=1
        rowList=list(row)
        newMapListList.append(rowList)
        if emptySpaceSum==rowLength:
            newMapListList.append(rowList)
    newMapListList2=list(map(list,zip(*newMapListList)))
    newSpaceMap=''
    for row in newMapListList2:
        newSpaceMap+=''.join(row)+'\n'
    newSpaceMap=newSpaceMap[:-1]
    return newSpaceMap,newMapListList2

#initial solution for part 1
# spaceMap,_=addEmptySpaceAndTranspose(inputStr)
# spaceMap2,spaceMap2ListList=addEmptySpaceAndTranspose(spaceMap)
# galaxyList=[]
# for ir,row in enumerate(spaceMap2ListList):
#     for ic,ch in enumerate(row):
#         if ch=='#':
#             newGalaxy=galaxy(np.array([ir,ic]))
#             galaxyList.append(newGalaxy)
# for galaxy_ in galaxyList:
#     for galaxy__ in galaxyList:
#         galaxy_.assignGalaxy(galaxy__)
# # for galaxy_ in galaxyList:
# #     print(len(galaxy_.otherGalaxies))
# # print(' ',len(galaxyList))
# allDistances=[]
# for galaxy_ in galaxyList:
#     startPosition=galaxy_.position
#     for galaxy__ in galaxy_.otherGalaxies:
#         startIndex=galaxy__.otherGalaxies.index(galaxy_)
#         if galaxy__.distanceToOtherGalaxies[startIndex]==np.inf:
#             goalPosition=galaxy__.position
#             galaxyDistance=sum(np.abs(goalPosition-startPosition))
#             galaxy__.distanceToOtherGalaxies[startIndex]=galaxyDistance
#             goalIndex=galaxy_.otherGalaxies.index(galaxy__)
#             galaxy_.distanceToOtherGalaxies[goalIndex]=galaxyDistance
#             allDistances.append(galaxyDistance)
# print(sum(allDistances))

#updated solution that also works for part 2, only counting empty space between galaxies
inputStrList=inputStr.split('\n')
galaxyList=[]
rowLength=len(inputStrList[0])
emptyRowIndices=[]
spaceMapListList=[]
for ir,row in enumerate(inputStrList):
    emptyRowSum=0
    spaceMapListList.append(list(row))
    for ic,ch in enumerate(row):
        if ch=='#':
            newGalaxy=galaxy(np.array([ir,ic]).astype(np.int64)) #int64 to not get overflow issues on 2nd part when adding distances
            galaxyList.append(newGalaxy)
        else:
            emptyRowSum+=1
    if emptyRowSum==rowLength:
        emptyRowIndices.append(ir)

spaceMapListList_transposed=list(map(list,zip(*spaceMapListList)))
columnLength=len(spaceMapListList_transposed[0])
emptyColumnIndices=[]
for ic,col in enumerate(spaceMapListList_transposed):
    emptyColSum=0
    for ir,ch in enumerate(col):
        if ch=='.':
           emptyColSum+=1 
    if emptyColSum==columnLength:
        emptyColumnIndices.append(ic)
for galaxy_ in galaxyList:
    for galaxy__ in galaxyList:
        galaxy_.assignGalaxy(galaxy__)

def getDistanceSum(galaxyList,expansion):
    Ngalaxies=len(galaxyList)
    for galaxy_ in galaxyList:
        galaxy_.distanceToOtherGalaxies=[np.inf for _ in range(Ngalaxies-1)]
    allDistances=[]
    for galaxy_ in galaxyList:
        startPosition=galaxy_.position
        for galaxy__ in galaxy_.otherGalaxies:
            startIndex=galaxy__.otherGalaxies.index(galaxy_)
            if galaxy__.distanceToOtherGalaxies[startIndex]==np.inf:
                goalPosition=galaxy__.position
                affectedRows=[startPosition[0],goalPosition[0]]
                affectedRowIndices=np.linspace(min(affectedRows),max(affectedRows),max(affectedRows)-min(affectedRows)+1)
                affectedColumns=[startPosition[1],goalPosition[1]]
                affectedColumnIndices=np.linspace(min(affectedColumns),max(affectedColumns),max(affectedColumns)-min(affectedColumns)+1)
                
                rowExpansionFactor=len([ri for ri in affectedRowIndices if ri in emptyRowIndices])
                columnExpansionFactor=len([ci for ci in affectedColumnIndices if ci in emptyColumnIndices])
                galaxyDistance=sum(np.abs(goalPosition-startPosition)+np.array([rowExpansionFactor,columnExpansionFactor])*(expansion-1))
                galaxy__.distanceToOtherGalaxies[startIndex]=galaxyDistance
                goalIndex=galaxy_.otherGalaxies.index(galaxy__)
                galaxy_.distanceToOtherGalaxies[goalIndex]=galaxyDistance
                allDistances.append(galaxyDistance)
    return sum(allDistances)
print('1st:',getDistanceSum(galaxyList,expansion=2))
print('2nd:',getDistanceSum(galaxyList,expansion=1000000))