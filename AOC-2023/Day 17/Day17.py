import os
import numpy as np
import bisect
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

#main idea was to the let nodes/city blocks add paths to the path queue
#the main challenge was to realize that one needed to add paths to queue based on accumulated weight AND the direction of entry AND number of steps taken in that direction
#this was necessary to allow the same node/city tile to be passed in multiple ways
#In hindsight it might have been worth trying to only account for accumulated weight AND number of steps taken in that direction but I first investigated the direction and then added the number of steps...

directions=['north','east','south','west']
class cityBlock: #base class, only works for part 1
    def __init__(self,heatLoss,pathQueue,position):
        self.heatLoss=heatLoss
        self.pathQueue=pathQueue
        self.position=position
        self.leastAccumulatedWeightDict=dict()
        self.neighborDict=dict()
        self.differentDirectionsDict=dict()
        self.differentDirectionsDict['north']=['west','east']
        self.differentDirectionsDict['south']=['west','east']
        self.differentDirectionsDict['west']=['north','south']
        self.differentDirectionsDict['east']=['north','south']
        self.straightDirectionDict=dict()
        self.straightDirectionDict['north']=['north']
        self.straightDirectionDict['south']=['south']
        self.straightDirectionDict['east']=['east']
        self.straightDirectionDict['west']=['west']
        for direction in directions:
            self.neighborDict[direction]=None
            for i in range(4):
                self.leastAccumulatedWeightDict[(direction,i)]=[np.inf,[]]
    def addNeighboringCityBlock(self,direction,cityBlock):
        self.neighborDict[direction]=cityBlock
    def assignWeight(self,goalPosition):
        self.weight=np.sum(np.abs(goalPosition-self.position))*0+self.heatLoss #tried using A* but did not work well unless the weight for the positional contribution was optimized
    def initializeCityBlock(self,goalPosition):
        self.assignWeight(goalPosition)
        directionsToRemove=[]
        for direction in directions: #find neighbors outside the grid
            if self.neighborDict[direction]==None:
                directionsToRemove.append(direction)        
        for direction_ in directionsToRemove: #remove possibility of adding "none" neighbors outside the city grid to the path queue
            del self.straightDirectionDict[direction_]
            for direction in directions:            
                try:
                    self.differentDirectionsDict[direction].remove(direction_)
                except:
                    pass
            
    def stepIntoCityBlock(self,direction,stepsInDirection,accumulatedWeight,priorPath):        
        possibleDirections=self.differentDirectionsDict[direction] #get valid directions not in current direction
        for possibleDirection in possibleDirections:
            self.addToPathQueue(possibleDirection,1,accumulatedWeight,priorPath+[self.position])
        if stepsInDirection<3:
            try:
                possibleDirections=self.straightDirectionDict[direction] #get the same as the current direction if it is valid
                for possibleDirection in possibleDirections:
                    self.addToPathQueue(possibleDirection,stepsInDirection+1,accumulatedWeight,priorPath+[self.position])
            except:
                pass #if the direction is not valid nothing will be added to the path queue
    def addToPathQueue(self,possibleDirection,nextStepCount,accumulatedWeight,path):
        nextCityBlock=self.neighborDict[possibleDirection] #fetch relevant neighbor
        nextAccumulatedWeight=nextCityBlock.weight+accumulatedWeight #calculate the weight that would be accumulated if stepping to this neighbor
        if nextCityBlock.leastAccumulatedWeightDict[(possibleDirection,nextStepCount)][0]>nextAccumulatedWeight: #check that there has not been any prior move to the relevant neighbor in the same direction and the same amount of accumulated steps with a lower accumulated weight, if so don't add this path to queue
            nextCityBlock.leastAccumulatedWeightDict[(possibleDirection,nextStepCount)]=[nextAccumulatedWeight,path] #update lowest value and corresponding path
            if len(self.pathQueue)==0:
                self.pathQueue.append((nextAccumulatedWeight,nextCityBlock,nextStepCount,possibleDirection,path))
            elif nextAccumulatedWeight<=self.pathQueue[0][0]:
                self.pathQueue.insert(0,(nextAccumulatedWeight,nextCityBlock,nextStepCount,possibleDirection,path))
            elif nextAccumulatedWeight>=self.pathQueue[-1][0]:
                self.pathQueue.append((nextAccumulatedWeight,nextCityBlock,nextStepCount,possibleDirection,path))
            else:
                #insert this new path into the path queue such that it remains ordered with the lowest accumulated weights first
                #this is done by checking the accumulated weight at the midpoint between lower and upper references indices, which are updated based on if the midpoint is lower or higher than the accumulated weight to insert
                lowerEnd=0
                upperEnd=len(self.pathQueue)
                checkIndex_old=0
                checkIndex=1
                while checkIndex_old!=checkIndex:
                    checkIndex_old=checkIndex
                    checkIndex=(upperEnd-lowerEnd)//2+lowerEnd
                    if nextAccumulatedWeight<self.pathQueue[checkIndex][0]:
                        upperEnd=checkIndex
                    else:
                        lowerEnd=checkIndex+1
                self.pathQueue.insert(checkIndex,(nextAccumulatedWeight,nextCityBlock,nextStepCount,possibleDirection,path))

