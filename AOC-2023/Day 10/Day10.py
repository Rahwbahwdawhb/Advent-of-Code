import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
# fileName='example2a.txt'
# fileName='example2b.txt'
# fileName='example2c.txt'
# fileName='example2d.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

grid=[]
for i,row in enumerate(inputStrList):
    grid.append(list(row))
    if 'S' in row:
        startPoint=np.array([i,row.index('S')])

enterPoint1=np.array([startPoint[0],startPoint[1]-1])
enterPoint2=np.array([startPoint[0]-1,startPoint[1]])

#dict for how pipes re-direct depending direction they are entered from
moveDict={}
pipeCharacters=['|','-','L','J','7','F']
indexChanges=[[[1,0],[-1,0]],[[0,1],[0,-1]],[[]]]
moveDict['|']={'up':[np.array([-1,0]),'up'],'down':[np.array([1,0]),'down']}
moveDict['-']={'left':[np.array([0,-1]),'left'],'right':[np.array([0,1]),'right']}
moveDict['L']={'down':[np.array([0,1]),'right'],'left':[np.array([-1,0]),'up']}
moveDict['J']={'right':[np.array([-1,0]),'up'],'down':[np.array([0,-1]),'left']}
moveDict['7']={'right':[np.array([1,0]),'down'],'up':[np.array([0,-1]),'left']}
moveDict['F']={'left':[np.array([1,0]),'down'],'up':[np.array([0,1]),'right']}

startPoints=[] #where to start going through loop
startDirections=[]
startModifiers=[np.array([1,0]),np.array([-1,0]),np.array([0,1]),np.array([0,-1])] #check if can make valid moves down, up, right and left
rowLimit=len(grid)
columnLimit=len(grid[0])
for modifier,direction in zip(startModifiers,['down','up','right','left']):
    testPoint=startPoint+modifier
    if testPoint[0]>=0 and testPoint[0]<rowLimit and testPoint[1]>=0 and testPoint[1]<columnLimit:
        testCharacter=grid[testPoint[0]][testPoint[1]]
        try: #if the pipe adjacent to the starting points is not oriented appropriately, it will not be added as a start point
            moveDict[testCharacter][direction]
            startPoints.append(testPoint+0)
            startDirections.append(direction+'')            
        except:
            pass
#turns out that only two start points are ever added (no dead-ends), so one can start at both ends and go on until they meet
currentPositions=[sp+0 for sp in startPoints]
currentDirections=[sd+'' for sd in startDirections]
counter=1 #the searches will start at the pipes adjacent to the start point, so one step has already been taken
histories=[[[startPoints[0]+0,startDirections[0]+'']],[[startPoints[1]+0,startDirections[1]+'']]]
# pipesInLoop=[startPoint,histories[0][0][0]+0,histories[1][0][0]+0]
while sum(currentPositions[0]!=currentPositions[1])!=0:
    counter+=1
    for i,(position,direction) in enumerate(zip(currentPositions,currentDirections)):
        currentCharacter=grid[position[0]][position[1]]
        positionModifier,newDirection=moveDict[currentCharacter][direction]
        currentPositions[i]+=positionModifier
        currentDirections[i]=newDirection
        # pipesInLoop.append(currentPositions[i]+0)
        histories[i].append([currentPositions[i]+0,''+newDirection])
print('1st:',counter)

# del pipesInLoop[-1]

# historySet=set()
# for h in histories[0]:
#     historySet.add((h[0][0],h[0][1],h[1]))
# pipesInLoop_rowSorted=sorted(pipesInLoop,key=lambda x:x[0])
# pipesInLoop_rowSorted_tuples=[(a,b) for a,b in pipesInLoop_rowSorted]
# pipesInLoop_columnSorted=sorted(pipesInLoop,key=lambda x:x[1])
# pipesInLoop_columnSorted_tuples=[(a,b) for a,b in pipesInLoop_columnSorted]

# trailSequence0=[(a[0],a[1]) for a,_ in histories[0]]
# trailSequence1=[(a[0],a[1]) for a,_ in histories[1]]
startPoint_tuple=(startPoint[0],startPoint[1])
trailSequence0=[]
trailSequence1=[]
allLoopPoints=[startPoint_tuple]
for h0,h1 in zip(histories[0],histories[1]):
    point0,_=h0
    point1,_=h1
    point0_tuple=(point0[0],point0[1])
    point1_tuple=(point1[0],point1[1])
    trailSequence0.append(point0_tuple)
    trailSequence1.append(point1_tuple)
    allLoopPoints.append(point0_tuple)
    allLoopPoints.append(point1_tuple)
