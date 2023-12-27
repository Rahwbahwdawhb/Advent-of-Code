import os
import numpy as np
import heapq
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

#main idea was to keep track of rows passed towards east and towards west separately, each direction was assigned a dictionary with columns as keys
#for each column key, a list in the form of a heap kept the row numbers associated with each column sorted
#with the dictionaries filled, one can for each column key subtract the row numbers from the east and west dictionaries in order
#(since the loop is closed each column will have at least 2 rows associated with it), the sorted row lists means that the subtraction
#gives the difference between the closest rows => inner points between them when adding +1 (since 0-3 corresponds to 0,1,2,3...)
#four special situations needed to be accounted for separately
#the function below handles each step and works for both part 1 and part 2, although quite slow for part 2 (takes about 2 minutes to get solutions for part 1 and part 2 with input)
#this version assumes clockwise circling around the loop which was the case for both the example and the input
def recordStep(movementDict,RL_dict,position,steps,oldODstep,direction,lastDirection,lastLR,extras_clockwise):
    drow,dcol=movementDict[direction]
    if direction=='R' or direction=='L': #check if current direction is towards east or west
        directionDict,directionMax=RL_dict[direction] #fetch the dictionary that corresponds to this direction
        if lastLR!=direction: #if the last west/east movement was to west and now is to east
            loopRange=range(int(steps)+1) #loop over all steps 

            if (lastLR=='L' and lastDirection=='D') or (lastLR=='R' and lastDirection=='U'): #special cases, if last west/east movement was to west followed by south and now to east, all but one of the points in the south movement will be lost since the start point when going to right again will be on a lower row which will be matched with a lower left going row, so adding these points. The 2nd condition has the same issue but now instead in the upward direction
                extras_clockwise+=oldODstep-1
                
        else: #if last east/west movement was to west now one is moving to west again, i.e. only a height change has been made since last west movement
            loopRange=range(1,int(steps)+1) #skip first step in loop as the row below for west moving will have the same column but a lower position (if the height has increased), and for east moving the previous row will be at a higher position if the height change was down
            if (direction=='R' and lastDirection=='U') or (direction=='L' and lastDirection=='D'): #for east movement, if the movement was up then the situation described in the comment above is not tru so the steps for the height increase must be added..the second conditions is the same but when having moved south for a west movement
                extras_clockwise+=oldODstep
                
        for i in loopRange:
            currentRow=i*drow+position[0]
            currentCol=i*dcol+position[1]
            RL_dict[direction][1]=max([directionMax,currentRow])
            if currentCol not in directionDict:
                directionDict[currentCol]=[currentRow]
                heapq.heapify(directionDict[currentCol])
            else:
                heapq.heappush(directionDict[currentCol],currentRow)
        lastLR=direction
    else:
        for i in range(int(steps)):
            currentRow=(i+1)*drow+position[0]
            currentCol=(i+1)*dcol+position[1]
            
        oldODstep=int(steps) #number of steps taken north or south
    position=(currentRow,currentCol) #update position
    return position,oldODstep,lastLR,extras_clockwise


movementDict={'R':[0,1],'L':[0,-1],'U':[1,0],'D':[-1,0]} #dictionary with row,column modifiers
dirDict={'0':'R','1':'D','2':'L','3':'U'} #dictionary to translate the directions in part 2

position_p1=(0,0)
RL_dict_p1={'R':[dict(),-1e9],'L':[dict(),-1e9]} #dictionaries for the columns as explained above and also max-values, was gonna use them to determine which direction dictionary to use as the "upper" one
lastLR_p1=''
extras_clockwise_p1=0
oldODstep_p1=1
lastDirection_p1=''
position_p2=(0,0)
RL_dict_p2={'R':[dict(),-1e9],'L':[dict(),-1e9]}
lastLR_p2=''
extras_clockwise_p2=0
oldODstep_p2=1
lastDirection_p2=''
for row in inputStrList:
    direction_p1,steps_p1,info=row.split(' ') #parsing for part 1

    #parsing for part 2
    info=info.strip('()')
    steps_p2=int(info[1:-1],16)
    direction_p2=dirDict[info[-1]]

    position_p1,oldODstep_p1,lastLR_p1,extras_clockwise_p1=recordStep(movementDict,RL_dict_p1,position_p1,steps_p1,oldODstep_p1,direction_p1,lastDirection_p1,lastLR_p1,extras_clockwise_p1)
    lastDirection_p1=direction_p1
    position_p2,oldODstep_p2,lastLR_p2,extras_clockwise_p2=recordStep(movementDict,RL_dict_p2,position_p2,steps_p2,oldODstep_p2,direction_p2,lastDirection_p2,lastLR_p2,extras_clockwise_p2)
    lastDirection_p2=direction_p2

def getCubicMeters(upperDict,lowerDict,extras_clockwise):
    cubicMeters=0
    for col in upperDict.keys():
        for upperRow,lowerRow in zip(upperDict[col],lowerDict[col]):
            cubicMeters+=upperRow-lowerRow+1
    return cubicMeters+extras_clockwise

print('1st:',getCubicMeters(RL_dict_p1['R'][0],RL_dict_p1['L'][0],extras_clockwise_p1))
print('2nd:',getCubicMeters(RL_dict_p2['R'][0],RL_dict_p2['L'][0],extras_clockwise_p2))



