import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

# #1st solution, part 1
# cubeRocks=[]
# roundRocks=[]
# Ncols=len(inputStrList[0])
# inputStrList.insert(0,'#'*Ncols)
# Nrows=len(inputStrList)
# for ic in range(Ncols):
#     cubeRocks.append([])
#     roundRocks.append([])
# for ir,row in enumerate(inputStrList):
#     # print(row)
#     for ic,col in enumerate(list(row)):
#         if col=='O':
#             roundRocks[ic].append(ir)
#         elif col=='#':
#             cubeRocks[ic].append(ir)
# # print(cubeRocks)
# # print(roundRocks)
# totalLoad=0
# for ic,(crs,rrs) in enumerate(zip(cubeRocks,roundRocks)):
#     columnLoad=0
#     rrs_=[]
#     while len(crs)!=0:
#         currentCubeRock=crs.pop(0)
#         try:
#             nextCubeRock=crs[0]
#         except:
#             nextCubeRock=np.inf
#             pass
#         relevantRoundRocks=[]
#         for icr,currentRoundRock in enumerate(rrs):
#             if currentRoundRock<nextCubeRock:
#                 relevantRoundRocks.append(currentCubeRock+1+icr)
#         rrs_+=relevantRoundRocks
#         for iter in range(len(relevantRoundRocks)):
#             columnLoad+=Nrows-(currentCubeRock+1)-iter
#             del rrs[0]
#     roundRocks[ic]=rrs_
#     totalLoad+=columnLoad
#     1
# # print(totalLoad)
    
#new solution working for part 1 and 2
#main idea:  
#replace grid with a zero matrix and give moving stones value of 1, cube rock positions are stored separately
#only look at slices between cube rocks in the matrix, the summation of this slice=number of moving stones
#move all the ones to pile up from the cube rock that the tilt is against
#store all moving positions after each tilt and check when all stone positions is repeated
#calculate cycle length for the positions to repeat
#then calculate how many complete cycles are passed for the remaining moves and how many moves that are left
#take the number of moves left in the stored position sequnce (after the index where it starts)
#reconstruct the grid and then calculate the total load
#-used dictionaries instead of if statements to avoid need for rewriting the same code in some places
padRow='#'*len(inputStrList[0])
inputStrList.insert(0,padRow)
inputStrList.append(padRow)
Nrows=len(inputStrList)
Ncols=len(padRow)+2
roundRocks=[]
cubeRocks_cols=[[] for _ in range(Ncols)]
cubeRocks_rows=[[] for _ in range(Nrows)]
roundRockGrid=np.zeros((Nrows,Ncols))
cubeRock_coordinates=[]
for ir,row in enumerate(inputStrList): #adding rocks to edges of grid to not have to treat edges differently
    row='#'+row+'#'
    for ic,col in enumerate(list(row)):
        if col=='O':
            roundRockGrid[ir,ic]=1
        elif col=='#':
            cubeRocks_cols[ic].append(ir)
            cubeRocks_rows[ir].append(ic)
            cubeRock_coordinates.append((ir,ic))

def getCubeRockSliceList(cubeRocksList): #create slices between cube rock pairs to not have to recreate slices each time with x[start:stop], the start:stop is replaced by the slice
    cubeRocksSlices=[]
    for cubeRocks in cubeRocksList:
        cubeRocks.sort()
        cubeRocks_slices=[slice(cubeRock,cubeRocks[i+1]+1,1) for i,cubeRock in enumerate(cubeRocks[0:-1])]
        cubeRocksSlices.append(cubeRocks_slices)
    return cubeRocksSlices
#functions generating round rock positions depending on tilt and their dictonairy
def westeastPositionList(containedRockRange,fromRowCol):
    return [(fromRowCol,iter) for iter in containedRockRange]
def northSouthPositionList(containedRockRange,fromRowCol):
    return [(iter,fromRowCol) for iter in containedRockRange]
positionStrDict={}
positionStrDict['northSouth']=northSouthPositionList
positionStrDict['westEast']=westeastPositionList
#functions adding rocks to beginning or end of considered grid slice
def first(currentSlice,iterSlice,rowCol,westeastNorthsouth,containedRoundRocks,idStr):
    currentSlice[1:containedRoundRocks+1]=1    
    positionList=positionStrDict[westeastNorthsouth](range(iterSlice.start+1,iterSlice.start+1+containedRoundRocks),rowCol)
    if len(positionList)>0:
        idStr+=str(positionList)
    return idStr
def last(currentSlice,iterSlice,rowCol,westeastNorthsouth,containedRoundRocks,idStr):
    currentSlice[-containedRoundRocks-1:-1]=1
    positionList=positionStrDict[westeastNorthsouth](range(iterSlice.stop-containedRoundRocks-1,iterSlice.stop-1),rowCol)
    if len(positionList)>0:
        idStr+=str(positionList)
    return idStr
firstLastDict={} #dictonairy holding above functions, returning the appropriate one
firstLastDict['first']=first
firstLastDict['last']=last
#functions adjusting rock positions depending on tilt and slide along rows or columns
def northSouthSlide(cubeRocksSlices_cols,roundRockGrid,firstLastStr,idStr):
    for ic,iterSlices in enumerate(cubeRocksSlices_cols[1:-1]):
        for iterSlice in iterSlices:
            currentSlice=roundRockGrid[iterSlice,ic+1]
            containedRoundRocks=int(np.sum(currentSlice))
            currentSlice*=0
            idStr=firstLastDict[firstLastStr](currentSlice,iterSlice,ic,'northSouth',containedRoundRocks,idStr)
    return idStr    