loop_minRow=min([a for a,_ in allLoopPoints])
loopMinRow_minColumn=min([b for a,b in allLoopPoints if a==loop_minRow])
startPoint2=(loop_minRow,loopMinRow_minColumn)

if startPoint2 in trailSequence0:
    trailSequence=[startPoint_tuple]+trailSequence0+trailSequence1[::-1][1:]
else:
    trailSequence=[(startPoint[0],startPoint[1])]+trailSequence1+trailSequence0[::-1][1:]
refIndex=trailSequence.index(startPoint2)
trailSequence2=trailSequence[refIndex:]+trailSequence[:refIndex]
trailSequenceCheckDiff=np.array(trailSequence2[1])-np.array(trailSequence2[0])
if sum(trailSequenceCheckDiff==[0,1])!=2:
    trailSequence2=[trailSequence2[0]]+trailSequence2[::-1][:-1]

#go around loop clockwise and check points between current loop position and the first pipe along the direction that leads clockwise by 90 degrees
#since the loop is closed, this guarnatees to only check internal points
def findEnclosedPoints(currentPosition,positionModifier,trailSequence2):
    currentPosition_tuple=(currentPosition[0],currentPosition[1])
    relevantColumnPoints=[point for point in trailSequence2 if point[0]==currentPosition[0]]
    relevantColumnPoints=list(set(relevantColumnPoints))
    relevantColumnPoints.sort(key=lambda x:x[1])
    relevantRowPoints=[point for point in trailSequence2 if point[1]==currentPosition[1]]
    relevantRowPoints=list(set(relevantRowPoints))
    relevantRowPoints.sort(key=lambda x:x[0])
    index_check_column=relevantColumnPoints.index(currentPosition_tuple)
    index_check_row=relevantRowPoints.index(currentPosition_tuple)
    if sum(positionModifier==[0,1])==2: #moved right to get to current position, look down
        limitingDownPoint_row=relevantRowPoints[index_check_row+1][0]
        enclosedPoints=[(rowIndex,currentPosition[1]) for rowIndex in range(currentPosition[0],limitingDownPoint_row+1)]        
    elif sum(positionModifier==[0,-1])==2: #moved left to get to current position, look up
        limitingUpPoint_row=relevantRowPoints[index_check_row-1][0]
        enclosedPoints=[(rowIndex,currentPosition[1]) for rowIndex in range(limitingUpPoint_row,currentPosition[0]+1)]        
    elif sum(positionModifier==[-1,0])==2: #moved up to get to current position, look right
        limitingRightPoint_column=relevantColumnPoints[index_check_column+1][1]
        enclosedPoints=[(currentPosition[0],columnIndex) for columnIndex in range(currentPosition[1],limitingRightPoint_column+1)]
    elif sum(positionModifier==[1,0])==2: #moved down to get to current position, look left
        limitingLeftPoint_column=relevantColumnPoints[index_check_column-1][1]
        enclosedPoints=[(currentPosition[0],columnIndex) for columnIndex in range(limitingLeftPoint_column,currentPosition[1]+1)]
    return enclosedPoints

allEnclosedPoints=set() #only add unique inner points
previousPosition=trailSequence2[0]
lastPositionModifier=[0,0]
for iter,currentPosition in enumerate(trailSequence2[1:]):
    positionModifier=np.array(currentPosition)-np.array(previousPosition)
    enclosedPoints=findEnclosedPoints(currentPosition,positionModifier,trailSequence2)
    modifierComparisonBool=sum(positionModifier==lastPositionModifier)==2
    if not modifierComparisonBool and iter>0: #at bends, internal points will generally be missed as the direction leading by 90 degrees will advance forward (and not look for points in its direction at the bend), in such cases go back one step and check for inner points in this new direction
        enclosedPoints_extra=findEnclosedPoints(previousPosition,positionModifier,trailSequence2)
        enclosedPoints=enclosedPoints+enclosedPoints_extra
    for point in enclosedPoints:
        allEnclosedPoints.add(point)
    # grid visualization for debugging
    # for ir,r in enumerate(grid):
    #     rowStr=''
    #     for ic,c in enumerate(r):
    #         if (ir,ic)==(currentPosition[0],currentPosition[1]):
    #             rowStr+='X'
    #         else:
    #             # if (ir,ic) in pipesInLoop_rowSorted_tuples:
    #             #     rowStr+='x'
    #             # else:
    #             rowStr+=c
    #     print(rowStr)
    previousPosition=currentPosition
    lastPositionModifier=[pM+0 for pM in positionModifier]

counter=0
pipesInLoop_tuples_set=set(allLoopPoints)
enclosed=[]
for point in allEnclosedPoints:
    if point not in pipesInLoop_tuples_set:
        counter+=1
        enclosed.append(point)
print('2nd:',counter)
