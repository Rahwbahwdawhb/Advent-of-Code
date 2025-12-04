import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    map_rows=f.read().strip().split('\n')

positions_1=set()
positions_2=set()
for ir,row in enumerate(map_rows):
    for ic,col in enumerate(row):
        if col=='@':
            positions_1.add((ir,ic))
            positions_2.add((ir,ic))
offsets=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
reachable_count=0
for position in positions_1:
    count=0
    for offset in offsets:
        if (position[0]+offset[0],position[1]+offset[1]) in positions_1:
            count+=1
        if count==4:
            break
    if count!=4:
        reachable_count+=1
        positions_2.remove(position)
print("1st:",reachable_count)

from time import time
t0=time()
can_be_removed_count=reachable_count
to_be_removed=[]
while True:
    for position in positions_2:
        count=0
        for offset in offsets:
            if (position[0]+offset[0],position[1]+offset[1]) in positions_2:
                count+=1
            if count==4:
                break
        if count!=4:
            to_be_removed.append(position)
    if not to_be_removed:
        break
    while to_be_removed:  
        position=to_be_removed.pop()
        positions_2.remove(position)
        can_be_removed_count+=1
print("2nd:",can_be_removed_count)
print(time()-t0)