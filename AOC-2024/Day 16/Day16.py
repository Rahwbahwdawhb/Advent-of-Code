import os
from bisect import insort
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
# file='example2.txt'
with open(file) as f:
    map_rows=f.read().strip().split('\n')

for ir,row in enumerate(map_rows):
    for ic,ch in enumerate(row):
        if ch=='S':
            start_position=(ir,ic)
        elif ch=='E':
            end_position=(ir,ic)

#debug tool
def print_grid(position):
    for ir,row in enumerate(map_rows):
        temp=''
        for ic,ch in enumerate(row):
            if (ir,ic)==position:
                temp+='O'
            else:
                temp+=ch
        print(temp)

directions=[(0,1),(-1,0),(0,-1),(1,0)] #east, north, west, south
index_changes=[(0,0),(1,1000),(-1,1000),(2,2000)] #index change in direction,associated cost
visited=set()
position_queue=[(0,start_position,0,[start_position])] #cost,position,direction_index,history (for 2nd part)
stop=False
end_reached=False
while not stop:
    current_cost,current_position,current_direction_index,history=position_queue.pop(0)
    visited.add((current_position[0],current_position[1],current_direction_index)) #it's not only the position that is important, the full "state" also has a direction -not including this misses out potential paths and gives the wrong answer!
    for index_change,cost in index_changes:
        new_direction_index=current_direction_index+index_change
        if new_direction_index>3:
            new_direction_index-=4
        if new_direction_index<0:
            new_direction_index+=4
        new_position=(current_position[0]+directions[new_direction_index][0],current_position[1]+directions[new_direction_index][1])
        new_cost=cost+current_cost+1
        if map_rows[new_position[0]][new_position[1]]!='#' and (new_position[0],new_position[1],new_direction_index) not in visited:
            insort(position_queue,(new_cost,new_position,new_direction_index,history+[new_position]))
        if new_position==end_position: #because of the 2nd part, the loop is not stopped until one reaches the end position with a higher cost than the first one that one reached it with
            if not end_reached: #set up reference quantities
                reference_cost=new_cost
                unique_tiles=set(history+[new_position])
                end_reached=True
            elif new_cost==reference_cost:
                unique_tiles=unique_tiles.union(set(history))
            else:
                stop=True #stop while loop when one reaches the end position with a cost that is not the same as the first cost one reached it with

print('1st:',reference_cost)
print('2nd:',len(unique_tiles))