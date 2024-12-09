import os
from copy import deepcopy
os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'

with open(file) as f:
    dataList=f.read().strip().split('\n')

grid=[]
for ir,row in enumerate(dataList):
    temp=[]
    for ic,ch in enumerate(row):
        temp.append(ch)
        if ch=='^':
            start=(ir,ic)
            temp[-1]='.'
    grid.append(temp)

dims=(len(grid)-1,len(grid[0])-1)
directions=[(-1,0),(0,1),(1,0),(0,-1)]
direction_i=0
direction=directions[direction_i]
last_position=start
position=(start[0]+direction[0],start[1]+direction[1])

path0=[]
dir0=[]
path0.append(start)
dir0.append(direction_i)
while 0<=position[0]<=dims[0] and 0<=position[1]<=dims[1]:
    if grid[position[0]][position[1]]=='#':
        direction_i+=1
        if direction_i>3:
            direction_i=0
        direction=directions[direction_i]
        position=last_position
    else:
        last_position=position
        path0.append((last_position[0],last_position[1]))
        dir0.append(direction_i)
    position=(position[0]+direction[0],position[1]+direction[1])

print('1st:',len(set(path0)))

#part 2, slow solution: start from last position from path0, replace its gridpoint with # and start from the second last position
#repeat this for every position in path0 and add positions of new # that result in loops to set, print the set length
def checkPath(start_position,grid,direction_i):
    last_position=start_position
    direction=directions[direction_i]
    position=(last_position[0]+direction[0],last_position[1]+direction[1])    
    loop_value=0
    new_path=set()
    while (0<=position[0]<=dims[0] and 0<=position[1]<=dims[1]):        
        if grid[position[0]][position[1]]=='#':
            direction_i+=1
            if direction_i>3:
                direction_i=0
            direction=directions[direction_i]
            position=last_position
        else:    
            last_position=position
            if (last_position[0],last_position[1],direction_i) in new_path:
                loop_value=1
                break
            else:
                pass
            new_path.add((last_position[0],last_position[1],direction_i))
            position=(position[0]+direction[0],position[1]+direction[1])
    return new_path,loop_value

all_nodes=set()
while path0:
    try:
        pos_r,pos_c=path0.pop()
        d_i=dir0.pop()
        if (pos_r,pos_c) not in path0:
            grid_=deepcopy(grid)
            grid_[pos_r][pos_c]='#'    
            p,loop_value=checkPath((path0[-1][0],path0[-1][1]),grid_,dir0[-1])
            if loop_value==1:
                all_nodes.add((pos_r,pos_c))
    except:
        print('2nd',len(all_nodes))
