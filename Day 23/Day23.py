from preload import input

# input=open('ex.txt').read()
# print(input)
inpList=input.strip().split('\n')

#1st problem
positions_0=[]
rowMin=len(inpList)
rowMax=0
colMin=len(inpList[0])
colMax=0
for i,inp in enumerate(inpList):
    for ii,ch in enumerate(inp):
        if ch=='#':
            positions_0.append((i,ii))
            rowMax=max([rowMax,i])
            rowMin=min([rowMin,i])
            colMax=max([colMax,ii])
            colMin=min([colMin,ii])

def printConfig(posIn,desiredRows,desiredCols):
    extraPad=4
    rowMax=max(posIn,key=lambda x:x[0])[0]
    rowMin=min(posIn,key=lambda x:x[0])[0]
    colMax=max(posIn,key=lambda x:x[1])[1]
    colMin=min(posIn,key=lambda x:x[1])[1]
    rowExt=rowMax-rowMin
    colExt=colMax-colMin
    padRow=['.' for _ in range(colExt+2*extraPad+1)]
    padRow=''.join(padRow)
    padPart=['.' for _ in range(extraPad)]
    padPart=''.join(padPart)
    field=[]
    for _ in range(extraPad):
        field.append(padRow)    
    for i in range(rowExt+1):
        rowStr=padPart
        for ii in range(colExt+1):
            if [rowMin+i,colMin+ii] in posIn:
                rowStr+='#'
            else:
                rowStr+='.'
        field.append(rowStr+padPart)
    for _ in range(extraPad):
        field.append(padRow)

    rowVals=[rowMin-(extraPad-i) for i in range(1,extraPad+1,1)]+[rowMin+i for i in range(rowExt+1)]+[rowMax+i for i in range(1,extraPad+1,1)]
    colVals=[colMin-(extraPad-i) for i in range(1,extraPad+1,1)]+[colMin+i for i in range(colExt+1)]+[colMax+i for i in range(1,extraPad+1,1)]
    if rowExt<desiredRows[1]-desiredRows[0]:
        field=field[rowVals.index(desiredRows[0]):rowVals.index(desiredRows[1])+1]
    if colExt<desiredCols[1]-desiredCols[0]:
        for i,row in enumerate(field):
            field[i]=row[colVals.index(desiredCols[0]):colVals.index(desiredCols[1])+1]
    fieldStr=''
    for row in field:
        fieldStr+=''.join(row)+'\n'
    return fieldStr

# print(printConfig(positions,[rowMin-1,rowMax+3],[colMin-2,colMax+4]))

checks=[]
checks.append([(-1,-1),(-1,0),(-1,1)]) #north
checks.append([(1,-1),(1,0),(1,1)]) #south
checks.append([(-1,-1),(0,-1),(1,-1)]) #west
checks.append([(-1,1),(0,1),(1,1)]) #east

from collections import Counter
def elfRound(positions,checks):
    potentialPos=[]
    doesNotMove=0
    for i,pos in enumerate(positions):
        cannotMoveInDirs=0
        considerDirection=3
        for ii,posAdjusters in enumerate(checks):
            couldMoveInDir=True
            for rowAdjust,colAdjust in posAdjusters:
                if (pos[0]+rowAdjust,pos[1]+colAdjust) in positions:
                    couldMoveInDir=False
                    break
            if couldMoveInDir:
                considerDirection=min([considerDirection,ii])
            else:
                cannotMoveInDirs+=1
        if cannotMoveInDirs==4 or cannotMoveInDirs==0:
            # potentialAdjustments.append((0,0))
            potentialPos.append(pos)
            doesNotMove+=1
        else:        
            # potentialAdjustments.append(posAdjusters[considerDirection])
            potentialPos.append((pos[0]+checks[considerDirection][1][0],pos[1]+checks[considerDirection][1][1]))

    positionCounts=Counter(potentialPos)
    for i,pos in enumerate(potentialPos):
        if positionCounts[pos]!=1:
            potentialPos[i]=positions[i]
    return potentialPos,doesNotMove
    #     1
    # checkPotentialPos=[p for p in potentialPos]
    # okPositions=[]    
    # while len(checkPotentialPos)!=0:
    #     toCheck=checkPotentialPos.pop(0)
    #     interestInPos=checkPotentialPos.count(toCheck)
    #     posHolder=[]
    #     if interestInPos!=0:
    #         for i,p in enumerate(checkPotentialPos):
    #             if p!=toCheck:
    #                 positions[i]=
    #         checkPotentialPos=[p for p in checkPotentialPos if p!=toCheck]
    #     else:
    #         okPositions.append(toCheck)
