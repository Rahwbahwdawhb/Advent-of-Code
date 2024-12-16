import os
import numpy as np
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    data_list=f.read().strip().split('\n')

if file=='example.txt':
    N_rows=7
    N_cols=11
else:
    N_rows=103
    N_cols=101

start_positions=[]
velocities=[]
for row in data_list:
    row_list=[s.split('=')[1] for s in row.split()]
    start_position=np.array([int(p) for p in row_list[0].split(',')])
    start_positions.append(start_position)
    velocity=np.array([int(v) for v in row_list[1].split(',')])
    velocities.append(velocity)

def get_final_positions(start_positions,velocities,time_elapsed):
    final_positions=[]
    quadrant_dict={1:0,2:0,3:0,4:0} #keep robot count within each quadrant
    for start_position,velocity in zip(start_positions,velocities):
        unwrapped_steps=velocity*time_elapsed
        wrapped_steps=np.array([np.abs(unwrapped_steps[0])%N_cols,np.abs(unwrapped_steps[1])%N_rows]) #maintain magnitude of steps (direction not accounted for as it gets weird with % operator) that remains after looping as many integer number around the entire grid as possible
        wrapped_steps_signed=np.sign(unwrapped_steps)*np.array(wrapped_steps) #getting back the direction of the steps
        final_position=start_position+wrapped_steps_signed
        for i,dimension in enumerate([N_cols,N_rows]): #correct final position if it ends up outside the grid
            if final_position[i]<0:
                final_position[i]+=dimension
            elif final_position[i]>=dimension:
                final_position[i]-=dimension
        final_positions.append((final_position[1],final_position[0]))
        #add a count to the quadrant that the robot ends up in
        if final_position[0]<N_cols//2 and final_position[1]<N_rows//2:
            quadrant_dict[1]+=1
        elif final_position[0]>N_cols//2 and final_position[1]<N_rows//2:
            quadrant_dict[2]+=1
        elif final_position[0]<N_cols//2 and final_position[1]>N_rows//2:
            quadrant_dict[3]+=1
        elif final_position[0]>N_cols//2 and final_position[1]>N_rows//2:
            quadrant_dict[4]+=1
        
    return quadrant_dict,final_positions

def print_grid(final_positions_,filename='robot_distribution.txt',terminal_print=False):
    from copy import deepcopy
    final_positions=deepcopy(final_positions_)
    with open(filename,'w') as f:
        for i in range(N_rows):
            temp=''
            for ii in range(N_cols):
                count=0
                while True:
                    if (i,ii) in final_positions:
                        final_positions.remove((i,ii))
                        count+=1
                    else:
                        break
                if count==0:
                    temp+='.'
                else:
                    temp+=str(count)            
            f.write(temp+'\n')
            if terminal_print:
                print(temp)

#part 1
quadrant_dict,_=get_final_positions(start_positions,velocities,100)
safety_factor=1
for quadrant in quadrant_dict.keys():
    safety_factor*=quadrant_dict[quadrant]
print('1st',safety_factor)

#part 2, quite slow because of looping through robot positions to calculate a reference sum to identify when the chirstmas tree is formed..but it works
time_steps=0
position_str_dict=dict()
chain_sums=[]
while True:
    time_steps+=1
    quadrant_dict,final_positions=get_final_positions(start_positions,velocities,time_steps)
    final_position_set=set(final_positions)
    chain_sum=0 #sum of number of robots with at least one adjacent robot (when the tree is formed this number should be maximized!)
    for position in final_position_set:
        for dr,dc in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
            if (position[0]+dr,position[1]+dc) in final_position_set:
                chain_sum+=1
                break
    chain_sums.append(chain_sum)
    final_positions_str=str(final_positions)
    try:
        position_str_dict[final_positions_str]
        break
    except:
        position_str_dict[final_positions_str]=time_steps
time_steps_to_tree=np.argmax(chain_sums)+1
print('2nd:',time_steps_to_tree)
#get the robot positions when they form a tree and print the distribution to a file
quadrant_dict,final_positions=get_final_positions(start_positions,velocities,time_steps_to_tree)
print_grid(final_positions,f'christmas_tree_after_{time_steps_to_tree}_seconds.txt')