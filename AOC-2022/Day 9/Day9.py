from preload import input
# print(input)

#1st problem
# input='R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2'
inpList=input.split('\n')
inpList=inpList[:-1]
# print(inpList)
currentHeadPos=(0,0)
currentTailPos=currentHeadPos
uniqueTailPos=[currentHeadPos]
for move in inpList:
    direction,length=move.split(' ')
    for it in range(int(length)):
        if direction=='R':
            currentHeadPos=(currentHeadPos[0]+1,currentHeadPos[1])
        elif direction=='L':
            currentHeadPos=(currentHeadPos[0]-1,currentHeadPos[1])
        elif direction=='U':
            currentHeadPos=(currentHeadPos[0],currentHeadPos[1]+1)
        elif direction=='D':
            currentHeadPos=(currentHeadPos[0],currentHeadPos[1]-1)
        posDiff=(currentHeadPos[0]-currentTailPos[0],currentHeadPos[1]-currentTailPos[1])
        # currentTailPos=currentTailPos
        if posDiff[0]!=0 and posDiff[1]!=0:
            if abs(posDiff[1])>1 or abs(posDiff[0])>1:
                currentTailPos=(currentTailPos[0]+posDiff[0]//abs(posDiff[0]),currentTailPos[1]+posDiff[1]//abs(posDiff[1]))
            # if abs(posDiff[0])>1:
            #     currentTailPos=(currentTailPos[0]+int(posDiff[0]/abs(posDiff[0])),currentTailPos[1])    
        else:
            if posDiff[0]==0:
                if abs(posDiff[1])>1:
                    currentTailPos=(currentTailPos[0],currentTailPos[1]+posDiff[1]//abs(posDiff[1]))
            else:
                if abs(posDiff[0])>1:
                    currentTailPos=(currentTailPos[0]+posDiff[0]//abs(posDiff[0]),currentTailPos[1])    
        # print(currentTailPos)
        if currentTailPos not in uniqueTailPos:
            uniqueTailPos.append(currentTailPos)
# for pos in uniqueTailPos:
#     print(pos)
print('1st: ',len(uniqueTailPos))

#2nd problem

def knotMove(direction,length,ropeKnotPos):
    movedTailPos=[]
    knotLast=len(ropeKnotsPos)-1
    for _ in range(int(length)):
        for it in range(knotLast+1):
            if it==0:
                currentHeadPos=ropeKnotsPos[it]
                if direction=='R':
                    currentHeadPos=(currentHeadPos[0]+1,currentHeadPos[1])
                elif direction=='L':
                    currentHeadPos=(currentHeadPos[0]-1,currentHeadPos[1])
                elif direction=='U':
                    currentHeadPos=(currentHeadPos[0],currentHeadPos[1]+1)
                elif direction=='D':
                    currentHeadPos=(currentHeadPos[0],currentHeadPos[1]-1)
                ropeKnotsPos[it]=currentHeadPos
            else:
                currentHeadPos=ropeKnotsPos[it-1]
                currentTailPos=ropeKnotsPos[it]
                # if direction=='R':
                #     currentHeadPos=(currentHeadPos[0]+1,currentHeadPos[1])
                # elif direction=='L':
                #     currentHeadPos=(currentHeadPos[0]-1,currentHeadPos[1])
                # elif direction=='U':
                #     currentHeadPos=(currentHeadPos[0],currentHeadPos[1]+1)
                # elif direction=='D':
                #     currentHeadPos=(currentHeadPos[0],currentHeadPos[1]-1)
                posDiff=(currentHeadPos[0]-currentTailPos[0],currentHeadPos[1]-currentTailPos[1])
                # currentTailPos=currentTailPos
                if posDiff[0]!=0 and posDiff[1]!=0:
                    if abs(posDiff[1])>1 or abs(posDiff[0])>1:
                        currentTailPos=(currentTailPos[0]+posDiff[0]//abs(posDiff[0]),currentTailPos[1]+posDiff[1]//abs(posDiff[1]))
                        # movedTailPos.append(currentTailPos)
                    # if abs(posDiff[0])>1:
                    #     currentTailPos=(currentTailPos[0]+int(posDiff[0]/abs(posDiff[0])),currentTailPos[1])    
                else:
                    if posDiff[0]==0:
                        if abs(posDiff[1])>1:
                            currentTailPos=(currentTailPos[0],currentTailPos[1]+posDiff[1]//abs(posDiff[1]))
                            # movedTailPos.append(currentTailPos)
                    else:
                        if abs(posDiff[0])>1:
                            currentTailPos=(currentTailPos[0]+posDiff[0]//abs(posDiff[0]),currentTailPos[1])    
                if it==knotLast:
                    movedTailPos.append(currentTailPos)
                ropeKnotsPos[it]=currentTailPos
    return ropeKnotPos,movedTailPos

ropeKnotsPos=[]
for it in range(10):
    ropeKnotsPos.append((0,0))
# currentHeadPos=(0,0)
currentTailPos=(0,0)
uniqueTailPos=[currentTailPos]
for move in inpList:
    direction,length=move.split(' ')
    ropeKnotsPos,movedTailPos=knotMove(direction,length,ropeKnotsPos)
    for pos in movedTailPos:
        if pos not in uniqueTailPos:
            uniqueTailPos.append(pos)
print('2nd: ',len(uniqueTailPos))