# potentialAdjustments=[]

positions=[p for p in positions_0]
for bigIter in range(10):
    positions,didNotMove=elfRound(positions,checks)
    checks=checks[1:]+[checks[0]]

rowMax_=max(positions,key=lambda x:x[0])[0]
rowMin_=min(positions,key=lambda x:x[0])[0]
colMax_=max(positions,key=lambda x:x[1])[1]
colMin_=min(positions,key=lambda x:x[1])[1]
Nelves=len(positions)
freeSquares=(rowMax_-rowMin_+1)*(colMax_-colMin_+1)-Nelves
print('1st: ',freeSquares)
1
#2nd problem

def elfRound_2(positions,checkOrder):
    posStep=[(-1,0),(1,0),(0,-1),(0,1)]
    wantedPos=[]
    proposedPos=set()
    checkedPos=set()
    while len(positions)!=0:
        posIter=positions.pop()        
        checkVals=[]
        for rowStep,colStep in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            temp=(posIter[0]+rowStep,posIter[1]+colStep)
            if temp in positions or temp in checkedPos:
                checkVals.append(1)
            else:
                checkVals.append(0)
        if sum(checkVals)==0:
            proposedPos.add((posIter,posIter))
            wantedPos.append(posIter)
        else:
            sumChecks=[sum(checkVals[0:3]),sum(checkVals[5:8]),checkVals[0]+checkVals[3]+checkVals[5],checkVals[2]+checkVals[4]+checkVals[7]]
            canMove=False
            for ch in checkOrder:
                if sumChecks[ch]==0:
                    canMove=True
                    break
            if canMove:
                proposedPos.add((posIter,(posStep[ch][0]+posIter[0],posStep[ch][1]+posIter[1])))
                wantedPos.append((posStep[ch][0]+posIter[0],posStep[ch][1]+posIter[1]))
            else:
                proposedPos.add((posIter,posIter))
                wantedPos.append(posIter)
        checkedPos.add(posIter)
    countDict=Counter(wantedPos)
    movedSum=0
    newPos=set()
    while len(proposedPos)!=0:
        currentPos,propPos=proposedPos.pop()
        if countDict[propPos]==1:
            newPos.add(propPos)
            if currentPos!=propPos:
                movedSum+=1
        else:
            newPos.add(currentPos)
    return newPos,movedSum

        # 1
        # checks.append([(-1,-1),(-1,0),(-1,1)]) #north
        # checks.append([(1,-1),(1,0),(1,1)]) #south
        # checks.append([(-1,-1),(0,-1),(1,-1)]) #west
        # checks.append([(-1,1),(0,1),(1,1)]) #east

#faster solution of the 1st problem
checkOrder=[0,1,2,3]
positions=[p for p in positions_0]
for bigIter in range(10):
    positions,moved=elfRound_2(positions,checkOrder)
    checkOrder=checkOrder[1:]+[checkOrder[0]]
    # print('')
    # print(printConfig([[row,col] for row,col in positions],[rowMin-1,rowMax+3],[colMin-2,colMax+4]))

rowMax_=max(positions,key=lambda x:x[0])[0]
rowMin_=min(positions,key=lambda x:x[0])[0]
colMax_=max(positions,key=lambda x:x[1])[1]
colMin_=min(positions,key=lambda x:x[1])[1]
Nelves=len(positions)
freeSquares=(rowMax_-rowMin_+1)*(colMax_-colMin_+1)-Nelves
print('1st: ',freeSquares)

bigIter2=0
while moved!=0:
    bigIter2+=1
    positions,moved=elfRound_2(positions,checkOrder)
    checkOrder=checkOrder[1:]+[checkOrder[0]]
print('2nd: ',bigIter+1+bigIter2)