def westEastSlide(cubeRocksSlices_rows,roundRockGrid,firstLastStr,idStr):
    for ir,iterSlices in enumerate(cubeRocksSlices_rows[1:-1]):
        for iterSlice in iterSlices:
            currentSlice=roundRockGrid[ir+1,iterSlice]
            containedRoundRocks=int(np.sum(currentSlice))
            currentSlice*=0
            idStr=firstLastDict[firstLastStr](currentSlice,iterSlice,ir,'westEast',containedRoundRocks,idStr)
    return idStr

cubeRocksSlices_cols=getCubeRockSliceList(cubeRocks_cols)
cubeRocksSlices_rows=getCubeRockSliceList(cubeRocks_rows)

tiltDirectionSlideMatchDict=dict() #dictionary returning functions and keys to use for different tilts
tiltDirectionSlideMatchDict['north']=[cubeRocksSlices_cols,northSouthSlide,'first']
tiltDirectionSlideMatchDict['south']=[cubeRocksSlices_cols,northSouthSlide,'last']
tiltDirectionSlideMatchDict['west']=[cubeRocksSlices_rows,westEastSlide,'first']
tiltDirectionSlideMatchDict['east']=[cubeRocksSlices_rows,westEastSlide,'last']
#function to create character representation of rock distribution
def rockGridStr(roundRockGrid,cubeRock_coordinates):
    rockGridStr=''
    for ir,row in enumerate(roundRockGrid):
        for ic,value in enumerate(row):
            if value==0:
                if (ir,ic) in cubeRock_coordinates:
                    rockGridStr+='#'
                else:
                    rockGridStr+='.'
            elif value==1:
                rockGridStr+='O'
        rockGridStr+='\n'
    return rockGridStr

#quick check 1 with example input
# idStrs=[]
# for tiltDirection in ['north','east','south','west']:
#     roundRockGrid_iter=roundRockGrid+0
#     cubeRocksSlices,slideFunction,firstLast=tiltDirectionSlideMatchDict[tiltDirection]
#     idStr_iter=slideFunction(cubeRocksSlices,roundRockGrid_iter,firstLast,'')
#     idStrs.append(idStr_iter)
#     print(rockGridStr(roundRockGrid_iter,cubeRock_coordinates))
#quick check 2 with example
# roundRockGrid_iter=roundRockGrid+0
# idStrs=[]
# for _ in range(3):
#     for tiltDirection in ['north','west','south','east']:        
#         cubeRocksSlices,slideFunction,firstLast=tiltDirectionSlideMatchDict[tiltDirection]
#         idStr_iter=slideFunction(cubeRocksSlices,roundRockGrid_iter,firstLast,'')
#         idStrs.append(idStr_iter)
#     print(rockGridStr(roundRockGrid_iter,cubeRock_coordinates))
roundRockGrid_iter=roundRockGrid+0
idStrs=[]
idStr_iter=''
loopOuter=True
while loopOuter:
    for tiltDirection in ['north','west','south','east']:   
        cubeRocksSlices,slideFunction,firstLast=tiltDirectionSlideMatchDict[tiltDirection]
        idStr_iter=slideFunction(cubeRocksSlices,roundRockGrid_iter,firstLast,'')
        if idStr_iter in idStrs:
            loopOuter=False
            break
        idStrs.append(idStr_iter)
idStrs.append(idStr_iter)
numberOfTilts=len(idStrs)
bigCycleStartIndex=idStrs.index(idStr_iter)
bigCycleLength=numberOfTilts-1-bigCycleStartIndex
totalCycles=1000000000
numberOfTiltsToGo=totalCycles*4-numberOfTilts
numberOfFullBigCycles=numberOfTiltsToGo//bigCycleLength
stepsWithinLastCycle=numberOfTiltsToGo-numberOfFullBigCycles*bigCycleLength
idStr_afterAllTilts=idStrs[bigCycleStartIndex+stepsWithinLastCycle-1]

def reconstructGrid(idStr_toReconstructFrom,roundRockGrid):    
    rockGrid_reconstructed=roundRockGrid*0
    idStrSplitList=idStr_toReconstructFrom.replace('][',',').replace(' ','').strip('[]').split('),(')
    idStrSplitList[0]=idStrSplitList[0][1:]
    idStrSplitList[-1]=idStrSplitList[-1][0:-1]
    for roundRock_coordinatesStr in idStrSplitList:
        rowStr,colStr=roundRock_coordinatesStr.split(',')
        rockGrid_reconstructed[int(rowStr),int(colStr)+1]=1
    return rockGrid_reconstructed
def totalLoadFromGrid(roundRockGrid,Nrows):
    totalLoad=0
    for roundRock in np.argwhere(roundRockGrid==1):
        totalLoad+=Nrows-1-roundRock[0]
    return totalLoad

rockGrid_afterFirstTilt=reconstructGrid(idStrs[0],roundRockGrid)
totalLoad_afterFirstTilt=totalLoadFromGrid(rockGrid_afterFirstTilt,Nrows)
rockGrid_afterAllTilts=reconstructGrid(idStr_afterAllTilts,roundRockGrid)
totalLoad_afterAllTilts=totalLoadFromGrid(rockGrid_afterAllTilts,Nrows)
print('1st:',totalLoad_afterFirstTilt)
print('2nd:',totalLoad_afterAllTilts)

