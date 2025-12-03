import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    instruction_list=f.read().strip().split('\n')

position=50
count_1=0
count_2=0
last_position=100
for instruction in instruction_list:
    direction=instruction[0]
    if direction=='L':
        sign=-1
    else:
        sign=1
    steps=int(instruction[1:])
    full_rotations=steps//100
    steps%=100

    count_2+=full_rotations
    position+=sign*steps
    count_2_incremented=False
    if position<0:
        position+=100
        if last_position!=0:
            count_2+=1
            count_2_incremented=True
    elif position>99:
        count_2+=1
        count_2_incremented=True
    position%=100
    if position==0:
        count_1+=1
        if not count_2_incremented:
            count_2+=1
    last_position=position
print('1st:',count_1)
print('2nd:',count_2)

