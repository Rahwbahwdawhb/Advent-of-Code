from preload import input
import string
# print(input)

# input='Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi'

inpList=input.strip().split('\n')
low=string.ascii_lowercase
heightDict={}
for i,val in enumerate(low):
    heightDict[val]=i
heightDict['S']=0
heightDict['E']=25
# print(heightDict)

heights=[]
rowIter=0
for inp in inpList:
    row=[]
    # print(len(inp))
    colIter=0
    for ch in inp:
        row.append(heightDict[ch])
        if ch=='E':
            goal=(rowIter,colIter)
        if ch=='S':
            start=(rowIter,colIter)
        colIter+=1
    heights.append(row)
    rowIter+=1
# print(input)
# print('')
# for row in heights:
#     print(row)
# print(goal)

# 1st problem
def shortestPath(heights,start,goal):
    stepsToPoint=[]
    visited=[]
    for row in heights:
        rowTemp=[]
        visRow=[]
        for point in row:
            rowTemp.append(float('inf'))
            visRow.append(False)
        stepsToPoint.append(rowTemp)
        visited.append(visRow)
    stepsToPoint[start[0]][start[1]]=0
    visited[start[0]][start[1]]=True
    # for row in stepsToPoint:
    #     print(row)
    neighborChecks=[(-1,0),(1,0),(0,-1),(0,1)]
    rowMax=len(heights)-1
    colMax=len(heights[0])-1
    currentPos=start
    steps=1
    # canVisit=set()
    canVisit=[]
    while currentPos!=goal:
        rowPos=currentPos[0]
        colPos=currentPos[1]
        neighbors=[]
        for ch in neighborChecks:
            r=rowPos+ch[0]
            c=colPos+ch[1]
            if c>=0 and c<=colMax and r>=0 and r<=rowMax:
                neighbors.append((r,c))
        
        for n in neighbors:
            if heights[n[0]][n[1]]<=heights[rowPos][colPos]+1:
                stepsToPoint[n[0]][n[1]]=min([stepsToPoint[n[0]][n[1]],stepsToPoint[rowPos][colPos]+1])
                if not visited[n[0]][n[1]] and n not in canVisit:
                    # canVisit.add((steps,n[0],n[1]))
                    canVisit.append(n)
        if len(canVisit)!=0:
            # currentPos=canVisit.pop()[1:]
            currentPos=canVisit.pop(0)
        else:
            break
        visited[currentPos[0]][currentPos[1]]=True
        steps+=1
    return stepsToPoint[goal[0]][goal[1]]
    
sp=shortestPath(heights,start,goal)
print('1st: ',sp)
    



#2nd problem
startVals=[]
for i,row in enumerate(heights):
    for j,h in enumerate(row):
        if h==0:
            startVals.append((i,j))
sps=[]
for stv in startVals:
    sps.append(shortestPath(heights,stv,goal))
print('2nd: ',min(sps))

#issues when trying to store places to visit in a set, it seems like the order is not preserved when adding new items and pop fetches a RANDOM item, not the first which was needed :'D..need to use list and check for no such entries to only store places (and hence visit them) once
#initial idea (looping was the first idea but it seemed boring, but went for that approach after some time anyhow) below, start from goal and go down until first find a place with the right height -but this does not guarantee that all paths to between those two points have been accounted for and it does therefore not have to be the shortest!

# stepsToPoint=[]
# visited=[]
# for row in heights:
#     rowTemp=[]
#     visRow=[]
#     for point in row:
#         rowTemp.append(float('inf'))
#         visRow.append(False)
#     stepsToPoint.append(rowTemp)
#     visited.append(visRow)

# zeroSum=0
# for row in heights:
#     for h in row:
#         if h==0:
#             zeroSum+=1

# stepsToPoint[goal[0]][goal[1]]=0
# visited[goal[0]][goal[1]]=True
# currentPos=goal
# steps=1
# canVisit=set()
# stepsToZeros=[]
# while len(stepsToZeros)!=zeroSum:
#     rowPos=currentPos[0]
#     colPos=currentPos[1]
#     neighbors=[]
#     for ch in neighborChecks:
#         r=rowPos+ch[0]
#         c=colPos+ch[1]
#         if c>=0 and c<=colMax and r>=0 and r<=rowMax:
#             neighbors.append((r,c))
    
#     for n in neighbors:
#         # print(heights[n[0]][n[1]],heights[rowPos][colPos])
#         if heights[n[0]][n[1]]>=heights[rowPos][colPos]-1:
#             stepsToPoint[n[0]][n[1]]=min([stepsToPoint[n[0]][n[1]],stepsToPoint[rowPos][colPos]+1])
#             if not visited[n[0]][n[1]]:
#                 canVisit.add((steps,n[0],n[1]))
#     # sortVisit=sorted(canVisit,key=lambda x:x[0])
#     # currentPos=sortVisit[0][1:]
#     # canVisit.remove(sortVisit[0])
#     currentPos=canVisit.pop()[1:]
#     visited[currentPos[0]][currentPos[1]]=True
#     # print(len(canVisit),heights[currentPos[0]][currentPos[1]])
#     if heights[currentPos[0]][currentPos[1]]==0:
#         stepsToZeros.append(stepsToPoint[currentPos[0]][currentPos[1]])
#     steps+=1
#     # print('')
#     # for row in stepsToPoint:
#     #     print(row)
#     if len(stepsToZeros)==zeroSum:
#         break
#     1
    
#     print('2nd: ',stepsToZeros,zeroSum)
