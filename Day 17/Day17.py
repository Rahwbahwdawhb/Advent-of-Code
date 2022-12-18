from preload import input
# print(input)
# input='>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
input=input.strip()

#1st problem
from copy import deepcopy
import numpy as np

def getRock(prevRockNumber,height):
    match prevRockNumber:
        case 0:
            nextRock=[[3,height+2],[2,height+1],[3,height+1],[4,height+1],[3,height]]
            rockNumber=1
        case 1:
            nextRock=[[4,height+2],[4,height+1],[2,height],[3,height],[4,height]]
            rockNumber=2
        case 2:
            nextRock=[[2,height+3],[2,height+2],[2,height+1],[2,height]]
            rockNumber=3
        case 3:
            nextRock=[[2,height+1],[3,height+1],[2,height],[3,height]]
            rockNumber=4
        case 4:
            nextRock=[[2,height],[3,height],[4,height],[5,height]]          
            rockNumber=0
    rockX=np.array([x for x,_ in nextRock])
    rockY=np.array([y for _,y in nextRock])
    return rockNumber,rockX,rockY

maxJetIndex=len(input)-1

def getHeight(Nrocks,writeToFile):
    if len(writeToFile)!=0:
        file=open(writeToFile,'w')
    emptyRow=['.','.','.','.','.','.','.']
    occupiedDict=dict()
    occupiedDict[-1]=['#','#','#','#','#','#','#']
    maxHeight=-1
    rockNumber=4
    jetIndex=0
    heightEvolution=[]
    for mainIter in range(Nrocks):
        #create empty space
        spawnHeight=maxHeight
        for _ in range(4):
            spawnHeight+=1
            occupiedDict[spawnHeight]=deepcopy(emptyRow)        
        # maxHeight-=1
        #create falling rock
        rockNumber,rockX,rockY=getRock(rockNumber,spawnHeight)
        # print(rockNumber,rockX,rockY)
        canFall=True
        while canFall:
            match input[jetIndex]:
                case '<':
                    dx=-1
                case '>':
                    dx=+1
            jetIndex+=1
            if jetIndex>maxJetIndex:
                jetIndex=0
            bump=False
            if max(rockX)+dx<=6 and min(rockX)+dx>=0:
                for ind,x in enumerate(rockX):
                    if rockY[ind] in occupiedDict.keys():
                        if occupiedDict[rockY[ind]][x+dx]=='#':
                            bump=True
                            break
            else:
                bump=True
            if not bump:
                rockX+=dx
            for ind,x in enumerate(rockX):
                if rockY[ind] in occupiedDict.keys():
                    if occupiedDict[rockY[ind]-1][x]=='#':
                        canFall=False
                        break
            if canFall:
                rockY-=1
        for ind,x in enumerate(rockX):
            # if not rockY[ind] in occupiedDict.keys():
            #     occupiedDict[rockY[ind]]=deepcopy(emptyRow)
            occupiedDict[rockY[ind]][x]='#'
            if occupiedDict[rockY[ind]]==['#','#','#','#','#','#','#']:
                for delInd in range(min(occupiedDict.keys()),rockY[ind]-1,1):
                    del occupiedDict[delInd]
        maxHeight=max([maxHeight,max(rockY)])
        if len(writeToFile)!=0:
            file.write(str(mainIter)+','+str(maxHeight)+'\n')
        heightEvolution.append([mainIter+1,maxHeight+1])
    # print('')
    # rows=occupiedDict.keys()
    # for key in rows.__reversed__():
    #     print(occupiedDict[key])
    if len(writeToFile)!=0:
        file.close()
    return maxHeight+1,heightEvolution

height,_=getHeight(2022,[])
print('1st: ',height)

#"cheated" a bit by printing the contents in data.txt in MATLAB and saw the linear-like trend and then found this cyclic evolution implemented below
#had some issues with overflow and got negative value took some time to find that the int had to be declared with int64 from numpy: NcompleteCycles=np.int64((rocksToFall-refRocks)//rocksDuringCycle)
#2nd problem
rocksToFall=1000000000000

_,heightEvolution=getHeight(5000,'data.txt')
refRocks=2000
refHeight=heightEvolution[refRocks-1][1]
hVals=np.array([h for _,h in heightEvolution[refRocks-1:]])
refChunk=hVals[0:100]
for ii in range(1,4000,1):
    diffArr=hVals[0+ii:100+ii]-refChunk
    if np.all(diffArr==diffArr[0]):        
        break
rocksDuringCycle=ii
cycleHeight=diffArr[0]
NcompleteCycles=np.int64((rocksToFall-refRocks)//rocksDuringCycle)
NextraRocks=(rocksToFall-refRocks)%rocksDuringCycle
extraHeight=heightEvolution[refRocks-1+NextraRocks][1]-refHeight
finalHeight=refHeight+cycleHeight*NcompleteCycles+extraHeight
# print(cycleHeight,NcompleteCycles,NextraRocks)
# print([refHeight,cycleHeight*NcompleteCycles,extraHeight])
print('2nd: ',finalHeight)
# for nRocks,h in heightEvolution[refRocks:]:
1



# spawnHeight=max(heights)+4
# rockNumber,rockX,rockY=getRock(rockNumber,spawnHeight)
