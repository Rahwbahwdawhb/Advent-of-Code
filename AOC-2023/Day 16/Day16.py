import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

#main idea: let the stationary mirros and splitters do all work, assign them with dictionaries that give info on how to
#redirect light to neighboring mirrors/splitters, keep track of beam path (to avoid getting stuck in loops) and 
#direction going into next mirror/splitter, add this info into a queue and pop first element and iterate until it is empty
#next mirror/splitter is appended to queue if it is not part of a loop

class beamInteracter:
    def __init__(self,gridPosition,interactionDict,energizedGridPointSet,beamQueue,historyStrSet):
        self.gridPositionStr=str(gridPosition)
        self.interactionDict=interactionDict
        self.energizedGridPointSet=energizedGridPointSet
        self.beamQueue=beamQueue
        self.gridPointDict=dict()
        self.neighboringBeamInteractorDict=dict()
        self.historyStrSet=historyStrSet
        for direction in ['north','east','south','west']:
            self.gridPointDict[direction]=[gridPosition]
            self.neighboringBeamInteractorDict[direction]=None
    def interact(self,direction,historyStr):
        outgoingDirections=self.interactionDict[direction]
        historyIndex=historyStr.find(self.gridPositionStr)
        partOfCycle=False
        if historyIndex!=-1: #check if the mirror/splitter is part of a cycle/loop
            for outgoingDirection in outgoingDirections:
                nextBeamInteracter=self.neighboringBeamInteractorDict[outgoingDirection]
                if nextBeamInteracter!=None:
                    #check that next mirror/splitter is not the same and entered in the same direction as the next one would be
                    if historyStr.find(nextBeamInteracter.gridPositionStr)==historyIndex+len(self.gridPositionStr+outgoingDirection):
                        partOfCycle=True
        if historyStr not in self.historyStrSet and not partOfCycle:
            if len(outgoingDirections)==2:
                if historyStr!='':
                    self.historyStrSet.add(historyStr)
                outgoingHistoryStrs=[self.gridPositionStr,self.gridPositionStr]
            else:
                outgoingHistoryStrs=[historyStr+self.gridPositionStr]
            for outgoingDirection,historyStr_ in zip(outgoingDirections,outgoingHistoryStrs):            
                nextBeamInteracter=self.neighboringBeamInteractorDict[outgoingDirection]
                if nextBeamInteracter!=None:
                    self.beamQueue.append((outgoingDirection,historyStr_+outgoingDirection,nextBeamInteracter))
                passingGridPoints=self.gridPointDict[outgoingDirection]
                for gridPoint in passingGridPoints:
                    self.energizedGridPointSet.add(gridPoint)
    def addNeighboringBeamInteracter(self,neighboringBeamInteractor,direction):
        self.neighboringBeamInteractorDict[direction]=neighboringBeamInteractor
    def addGridPoints(self,gridPoints,direction):
        self.gridPointDict[direction]+=gridPoints

#dictionary containing dictionaries with instructions on how to re-direct light for each type of mirror/splitter
interactionDictsDict=dict()
interactionDictsDict['/']={'north':['east'],'east':['north'],'south':['west'],'west':['south']}
interactionDictsDict['\\']={'north':['west'],'east':['south'],'south':['east'],'west':['north']}
interactionDictsDict['-']={'north':['west','east'],'east':['east'],'south':['west','east'],'west':['west']}
interactionDictsDict['|']={'north':['north'],'east':['north','south'],'south':['south'],'west':['north','south']}

