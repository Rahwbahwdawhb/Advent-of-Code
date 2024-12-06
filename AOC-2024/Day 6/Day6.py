import os

os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'

with open(file) as f:
    dataList=f.read().strip().split('\n')

grid=[]
obstacles=set()
for ir,row in enumerate(dataList):
    temp=[]
    for ic,ch in enumerate(row):
        temp.append(ch)
        if ch=='^':
            start=(ir,ic)
            temp[-1]='.'
        elif ch=='#':
            obstacles.add((ir,ic))
    grid.append(temp)

dims=(len(grid)-1,len(grid[0])-1)
grid2=grid+[]
directions=[(-1,0),(0,1),(1,0),(0,-1)]
direction_i=0
direction=directions[direction_i]
last_position=start
position=(start[0]+direction[0],start[1]+direction[1])
# step_count=0
path=set()
path.add(start)
import time
pathLens=[]
c0=0
c1=0
c2=0
printBool=False
while 0<=position[0]<=dims[0] and 0<=position[1]<=dims[1]:
    c0+=1
    if grid[position[0]][position[1]]=='#':
        direction_i+=1
        if direction_i>3:
            direction_i=0
        direction=directions[direction_i]
        position=last_position
        # step_count-=1
        # print(direction_i)
        c1+=1
        # print(' ')
        # for r in range(low_r,high_r+1,1):
        #     temp=''
        #     for c in range(low_c,high_c+1,1):
        #         temp+=grid2[r][c]
        #     print(temp)
        # print(len(path))
        1
        # printBool=True
    else:    
        c2+=1    
        last_position=position
        path.add(last_position)
        pathLens.append(last_position)

        pad=5
        low_r=max([0,position[0]-pad])
        high_r=min([dims[0],position[0]+pad])
        low_c=max([0,position[1]-pad])
        high_c=min([dims[1],position[1]+pad])

        
        if printBool:
            grid2[position[0]][position[1]]='o'
            print(' ')
            for r in range(low_r,high_r+1,1):
                temp=''
                for c in range(low_c,high_c+1,1):
                    temp+=grid2[r][c]
                print(temp)
            print(len(path))
            printBool=False
            1
        grid2[position[0]][position[1]]='X'
            
        # time.sleep(.4)
        # for r in grid2:
        #     print(''.join(r))
    #     step_count+=1
    # print(step_count)    
    position=(position[0]+direction[0],position[1]+direction[1])
path.add(last_position)
print(len(path))
#4646 not correct
#4638 too low