class cityBlock_part2(cityBlock): #modified inherited version of cityBlock for part 1
    def __init__(self,heatLoss,pathQueue,position):
        super(cityBlock_part2,self).__init__(heatLoss,pathQueue,position)
        self.heatLoss=heatLoss
        self.pathQueue=pathQueue
        self.position=position
        self.leastAccumulatedWeightDict=dict()
        self.neighborDict=dict()
        for direction in directions:
            self.neighborDict[direction]=None
            for i in range(11): #the step dictionary must now have values up to 10
                self.leastAccumulatedWeightDict[(direction,i)]=[np.inf,[]]
    def stepIntoCityBlock(self,direction,stepsInDirection,accumulatedWeight,priorPath):        
        possibleDirections=self.differentDirectionsDict[direction]
        #these two if-statements apply the new rules for moving
        if stepsInDirection<10:
            if stepsInDirection>=4:
                for possibleDirection in possibleDirections:
                    self.addToPathQueue(possibleDirection,1,accumulatedWeight,priorPath+[self.position])
            try:
                possibleDirections=self.straightDirectionDict[direction]
                for possibleDirection in possibleDirections:
                    self.addToPathQueue(possibleDirection,stepsInDirection+1,accumulatedWeight,priorPath+[self.position])
            except:
                pass
        else:
            for possibleDirection in possibleDirections:
                self.addToPathQueue(possibleDirection,1,accumulatedWeight,priorPath+[self.position])

def initializeCity(inputStrList,cityBlockClass):
    Ncol=len(inputStrList[0])
    Nrow=len(inputStrList)
    topCityBlocks=[None for _ in range(Ncol)] #keep track of city blocks from previous rows
    cityBlockList=[]
    pathQueue=[]
    heatLossGrid=np.zeros((Nrow,Ncol)).astype(int)
    for ir,row in enumerate(inputStrList):
        leftCityBlock=None #keep track of previous city block on the row
        for ic,col in enumerate(row):
            newCityBlock=cityBlockClass(int(col),pathQueue,np.array([ir,ic]).astype(int))
            #assign neighbors to adjacent city blocks
            newCityBlock.addNeighboringCityBlock('west',leftCityBlock)
            newCityBlock.addNeighboringCityBlock('north',topCityBlocks[ic])
            if leftCityBlock!=None:
                leftCityBlock.addNeighboringCityBlock('east',newCityBlock)
            if topCityBlocks[ic]!=None:
                topCityBlocks[ic].addNeighboringCityBlock('south',newCityBlock)
            #update the city block references to the new city block
            topCityBlocks[ic]=newCityBlock
            leftCityBlock=newCityBlock
            cityBlockList.append(newCityBlock)
            heatLossGrid[ir,ic]=int(col)
    return cityBlockList,pathQueue,heatLossGrid

def pathThroughCity(startCityBlock,startDirection,goalCityBlock,cityBlockList,pathQueue,heatLossGrid):
    goalPosition=goalCityBlock.position
    for cityBlock_ in cityBlockList:
        cityBlock_.initializeCityBlock(goalPosition)
    currentCityBlock=startCityBlock
    currentCityBlock.stepIntoCityBlock(startDirection,0,0,[])

    # counter=0
    while len(pathQueue)!=0:
        # counter+=1
        currentAccumulatedWeight,currentCityBlock,currentStepCount,currentDirection,currentPath=pathQueue.pop(0)
        currentCityBlock.stepIntoCityBlock(currentDirection,currentStepCount,currentAccumulatedWeight,currentPath)
    leastAccumulatedWeights=[]
    leastAccumulatedWeights_keys=list(goalCityBlock.leastAccumulatedWeightDict.keys())
    for key in leastAccumulatedWeights_keys:
        leastAccumulatedWeights.append(goalCityBlock.leastAccumulatedWeightDict[key][0])
    return min(leastAccumulatedWeights)
    #this part would have been necessary with A*
    minimumKey=leastAccumulatedWeights_keys[np.argmin(leastAccumulatedWeights)] 
    minimumPath=goalCityBlock.leastAccumulatedWeightDict[minimumKey][-1]
    totalHeatLoss=0
    for position in minimumPath[1:]: #
        totalHeatLoss+=heatLossGrid[position[0],position[1]]
    return totalHeatLoss+goalCityBlock.heatLoss #last cityBlock's heat loss will not have been added during loop

cityBlockList_part1,pathQueue_part1,heatLossGrid=initializeCity(inputStrList,cityBlock)
cityBlockList_part2,pathQueue_part2,_=initializeCity(inputStrList,cityBlock_part2)
minimumHeatLoss_part1=pathThroughCity(startCityBlock=cityBlockList_part1[0],startDirection='east',goalCityBlock=cityBlockList_part1[-1],cityBlockList=cityBlockList_part1,pathQueue=pathQueue_part1,heatLossGrid=heatLossGrid)
minimumHeatLoss_part2=pathThroughCity(startCityBlock=cityBlockList_part2[0],startDirection='east',goalCityBlock=cityBlockList_part2[-1],cityBlockList=cityBlockList_part2,pathQueue=pathQueue_part2,heatLossGrid=heatLossGrid)
print('1st:',minimumHeatLoss_part1)
print('2nd:',minimumHeatLoss_part2)