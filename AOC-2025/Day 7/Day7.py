import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    data_list=f.read().strip().split('\n')

splitter_positions=set()
for ir,row in enumerate(data_list):
    for ic,col in enumerate(row):
        if col=='S':
            start_position=(ir,ic,1)
        elif col=='^':
            splitter_positions.add((ir,ic))
beam_positions={start_position}
split_count=0
for _ in range(ir+1):
    # #works for part 1
    # next_beam_positions=set()
    # while beam_positions:
    #     current_beam_position=beam_positions.pop()
    #     temp=(current_beam_position[0]+1,current_beam_position[1])
    #     if temp in splitter_positions:
    #         split_count+=1
    #         next_beam_positions.add((current_beam_position[0]+1,current_beam_position[1]-1,current_beam_position[2]))
    #         next_beam_positions.add((current_beam_position[0]+1,current_beam_position[1]+1,current_beam_position[2]))
    #     else:
    #         next_beam_positions.add((current_beam_position[0]+1,current_beam_position[1],current_beam_position[2]))
    # beam_positions=next_beam_positions

    next_beam_positions=set()
    next_beam_positions_dict=dict()
    while beam_positions:
        current_beam_position=beam_positions.pop()
        temp=(current_beam_position[0]+1,current_beam_position[1])
        if temp in splitter_positions:
            split_count+=1
            try:
                next_beam_positions_dict[(current_beam_position[0]+1,current_beam_position[1]-1)]+=current_beam_position[2]
            except:
                next_beam_positions_dict[(current_beam_position[0]+1,current_beam_position[1]-1)]=current_beam_position[2]
            try:
                next_beam_positions_dict[(current_beam_position[0]+1,current_beam_position[1]+1)]+=current_beam_position[2]
            except:
                next_beam_positions_dict[(current_beam_position[0]+1,current_beam_position[1]+1)]=current_beam_position[2]
        else:
            try:
                next_beam_positions_dict[temp]+=current_beam_position[2]
            except:
                next_beam_positions_dict[temp]=current_beam_position[2]
    for position,count in next_beam_positions_dict.items():
        next_beam_positions.add((position[0],position[1],count))
    beam_positions=next_beam_positions
    
print("1st:",split_count)
world_count=0
for _,_,count in beam_positions:
    world_count+=count
print("2nd:",world_count)