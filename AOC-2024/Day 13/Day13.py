import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    machine_list=f.read().strip().split('\n\n')

def row_splitter(row,split_ch):
    split_1=row.split(':')[1]
    split_2=split_1.split(',')
    split_3=[]
    for part in split_2:
        split_3.append(int(part.split(split_ch)[1]))
    return split_3

#The problem for every machine is a system of two equations, one for each coordinate (x and y), which can be formulated as:
#a*A_1+b*B_1=P_1 (1)
#a*A_2+b*B_2=P_2 (2)
#where A_1,2 is the x,y increment for button_A; B_1,2 is the x,y increment for button_B; P_1,2 is the x,y coordinate of the price; and a and b are the number of presses on button_A and button_B respectively
#solving for a through: B_2*(1)-B2*(2) gives a*A_1*B_2-a*A_2*B_1=P_1*B2-P2*B_1 => a=(P_1*B2-P2*B_1)/(A_1*B_2-A_2*B_1)
#b can then be determined from (1): b=(P_1-A_1*a)/B_1
#for part 1, one can just evaluate the fractions directly and convert to integers
#for part 2, the numbers get too large for float point precision, so one instead checks whether integer division leaves any remainder
#-if it does not, do integer division and calculate the token cost.
#-the approach for part 2 naturally also works for part 1

a_press_cost=3
b_press_cost=1
def get_winning_tokens(button_a,button_b,prize):
    minumum_winning_tokens=0
    a_press_nominator=prize[0]*button_b[1]-prize[1]*button_b[0]
    a_press_denominator=button_a[0]*button_b[1]-button_a[1]*button_b[0]
    if a_press_nominator%a_press_denominator==0:
        a_press=a_press_nominator//a_press_denominator
        b_press_nominator=prize[0]-button_a[0]*a_press
        b_press_denominator=button_b[0]
        if b_press_nominator%b_press_denominator==0:
            b_press=b_press_nominator//b_press_denominator
            minumum_winning_tokens=a_press_cost*a_press+b_press_cost*b_press
    return minumum_winning_tokens

minumum_winning_tokens_1=0
minumum_winning_tokens_2=0
for machine in machine_list:
    info_rows=machine.split('\n')
    button_a=row_splitter(info_rows[0],'+') 
    button_b=row_splitter(info_rows[1],'+')
    prize=row_splitter(info_rows[2],'=')
    minumum_winning_tokens_1+=get_winning_tokens(button_a,button_b,prize)
    minumum_winning_tokens_2+=get_winning_tokens(button_a,button_b,[p+10000000000000 for p in prize])
    
print('1st:',minumum_winning_tokens_1)
print('2nd:',minumum_winning_tokens_2)