# #initial stuff, first part same as above, checks with adding points to set (unsure why this does not give the same result) and using flood fill (gives the same result but will only work on part 1)
# loop=[]
# position=(0,0)
# RL_dict={'R':[dict(),-1e9],'L':[dict(),-1e9]}
# lastLR=''
# extras_clockwise=0
# oldODstep=1
# lastDirection=''
# for row in inputStrList:
#     direction,steps,_=row.split(' ')
#     drow,dcol=movementDict[direction]

#     if direction=='R' or direction=='L':
#         directionDict,directionMax=RL_dict[direction]
#         if lastLR!=direction:
#             loopRange=range(int(steps)+1)

#             if (lastLR=='L' and lastDirection=='D') or (lastLR=='R' and lastDirection=='U'):
#                 extras_clockwise+=oldODstep-1
                
#         else:
#             loopRange=range(1,int(steps)+1)
#             if (direction=='R' and lastDirection=='U') or (direction=='L' and lastDirection=='D'):
#                 extras_clockwise+=oldODstep
                
#         for i in loopRange:
#             currentRow=i*drow+position[0]
#             currentCol=i*dcol+position[1]
#             RL_dict[direction][1]=max([directionMax,currentRow])
#             loop.append((currentRow,currentCol))
#             if currentCol not in directionDict:
#                 directionDict[currentCol]=[currentRow]
#                 heapq.heapify(directionDict[currentCol])
#             else:
#                 heapq.heappush(directionDict[currentCol],currentRow)
#         lastLR=direction
#     else:
#         for i in range(int(steps)):
#             currentRow=(i+1)*drow+position[0]
#             currentCol=(i+1)*dcol+position[1]
#             loop.append((currentRow,currentCol))
#         oldODstep=int(steps)
#     position=(currentRow,currentCol)
#     lastDirection=direction

# #initially thought that the direction that the loop was circled had to be checked, input and example were in the same directions
# Rmax=RL_dict['R'][1]
# Lmax=RL_dict['L'][1]
# if Rmax>Lmax:
#     upperDict=RL_dict['R'][0]
#     lowerDict=RL_dict['L'][0]
# else:
#     upperDict=RL_dict['L'][0]
#     lowerDict=RL_dict['R'][0]
    
# cubicMeters=0
# lagoonPoints=set(loop)
# for col in upperDict.keys():
#     for upperRow,lowerRow in zip(upperDict[col],lowerDict[col]):
#         for r in range(lowerRow,upperRow+1):        
#             lagoonPoints.add((r,col))
#         cubicMeters+=upperRow-lowerRow+1
#         # print(col,upperRow-lowerRow+1)
#         # cubicMeters+=lowerRow-upperRow+1
# print(len(lagoonPoints)) #feels like this should be the same, set contains points that make up perimeter (from parsing) and from loop above also inner points
# print(cubicMeters,cubicMeters+extras_clockwise,extras_clockwise)

# #generate 2D-grid representation
# rows=[y for y,_ in lagoonPoints]
# cols=[x for _,x in lagoonPoints]
# rows_ref=np.linspace(min(rows),max(rows),max(rows)-min(rows)+1).astype(int)
# cols_ref=np.linspace(min(cols),max(cols),max(cols)-min(cols)+1).astype(int)
# grid=np.zeros((len(rows_ref),len(cols_ref)))
# for i,position in enumerate(lagoonPoints):
#     if position==(0,0):
#         # print('hej')
#         grid[list(rows_ref).index(position[0]),list(cols_ref).index(position[1])]=2
#     else:
#         grid[list(rows_ref).index(position[0]),list(cols_ref).index(position[1])]=1

# # import matplotlib.pyplot as plt
# #flood fill
# loopSet=set(loop)
# insidePoints=set()
# searchQueue=set([(-1,1)])
# visited=set()
# while len(searchQueue)!=0:
#     currentPoint=searchQueue.pop()
#     visited.add(currentPoint)
#     for dDir in [(-1,0),(1,0),(0,1),(0,-1)]:
#         nextPoint=(currentPoint[0]+dDir[0],currentPoint[1]+dDir[1])
#         if nextPoint in loopSet:
#             continue
#         else:
#             if (nextPoint not in searchQueue) and (nextPoint not in visited):
#                 searchQueue.add(nextPoint)
#                 insidePoints.add(nextPoint)
#             # plt.clf()
#             # plt.imshow(grid[::-1,:],extent=[min(cols_ref),max(cols_ref),min(rows_ref),max(rows_ref)])
#             # plt.plot(nextPoint[1],nextPoint[0],'xr')
#             # plt.savefig('temp.png')
#             # if (nextPoint not in insidePoints) and (nextPoint not in searchQueue):
#             #     searchQueue.append(nextPoint)
#             #     insidePoints.append(nextPoint)
# # print(len(insidePoints),len(set(insidePoints)))
# print(len(loopSet)+len(insidePoints)+1)

# 1
# #generated string output for visualization at one point
# # gridStr=''
# # for row in grid:    
# #     for col in row:
# #         if col==1:
# #             gridStr+='#'
# #         elif col==2:
# #             gridStr+='X'
# #         else:
# #             gridStr+='.'
# #     gridStr+='\n'
# # print(gridStr)
