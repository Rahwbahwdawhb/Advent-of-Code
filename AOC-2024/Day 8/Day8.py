import os
import numpy as np
os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'
# file='example2.txt'

with open(file) as f:
    dataList=f.read().strip().split('\n')

dims=(len(dataList),len(dataList[0]))
antenna_dict=dict()
grid_positions=[]
for ir,row in enumerate(dataList):
    for ic,ch in enumerate(row):
        grid_positions.append([ir,ic])
        if ch!='.':
            position=np.array([ir,ic])
            try:
                antenna_dict[ch].append(position)
            except:
                antenna_dict[ch]=[position]
def check_antinode_position(pos):
    return sum([0<=pos[0]<dims[0],0<=pos[1]<dims[1]])==2

antinode_count=0
antinodes=set() #for part 1
antinodes_2=set() #for part 2
for key in antenna_dict.keys():
    antennas=antenna_dict[key]
    while True:
        position=antennas.pop()
        if len(antennas)>0:
            #part 1
            for position_ii in antennas:
                position_difference=position_ii-position
                possible_locations=[position_ii+position_difference,position-position_difference]
                for location in possible_locations:
                    check_bool=check_antinode_position(location)                 
                    if check_bool:
                        antinode_count+=1
                        antinodes.add((location[0],location[1]))
                outside_grid=False
                it=0
                antinodes_2.add((position[0],position[1]))
                antinodes_2.add((position_ii[0],position_ii[1]))
                #part 2
                while not outside_grid:
                    location=position_ii-position_difference*it
                    check_bool=check_antinode_position(location)
                    if check_bool:
                        antinodes_2.add((location[0],location[1]))
                    else:
                        break
                    it+=1
                it=0
                while not outside_grid:
                    location=position_ii+position_difference*it
                    check_bool=check_antinode_position(location)
                    if check_bool:
                        antinodes_2.add((location[0],location[1]))
                    else:
                        break
                    it+=1
        else:
            break

print('1st:',len(antinodes))
print('2nd:',len(antinodes_2))