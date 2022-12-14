from preload import input
# print(input)

# input='498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9'

inpList=input.strip().split('\n')

#1st problem
minX=500
maxX=500
maxY=0
entries=[]
for inp in inpList:
    points=inp.split(' -> ')
    points_=[]
    for point in points:
        x,y=point.split(',')
        y=int(y)
        x=int(x)
        points_.append((y,x))
        minX=min([minX,x])
        maxX=max([maxX,x])
        maxY=max([maxY,y])
    entries.append(points_)
# print(minX,maxX,maxY)
grid=[]
for _ in range(maxY+1):
    temp=[]
    for _ in range(maxX-minX+1):
        temp.append('.')
    grid.append(temp)

for entry in entries:
    # print(entry)
    for i in range(len(entry)-1):
        ySpan=range(min([entry[i][0],entry[i+1][0]]),max([entry[i][0],entry[i+1][0]])+1,1)
        xSpan=range(min([entry[i][1],entry[i+1][1]])-minX,max([entry[i][1],entry[i+1][1]])-minX+1,1)
        for y in ySpan:
            for x in xSpan:
                grid[y][x]='#'
# for row in grid:
#     print(row)
start=[0,500-minX]

current=[start[0],start[1]]
obstacles=['#','o']
def fall(current):
    while current[0]<=maxY:
        if grid[current[0]][current[1]] in obstacles:
            break
        current=[current[0]+1,current[1]]
    if current[1]-1<0 or current[0]>maxY:
        current=[]
    else:
        # print(current[0],current[1]-1,len(grid),len(grid[0]))
        if grid[current[0]][current[1]-1] not in obstacles:
            current=fall([current[0],current[1]-1])
        else:
            if current[1]+1>maxX:
                current=[]
            else:
                if grid[current[0]][current[1]+1] not in obstacles:
                    current=fall([current[0],current[1]+1])            
                else:
                    current=[current[0]-1,current[1]]
    return current

stopPos=[1,1]
sandAtRest=0
while len(stopPos)!=0:
    stopPos=fall(start)
    # stopPos,former=fall(former)
    if len(stopPos)!=0:
        grid[stopPos[0]][stopPos[1]]='o'
        sandAtRest+=1

# for row in grid:
#     st=''
#     for ch in row:
#         st+=ch
#     print(st)
print('1st: ',sandAtRest)    


#not very nice solution to 2nd, just using large number of columns and hope they are enough to prevent spill-over, tried to pad list with additional columns on each side when going outside, but seemed to be some issue with recursion depth so maybe some condition had to be adjusted -it just felt quicker to solve it like this 
#could maybe also have used information about the last point (before the sand settled) that was accessed by a vertical drop as input to the next sand to save some time?
#2nd problem
# sourceX=start[1]
# def padGrid():
#     for it,row in enumerate(grid):
#         grid[it]=[row[0]]+row+[row[0]]
#     global sourceX
#     sourceX+=1
def fall2(current):
    while True:
        if grid[current[0]][current[1]] in obstacles:
            break
        current=[current[0]+1,current[1]]
    # if current[1]-1<0 or current[0]>maxY:
    #     padGrid()
    #     current=fall2([current[0]-1,current[1]])
    # else:
        # print(current[0],current[1]-1,len(grid),len(grid[0]))
    if grid[current[0]][current[1]-1] not in obstacles:
        current=fall2([current[0],current[1]-1])
    else:
        # if current[1]+1>maxX:
        #     padGrid()
        #     current=fall2([current[0]-1,current[1]])
        # else:
        if grid[current[0]][current[1]+1] not in obstacles:
            current=fall2([current[0],current[1]+1])            
        else:
            current=[current[0]-1,current[1]]
    return current

grid=[]
for i in range(maxY+3):
    temp=[]
    if i<maxY+2:
        ch='.'
    else:
        ch='#'
    for _ in range(1000):
        temp.append(ch)
    grid.append(temp)

for entry in entries:
    # print(entry)
    for i in range(len(entry)-1):
        ySpan=range(min([entry[i][0],entry[i+1][0]]),max([entry[i][0],entry[i+1][0]])+1,1)
        xSpan=range(min([entry[i][1],entry[i+1][1]]),max([entry[i][1],entry[i+1][1]])+1,1)
        for y in ySpan:
            for x in xSpan:
                grid[y][x]='#'

# while grid[0][sourceX]!='o':
# for _ in range(1):
#     stopPos=fall2(start)
#     if len(stopPos)!=0:
#         grid[stopPos[0]][stopPos[1]]='o'
#         sandAtRest+=1

sandAtRest=0
while grid[0][500]!='o':
# for _ in range(200):
    stopPos=fall2([0,500])
    if len(stopPos)!=0:
        grid[stopPos[0]][stopPos[1]]='o'
        sandAtRest+=1
    # else:
    #     1
print('2nd: ',sandAtRest)
# for row in grid:
#     st=''
#     for ch in row:
#         st+=ch
#     print(st)
