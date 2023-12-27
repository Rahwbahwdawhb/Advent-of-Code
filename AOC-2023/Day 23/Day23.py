import os
import numpy as np
from copy import deepcopy

os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
# print(inputStrList)

class tileNodeClass:
    def __init__(self,row,col,tileNodeGrid):
        self.row=row
        self.col=col
        self.tileNodeGrid=tileNodeGrid
        self.neighbors=[]
        self.greatestPathDict=dict()
        self.greatestPath=[]
    def findNeighbors(self):
        for dRow,dCol in [[1,0],[-1,0],[0,1],[0,-1]]:
            try:
                gridNode=self.tileNodeGrid[self.row+dRow][self.col+dCol]
                if gridNode!='#':
                    self.neighbors.append(gridNode)
                    self.greatestPathDict[gridNode]=[]
            except:
                pass
    # def checkGreatestPath(self,suggestedPath):
    #     if (self not in suggestedPath) and (len(suggestedPath)>len(self.greatestPath)):
    #         self.greatestPath=suggestedPath
    #     for neighbor in self.neighbors:
    #         neighbor.checkGreatestPath(self.greatestPath+[self])
    #     1
    def assignCost(self,goalPosition):
        self.cost=np.abs(self.row-goalPosition[0])+np.abs(self.col-goalPosition[1])
    def checkOwnGreatestPath(self,suggestedPath):
        if (self not in suggestedPath) and (len(suggestedPath)>len(self.greatestPathDict[suggestedPath[-1]])):
            self.greatestPathDict[suggestedPath[-1]]=suggestedPath
            if len(suggestedPath)>len(self.greatestPath):
                self.greatestPath=suggestedPath
    def checkNeighborsGreatestPath(self,startNode):
        for neighbor in self.neighbors:
            pathLengths=[]
            paths=[]
            for neighbor_ in self.neighbors:                
                if neighbor_ != neighbor:
                    path=self.greatestPathDict[neighbor_]
                    pathLengths.append(len(path))
                    paths.append(path)
            try:
                pathToCheck=paths[pathLengths.index(max(pathLengths))]                
            except:
                pathToCheck=[]
            if startNode in pathToCheck or self==startNode:
                neighbor.checkOwnGreatestPath(pathToCheck+[self])
        return self.neighbors

slopeInterpretator={'^':[-1,0],'>':[0,1],'v':[1,0],'<':[-1,0]}
forestSet=set()
slopeDict=dict()
tileNodeGrid=[]
tileNodeList=[]
for ir,row in enumerate(inputStrList):
    tileNoderow=[]
    for ic,col in enumerate(row):
        if col=='#':
            forestSet.add((ir,ic))
            tileNoderow.append(col)
        else:
            tileNode=tileNodeClass(ir,ic,tileNodeGrid)
            tileNoderow.append(tileNode)
            tileNodeList.append(tileNode)
            if col in slopeInterpretator:
                slopeDict[(ir,ic)]=slopeInterpretator[col]
    tileNodeGrid.append(tileNoderow)
rowMax=len(inputStrList)-1
colMax=len(inputStrList[0])-1
startPoint=(0,inputStrList[0].index('.'))
goalPoint=(rowMax,inputStrList[-1].index('.'))
# print(startPoint,goalPoint)
# print((1,0) in forestSet)

stepQueue=[(startPoint,[])]
goalPaths=[]
goalPathLengths=[]
while len(stepQueue)!=0:
    currentPoint,currentPath=stepQueue.pop(0)
    # print(currentPoint,len(stepQueue),currentPath)
    if currentPoint==goalPoint:
        goalPaths.append(currentPath)
        goalPathLengths.append(len(currentPath))
    else:
        try:
            nextPoint=(currentPoint[0]+slopeDict[currentPoint][0],currentPoint[1]+slopeDict[currentPoint][1])
            if (nextPoint not in forestSet) and (nextPoint not in currentPath):
                stepQueue.append((nextPoint,currentPath+[nextPoint]))
        except:
            for dRow,dCol in [[1,0],[-1,0],[0,1],[0,-1]]:
                suggestedPoint=(currentPoint[0]+dRow,currentPoint[1]+dCol)
                if (suggestedPoint[0]>0) and (suggestedPoint not in forestSet) and (suggestedPoint not in currentPath):
                    stepQueue.append((suggestedPoint,currentPath+[suggestedPoint]))
# print(len(goalPaths))
print('1st:',max(goalPathLengths))

#part 2
# print(len(tileNodeList))
for tileNode in tileNodeList:
    tileNode.findNeighbors()
    tileNode.assignCost(goalPoint)

# for i,tileNode in enumerate(tileNodeList):
#     tileNode.checkGreatestPath()
1


# it=0
# for it in range(len(tileNodeList)+1):
#     nodesToCheck=[tileNodeList[0]]
#     checkedNodes=set()
#     while len(nodesToCheck)!=0:
#         currentNode=nodesToCheck.pop()
#         nextNodes=currentNode.checkNeighborsGreatestPath(tileNodeList[0])
#         for node in nextNodes:
#             if (currentNode,node) not in checkedNodes:
#                 nodesToCheck.append(node)
#                 checkedNodes.add((currentNode,node))

# greatestEndPath=tileNodeList[-1].greatestPathDict[next(iter(tileNodeList[-1].greatestPathDict))]
# endPath=[(node.row,node.col) for node in greatestEndPath]
# pathStr=''
# for ir,row in enumerate(inputStrList):
#     for ic,col in enumerate(row):
#         if (ir,ic) in endPath:
#             pathStr+='O'
#         else:
#             pathStr+=col
#     pathStr+='\n'
# print(pathStr)

#4574, 5150 too low
#idé: använd dijkstra med dynamisk kostfunktion, varje gridtile har manhattankostnad till goal
#då går från en tile till en annan lägg till (manhattan-distance nu)-(manhattan-distance nästa) till ackumulerad score
#och subtrahera varje steg som tar för ackumulerad score, borde promota att ta vägar som inte är nära mål så långt som möjligt
#testa m heap och popa första

goalNode=tileNodeList[-1]
import heapq
stepQueue=[]
heapq.heapify(stepQueue)
heapq.heappush(stepQueue,(0,0,tileNodeList[0],[]))
count=0
while True:    
    currentCost,_,currentNode,currentPath=heapq.heappop(stepQueue)
    if currentNode==goalNode:
        break
    for neighbor in currentNode.neighbors:
        count+=1
        if neighbor not in currentPath:
            heapq.heappush(stepQueue,(currentCost+(currentNode.cost-neighbor.cost)-1,count,neighbor,currentPath+[neighbor]))
print(len(currentPath))
1