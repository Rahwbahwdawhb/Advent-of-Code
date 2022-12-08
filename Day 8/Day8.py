from preload import input



# # print(input)

#1st problem
inpList=input.split('\n')
inpList=inpList[:-1]

# input='30373\n25512\n65332\n33549\n35390'
# inpList=input.split('\n')
# print(len(inpList),len(inpList[0]))

class tree:
    def __init__(self,row,col,height,maxRow,maxCol):
        self.row=row
        self.col=col
        self.height=height
        self.neighbors=[]
        self.maxRow=maxRow
        self.maxCol=maxCol
        self.visible=False
    def isVisible(self):
        if self.row==0 or self.row==self.maxRow or self.col==0 or self.col==self.maxCol:
            self.visible=True
        else:
            for n in self.neighbors:
                if self.height>n.height and n.visible:
                    self.visible=True
                    break
    def addNeighbor(self,neighbor):
        self.neighbors.append(neighbor)

treeList=[]
for it in range(len(inpList)):
    treeList.append([])
iterRow=0
maxRow=len(inpList)-1
maxCol=len(inpList[0])-1
for line in inpList:
    iterCol=0
    for ch in line:
        newTree=tree(iterRow,iterCol,int(ch),maxRow,maxCol)
        treeList[iterRow].append(newTree)
        if iterCol>0:
            treeList[iterRow][iterCol-1].addNeighbor(newTree)
            newTree.addNeighbor(treeList[iterRow][iterCol-1])
        if iterRow>0:
            treeList[iterRow-1][iterCol].addNeighbor(newTree)
            newTree.addNeighbor(treeList[iterRow-1][iterCol])
        iterCol+=1
    iterRow+=1

# print(len(treeList[0]))
vs=0
for row in treeList:
    for t in row:
        t.isVisible()
        if t.visible:
            vs+=1
for row in reversed(treeList):
    for t in row:
        t.isVisible()
for colIn in range(maxCol+1):
    for row in treeList:
        row[colIn].isVisible()
for colIn in range(maxCol+1):
    for row in reversed(treeList):
        row[colIn].isVisible()
visSum=0
for row in treeList:
    for t in row:
        if t.visible:
            visSum+=1
# print(visSum)

#1st problem take 2
import numpy as np
import copy
zz=np.zeros([maxRow+1,maxCol+1],dtype=int)
visible=copy.deepcopy(zz)
visible[:,0]=1
visible[:,-1]=1
visible[0,:]=1
visible[-1,:]=1
# print(visible)
iterRow=0
for line in inpList:
    iterCol=0
    for ch in line:
        zz[iterRow,iterCol]=int(ch)
        iterCol+=1
    iterRow+=1
# print(zz)
# iterRow=1
# iterCol=1
for rowIt in range(1,maxRow,1):
    for colIt in range(1,maxCol,1):
        zz[rowIt,colIt]
        check1=np.amax(zz[0:rowIt,colIt])
        check2=np.amax(zz[rowIt+1:maxRow+1,colIt])
        check3=np.amax(zz[rowIt,0:colIt])
        check4=np.amax(zz[rowIt,colIt+1:maxCol+1])
        if zz[rowIt,colIt]>check1 or zz[rowIt,colIt]>check2 or zz[rowIt,colIt]>check3 or zz[rowIt,colIt]>check4:
            visible[rowIt,colIt]=1
print('1st: ',np.sum(visible))
        

#2nd problem
scores=np.zeros([maxRow+1,maxCol+1],dtype=int)
for rowIt in range(1,maxRow,1):
    for colIt in range(1,maxCol,1):
        zz1=zz[0:rowIt,colIt]>=zz[rowIt,colIt]
        zz1=zz1[::-1]
        zz2=zz[rowIt+1:maxRow+1,colIt]>=zz[rowIt,colIt]
        zz3=zz[rowIt,0:colIt]>=zz[rowIt,colIt]
        zz3=zz3[::-1]
        zz4=zz[rowIt,colIt+1:maxCol+1]>=zz[rowIt,colIt]
        zzL=[zz1,zz2,zz3,zz4]
        val=1
        if colIt==2 and rowIt==3:
            1
        for ZZ in zzL:
            if len(ZZ)==0:
                valT=1
            else:
                trueIns=[i for i,x in enumerate(ZZ) if x]
                if len(trueIns)==0:
                    valT=len(ZZ)
                else:
                    valT=trueIns[0]+1
            val=valT*val
        scores[rowIt,colIt]=val
print('2nd: ',np.amax(scores))

        

