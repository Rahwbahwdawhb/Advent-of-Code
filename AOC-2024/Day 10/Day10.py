import os
from copy import deepcopy
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
# file='example2.txt'
# file='example3.txt'
with open(file) as f:
    dataList=f.read().strip().split('\n')

grid=[]
trailHeads=[]
for ir,row in enumerate(dataList):
    temp=[]
    for ic,height in enumerate(row):
        if height=='.':
            temp.append(-1)
        else:
            temp.append(int(height))
        if height=='0':
            trailHeads.append((ir,ic))
    grid.append(temp)

directions=[(1,0),(-1,0),(0,1),(0,-1)]
max_row=len(grid)-1
max_col=len(grid[0])-1
path_9_dict=dict() #for part 2, store all paths that lead to 9s with trailheads (starting positions) as keys
total_trail_rating_count=0 #simpler solution to part 2

#wasn't necessary, but could have memoized the number of 9s that each position lead to
def recursive_search(position,height,visited_9s=set(),path=[]):
    global total_trail_rating_count
    if not path:
        path=[position]
    if height==9:
        total_trail_rating_count+=1
        new_visited_9s=deepcopy(visited_9s)
        new_visited_9s.add(position)
        new_path=deepcopy(path)
        new_path.append(position)
        try:
            path_9_dict[new_path[0]].append(new_path)
        except:
            path_9_dict[new_path[0]]=[new_path]
        return new_visited_9s
    else:
        to_visit=[]
        for d in directions:
            position_r=position[0]+d[0]
            position_c=position[1]+d[1]
            if 0<=position_r<=max_row and 0<=position_c<=max_col:
                adjacent_position=(position_r,position_c)
                adjacent_height=grid[adjacent_position[0]][adjacent_position[1]]
                if adjacent_height-height==1:
                    to_visit.append((adjacent_position,adjacent_height))
        if not to_visit:
            return deepcopy(visited_9s)
        else:
            new_visited_9s=deepcopy(visited_9s)
            for adjacent_position,adjacent_height in to_visit:
                new_path=deepcopy(path)
                new_path.append(adjacent_position)
                new_visited_9s_=recursive_search(adjacent_position,adjacent_height,visited_9s,new_path)
                new_visited_9s=new_visited_9s.union(new_visited_9s_)
            return new_visited_9s

total_score=0
for th in trailHeads:
    visited_9s=recursive_search(th,0)
    total_score+=len(visited_9s)
print('1st:',total_score)

total_trail_rating=0
for trailhead in path_9_dict.keys():
    total_trail_rating+=len(path_9_dict[trailhead])
print('2nd:',total_trail_rating)
print('2nd:',total_trail_rating_count,'simpler solution')