import os
os.chdir(os.path.dirname(__file__))
# file='input.txt'
file='example.txt'
with open(file) as f:
    data=f.read().strip()
idList=[]
spaceListIndices=[]
fileID=0
currentIndex=0

spaceDict={} #for part 2, store indices for spaces of all sizes

spaceListIndicesSlots=[]
spaceListIndicesRanges=[]
occupiedSlots=[] #how many blocks each file occupies
occupiedRanges=[] #the corresponding indices
occupiedIds=[] #the corresponding IDs
for i in range(0,len(data)-1,2):
    occupiedRanges_=[]
    occupiedSlots.append(int(data[i]))
    occupiedIds.append(fileID)
    for _ in range(int(data[i])):
        idList.append([int(fileID),currentIndex])
        occupiedRanges_.append(currentIndex)
        currentIndex+=1
    occupiedRanges.append(occupiedRanges_+[])
    spaceListIndicesSlots.append(int(data[i+1]))
    spaceIndices_=[]
    for _ in range(int(data[i+1])):
        spaceListIndices.append(currentIndex)
        spaceIndices_.append(currentIndex)
        currentIndex+=1
    spaceListIndicesRanges.append(spaceIndices_)
    try: 
        spaceDict[int(data[i+1])].append(spaceIndices_+[])
    except:
        spaceDict[int(data[i+1])]=[spaceIndices_+[]]
    fileID+=1

if len(data)%2!=0: #necessary to not miss last value, could have looped through all elements and  checked i%2 to add spaces or blocks...
    occupiedRanges_=[]
    occupiedSlots.append(int(data[-1]))
    occupiedIds.append(fileID)
    for _ in range(int(data[-1])):
        idList.append([int(fileID),currentIndex])
        occupiedRanges_.append(currentIndex)
        currentIndex+=1
    occupiedRanges.append(occupiedRanges_+[])

def showStr(idList,cI):
    m=['.' for _ in range(cI)]
    for id,index in idList:
        m[index]=str(id)
    pStr=''.join(m)
    print(pStr)
    return pStr

movedFilesList=[]
while spaceListIndices:
    moveIndex=spaceListIndices.pop(0)
    fileToMove=idList.pop()
    if fileToMove[1]>moveIndex:
        movedFilesList.append([fileToMove[0],moveIndex])
    else: #keep moving file blocks until the index to move to exceeds the index of the block that is being moved (to stop when there are not gaps, continuing would introduce new gaps)
        idList.append(fileToMove)
        break
checksum=0
m=['.' for _ in range(currentIndex)]
for id,index in idList+movedFilesList:
    checksum+=id*index
    m[index]=str(id)
# showStr(idList+movedFilesList,currentIndex)
print('1st:',checksum)

#part 2
def showStrPart2(occupiedIds,occupiedRanges,cI):
    fullList=[]
    for id,oR in zip(occupiedIds,occupiedRanges):
        temp=[]
        for i in oR:
            temp.append([id,i])
        fullList+=temp
    return showStr(fullList,cI)
# showStrPart2(occupiedIds,occupiedRanges,currentIndex)
movedRanges=[]
movedIds=[]
nonMovedRanges=[]
nonMovedIds=[]
maxSpace=max(spaceDict.keys())
while occupiedSlots:
    oSlot=occupiedSlots.pop()
    oSlotRange=occupiedRanges.pop()
    oId=occupiedIds.pop()
    minIndex=currentIndex
    moveKey=None
    if oSlot>maxSpace:
        minIndex+=1
    for key in range(oSlot,maxSpace+1):
        try:
            leftmostSpace=spaceDict[key][0]
            if leftmostSpace[0]<minIndex:
                minIndex=leftmostSpace[0]
                moveKey=key
        except:
            pass
    if minIndex<oSlotRange[0]:
        if moveKey:
            moveIndices=spaceDict[moveKey].pop(0)
            if len(moveIndices)>oSlot:
                indicesLeft=moveIndices[oSlot:]
                moveIndices=moveIndices[:oSlot]
                N=len(indicesLeft)
                try:
                    stoppedBool=False
                    for i,s in enumerate(spaceDict[N]):
                        if indicesLeft[0]<s[0]:
                            stoppedBool=True
                            break
                    if stoppedBool:
                        spaceDict[N].insert(i,indicesLeft)
                    else:
                        spaceDict[N].append(indicesLeft)
                except:
                    spaceDict[N]=[indicesLeft]
                #move
            movedRanges.append(moveIndices)
            movedIds.append(oId)
    else:
        nonMovedRanges.append(oSlotRange)
        nonMovedIds.append(oId)
# showStrPart2(occupiedIds+movedIds+nonMovedIds,occupiedRanges+movedRanges+nonMovedRanges,currentIndex)
checksum_2=0
for id,oR in zip(occupiedIds+movedIds+nonMovedIds,occupiedRanges+movedRanges+nonMovedRanges):
    for i in oR:
        checksum_2+=id*i
print('2nd:',checksum_2)