Ncol=len(inputStrList[0])
energizedGridPointSet=set() #keep track of unique energized points
historyStrSet=set() #keep track of unique histories/paths
beamInteracterRowList=[[] for _ in range(len(inputStrList))]
beamInteracterColList=[[] for _ in range(Ncol)]
northBeamInteracters=[None for _ in range(Ncol)] #list to keep track of mirrors/splitters in each column on previous rows
accumulatedNorthGridPoints=[[] for _ in range(Ncol)] #list to keep track of grid points not yet assigned to a mirror/splitter in each column on previous rows
beamQueue=[]
#parsing: keep track of left-most mirror/splittr on each row and north-most mirror/splitter in every column and accumulate grid points until a mirror/splitter is encountered
#add accumulated grid points to the left and above for each encountered mirror/splitter and then put it as a new reference for left-most and north-most
#add accumulated grid points to the right and below for previous left-most and north-most references and also link new mirror/splitter as right/south of previous references and vice versa
for ir,row in enumerate(inputStrList):
    westBeamInteracter=None
    accumulatedGridPoints=[]
    for ic,col in enumerate(row):
        if col!='.':            
            newBeamInteracter=beamInteracter((ir,ic),interactionDictsDict[col],energizedGridPointSet,beamQueue,historyStrSet)
            newBeamInteracter.addNeighboringBeamInteracter(westBeamInteracter,'west')
            newBeamInteracter.addNeighboringBeamInteracter(northBeamInteracters[ic],'north')
            newBeamInteracter.addGridPoints(accumulatedGridPoints,'west')
            newBeamInteracter.addGridPoints(accumulatedNorthGridPoints[ic],'north')
            if westBeamInteracter!=None:
                westBeamInteracter.addNeighboringBeamInteracter(newBeamInteracter,'east')
                westBeamInteracter.addGridPoints(accumulatedGridPoints,'east')
            if northBeamInteracters[ic]!=None:
                northBeamInteracters[ic].addNeighboringBeamInteracter(newBeamInteracter,'south')
                northBeamInteracters[ic].addGridPoints(accumulatedNorthGridPoints[ic],'south')
            westBeamInteracter=newBeamInteracter
            northBeamInteracters[ic]=newBeamInteracter
            accumulatedGridPoints=[]
            accumulatedNorthGridPoints[ic]=[]
            beamInteracterRowList[ir].append(newBeamInteracter)
            beamInteracterColList[ic].append(newBeamInteracter)
        else:
            accumulatedGridPoints.append((ir,ic))
            accumulatedNorthGridPoints[ic].append((ir,ic))
    if len(accumulatedGridPoints)!=0:
        if westBeamInteracter!=None:
            westBeamInteracter.addGridPoints(accumulatedGridPoints,'east')
for gridPoints,northBeamInteracter in zip(accumulatedNorthGridPoints,northBeamInteracters):
    if northBeamInteracter!=None:
        northBeamInteracter.addGridPoints(gridPoints,'south')


def calculateEnergizing(beamQueue,startDirection,firstEncounteredBeamInteracter,energizedGridPointSet,historyStrSet):
    #clear prior results and initiate a new starting point and direction
    beamQueue.clear()
    historyStrSet.clear()
    energizedGridPointSet.clear()
    beamQueue.append((startDirection,'',firstEncounteredBeamInteracter))
    oppositeDict={'north':'south','east':'west','south':'north','west':'east'}
    #add energized grid points until the new first mirror/splitter is encountered
    for gridPoint in firstEncounteredBeamInteracter.gridPointDict[oppositeDict[startDirection]]:
        energizedGridPointSet.add(gridPoint)
    #run loop until the beam queue is empty
    while len(beamQueue)!=0:
        currentDirection,currentHistoryStr,currentBeamInteracter=beamQueue.pop(0)
        if currentBeamInteracter!=None:
            currentBeamInteracter.interact(currentDirection,currentHistoryStr)
    return len(energizedGridPointSet)

#part 1
print('1st:',calculateEnergizing(beamQueue,'east',beamInteracterRowList[0][0],energizedGridPointSet,historyStrSet))

#part 2
leftEdge=[]
rightEdge=[]
for rowList in beamInteracterRowList:
    if len(rowList)!=0:
        leftEdge.append((rowList[0],'east'))
        rightEdge.append((rowList[-1],'west'))
topEdge=[]
botEdge=[]
for colList in beamInteracterColList:
    if len(colList)!=0:
        topEdge.append((colList[0],'south'))
        botEdge.append((colList[-1],'north'))
allEdges=topEdge+rightEdge+botEdge+leftEdge
energizingList=[]
for edgeInitiation in allEdges:
    firstEncounteredBeamInteracter,startDirection=edgeInitiation
    energizing=calculateEnergizing(beamQueue,startDirection,firstEncounteredBeamInteracter,energizedGridPointSet,historyStrSet)
    energizingList.append(energizing)
print('2nd:',np.max(energizingList))