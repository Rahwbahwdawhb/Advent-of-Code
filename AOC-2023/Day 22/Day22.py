import os
import numpy as np

os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

#idea: assign each sand brick its own object keeping tack of sandblocks below it (which it is supported by) and sandblocks above it (which it supports)
#have a ground controling object that keep track of highest z-positions above each (x,y)-point, these heights is where falling sand blocks will stop depending on which (x,y)-points their xy-projection overlap
#for part 2, the references to sand bricks above/below can just be updated to account for whether sand bricks not immediately above would fall upon disintegration

class sandBrickClass:
    def __init__(self,endPoint1,endPoint2):
        self.supportedBy=set()
        self.supporting=set()
        if np.max(np.abs(endPoint1-endPoint2))==0:
            self.sandCubes=[endPoint1]
            self.lowestZ=endPoint1[2]
        else:
            differingIndex=np.argwhere(endPoint1-endPoint2!=0).flatten()[0] #find coordinate to vary to generate sand cubes within sand brick
            indexRange=[endPoint1[differingIndex],endPoint2[differingIndex]]
            self.sandCubes=[]
            for c in range(min(indexRange),max(indexRange)+1):
                temp=endPoint1+0
                temp[differingIndex]=c
                self.sandCubes.append(temp)
            self.lowestZ=min([endPoint1[2],endPoint2[2]])
        self.yxProjection=set() #which coordinates it will block in a xy-plane, only unique coordinates to not add onto itself for each sandcube if vertically oriented
        for sandCube in self.sandCubes:
            self.yxProjection.add((sandCube[1],sandCube[0]))
    def assignSupporter(self,sandBrick):
        self.supportedBy.add(sandBrick)
        sandBrick.supporting.add(self)
    def adjustZposition(self,newLowestZ): #change z-coordinates when falling
        newZs=[]
        for i,sandCube in enumerate(self.sandCubes):
            newZ=sandCube[2]-self.lowestZ+newLowestZ
            self.sandCubes[i][2]=newZ
            newZs.append(newZ)
        self.lowestZ=newLowestZ
        return max(newZs)

sandBrickList=[]
xRange=[np.inf,-np.inf] #ranges to set up xy-plane
yRange=[np.inf,-np.inf]
for row in inputStrList:
    endPoint1Str,endPoint2Str=row.split('~')
    endPoint1_=np.array([int(c) for c in endPoint1Str.split(',')])
    endPoint2_=np.array([int(c) for c in endPoint2Str.split(',')])
    xRange[0]=min([xRange[0],endPoint1_[0],endPoint2_[0]])
    xRange[1]=max([xRange[1],endPoint1_[0],endPoint2_[0]])
    yRange[0]=min([yRange[0],endPoint1_[1],endPoint2_[1]])
    yRange[1]=max([yRange[1],endPoint1_[1],endPoint2_[1]])
    sandBrick=sandBrickClass(endPoint1_,endPoint2_)
    sandBrickList.append((sandBrick.lowestZ,sandBrick))
sandBrickList.sort(key=lambda a: a[0])

class groundControlClass:
    def __init__(self,xRange,yRange):
        Ny=yRange[1]-yRange[0]+1
        Nx=xRange[1]-xRange[0]+1
        self.grid=np.zeros((Ny,Nx))
        self.gridAssociater=[[None for _ in range(Nx)] for _ in range(Ny)] #will hold the sand brick at the highest z-position above each (x,y)-point
    def fall(self,sandBrick):
        rowIndices=[]
        colIndices=[]
        heightsToConsider=[]
        supportingBricks=[]
        for yxP in sandBrick.yxProjection:
            rowIndices.append(yxP[0])
            colIndices.append(yxP[1])
            heightsToConsider.append(self.grid[yxP[0],yxP[1]])     
            supportingBricks.append(self.gridAssociater[yxP[0]][yxP[1]])   
        limitingHeight=np.max(heightsToConsider) #can only fall to the highest height above (x,y)-points the xy-projection overlap
        for ri,ci,h in zip(rowIndices,colIndices,heightsToConsider):
            currentAssociation=self.gridAssociater[ri][ci]
            if currentAssociation!=None and h==limitingHeight: #if the sand brick falls onto another sand brick, assign the lower sand brick to be supporting the falling sand brick
                sandBrick.assignSupporter(currentAssociation)
            self.gridAssociater[ri][ci]=sandBrick
        newLimitingHeight=sandBrick.adjustZposition(limitingHeight+1) #the new lowest height for the falling sand brick will be +1 of the limiting height (sand cubes extend 1 unit volume in z), return the resulting highest z-position of the previously falling sand brick
        self.grid[rowIndices,colIndices]=newLimitingHeight

groundControl=groundControlClass(xRange,yRange)
for _,sandBrick in sandBrickList: #let all sand bricks fall and get new heights and sandbrick to support and/or be supported by
    groundControl.fall(sandBrick)

#part 1
freeToDisintegrateCounter=0
for _,sandBrick in sandBrickList:
    NsupportingBricks=len(sandBrick.supporting)
    supportedByOtherBricks=0
    for sandBrick_ in sandBrick.supporting: #check that there is at least 1 other sand brick to support other sand bricks that the current sand brick is supporting
        if len(sandBrick_.supportedBy)>1:
            supportedByOtherBricks+=1
    if supportedByOtherBricks==NsupportingBricks: #if all sand bricks that are supported by the current sand brick are supported by at least one more sand brick, then the current sand brick can be disintegrated
        freeToDisintegrateCounter+=1
print('1st:',freeToDisintegrateCounter)

#part 2
otherFallingSandBrickSum=0
for _,sandBrick in sandBrickList[::-1]: #start checking sand bricks that are the furthest from the ground
    fallingSandBricks=set()
    for sandBrickAbove in sandBrick.supporting:
        if len(sandBrickAbove.supportedBy)==1: #add bricks that are above if they are only supported by the current sand brick
            fallingSandBricks.add(sandBrickAbove)
    otherFallingSandBrickSum+=len(fallingSandBricks)
    for sandBrickBelow in sandBrick.supportedBy:
        for sandBrickAbove in sandBrick.supporting: #add that sandbricks above are supported by sand bricks below and that sand bricks below support sand bricks above (using sets to not add the same sand brick multiple times)
            sandBrickAbove.supportedBy.add(sandBrickBelow) 
            sandBrickBelow.supporting.add(sandBrickAbove)
            try:
                sandBrickAbove.supportedBy.remove(sandBrick)
            except:
                pass

print('2nd:',otherFallingSandBrickSum)




