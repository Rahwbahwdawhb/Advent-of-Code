import os
import numpy as np
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    race_track_rows=f.read().strip().split('\n')

for ir,row in enumerate(race_track_rows):
    for ic,col in enumerate(row):
        if col=='S':
            start_position=(ir,ic)
        elif col=='E':
            end_position=(ir,ic)

#getting non-cheating path
directions=[(1,0),(-1,0),(0,1),(0,-1)]
steps_til_end=0
position=end_position
last_position=None
distance_dict=dict()
run_bool=True
non_cheating_track=[] #for part 1
non_cheating_track_2=[] #for part 2
while run_bool:
    for direction in directions:
        new_position=(position[0]+direction[0],position[1]+direction[1])
        if new_position!=last_position and race_track_rows[new_position[0]][new_position[1]]!='#':
            distance_dict[position]=steps_til_end
            non_cheating_track.append(position)
            non_cheating_track_2.append(position)
            if new_position==start_position:
                distance_dict[new_position]=steps_til_end+1
                non_cheating_track.append(new_position)
                non_cheating_track_2.append([position[0]+direction[0],position[1]+direction[1]])
                run_bool=False
            else:
                last_position=position
                position=new_position
                steps_til_end+=1
            break
non_cheating_track_2=np.array(non_cheating_track_2)[::-1] #for part 2
no_cheat_time=distance_dict[start_position]

#part 1
cheat_directions=[(2,0),(-2,0),(0,2),(0,-2)]
cheat_time_dict=dict()
while non_cheating_track:
    current_position=non_cheating_track.pop()
    for cheat_direction in cheat_directions:
        new_position=(current_position[0]+cheat_direction[0],current_position[1]+cheat_direction[1])
        try:
            time_saved=distance_dict[current_position]-(distance_dict[new_position]+2)
            if time_saved in cheat_time_dict:
                # cheat_time_dict[time_saved].append([current_position,new_position])
                cheat_time_dict[time_saved]+=1
            else:
                # cheat_time_dict[time_saved]=[[current_position,new_position]]
                cheat_time_dict[time_saved]=1
        except:
            pass

def example_print(cheat_time_dict):
    time_saving_cheats=sorted([time_save for time_save in cheat_time_dict.keys() if time_save>0])
    for key in time_saving_cheats:
        if cheat_time_dict[key]!=1:
            print(f"There are {cheat_time_dict[key]} cheats that save {key} picoseconds")
        else:
            print(f"There is one cheat that saves {key} picoseconds")
if file=='example.txt':
    print('Part 1:')
    example_print(cheat_time_dict)
    print(' ')
else:
    counted_cheats=0
    for time_save in cheat_time_dict.keys():
        if time_save>=100:
            counted_cheats+=cheat_time_dict[time_save]
    print('1st:',counted_cheats)

#part 2
cheat_time=20
if file=='example.txt':
    minimum_time_to_save=50
    use_dict_bool=True
else:
    minimum_time_to_save=100
    use_dict_bool=False
cheat_time_dict_2=dict()
cheats_of_interest_sum=0
for i,current_position in enumerate(non_cheating_track_2):
    try:
        positions_of_interest=non_cheating_track_2[i+minimum_time_to_save:]
    except:
        break
    manhattan_distances=np.abs(positions_of_interest[:,0]-current_position[0])+np.abs(positions_of_interest[:,1]-current_position[1])
    for md,poi in zip(manhattan_distances,positions_of_interest):
        if md<=cheat_time:
            time_save=distance_dict[tuple(current_position)]-(distance_dict[tuple(poi)]+md)
            if time_save>=minimum_time_to_save:
                if use_dict_bool:
                    try:
                        cheat_time_dict_2[time_save]+=1
                    except:
                        cheat_time_dict_2[time_save]=1
                else:
                    cheats_of_interest_sum+=1

if file=='example.txt':
    print('Part 2:')
    example_print(cheat_time_dict_2)
else:
    print('2nd:',cheats_of_interest_sum)