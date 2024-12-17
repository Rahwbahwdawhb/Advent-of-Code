import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
# file='example2.txt'
with open(file) as f:
    register_part,program_part=f.read().strip().split('\n\n')

register_dict=dict() #keeps track of register settings
for register_setting in register_part.split('\n'):
    register_str,register_value=register_setting.split(':')
    register_dict[register_str.split(' ')[1]]=int(register_value.strip())
program_str=program_part.split(':')[1].strip()
program=[int(x) for x in program_str.split(',')]

#calculate combo operand values from the operand inputs
def combo_operand_value(operand):
    if 0<=operand<=3:
        return operand
    elif operand==4:
        return register_dict['A']
    elif operand==5:
        return register_dict['B']
    elif operand==6:
        return register_dict['C']
    elif operand==7:
        print('Invalid program!')
        return None

#took some time to understand the text, but this function just a direct implementation of the text descirbing the instructions
def do_instruction(register_dict,opcode,operand):
    #return output string, bool indicating if instruction pointer should change and its new value
    if opcode==0:
        register_dict['A']=register_dict['A']//2**combo_operand_value(operand)
        return '',False,None
    elif opcode==1:
        register_dict['B']=int(bin(register_dict['B']),2)^int(bin(operand),2)
        return '',False,None
    elif opcode==2:
        register_dict['B']=combo_operand_value(operand)%8
        return '',False,None
    elif opcode==3:
        if register_dict['A']==0:
            return '',False,None
        else:
            return '',True,operand
    elif opcode==4:
        register_dict['B']=int(bin(register_dict['B']),2)^int(bin(register_dict['C']),2)
        return '',False,None
    elif opcode==5:
        return str(combo_operand_value(operand)%8),False,None
    elif opcode==6:
        register_dict['B']=register_dict['A']//2**combo_operand_value(operand)
        return '',False,None
    elif opcode==7:
        register_dict['C']=register_dict['A']//2**combo_operand_value(operand)
        return '',False,None

def run_program(register_dict,program):
    instruction_pointer=0
    output_list=[]
    it=0
    while instruction_pointer<len(program)-1:
        it+=1
        current_opcode=program[instruction_pointer]
        current_operand=program[instruction_pointer+1]
        output_str,pointer_bool,pointer_value=do_instruction(register_dict,current_opcode,current_operand)        
        if output_str!='':
            output_list.append(output_str)
        if pointer_bool:
            instruction_pointer=pointer_value
        else:
            instruction_pointer+=2
        # print([register_dict[key] for key in ['A','B','C']]) #checking these outputs showed that every time that the A-register was decreased the integer fraction // between the previous and the new value was always 8, which then lead to the approach described below for the 2nd part
    return ','.join(output_list)

#part 1
output_str=run_program(register_dict,program)
print('1st:',output_str)

#part 2
it=0
it_ok=[]
hunt_str=program_str[-3:] #this captures the last two "program elements", i.e. the last opcode and operand
N=len(hunt_str)
#this loop increments integer values to register A's start value, runs the program and appends integer values that gives an output that matches the last opcode and operand (hunt_str)
#these indices serve as starting point for calculating greater integer values that can result in the remaining "program elements", as described below
while True:
    register_dict['A']=it
    register_dict['B']=0
    register_dict['C']=0
    out_str=run_program(register_dict,program)
    if out_str==hunt_str:
        it_ok.append(it)
    if len(out_str)>N:
        break
    it+=1

#since the "integer fraction //" between register A values were 8 whenver it was decreased, this means that all values that give rise to the same result after // will produce the correct ending "program elements"
#i.e. if value1 gives the correct last two "program elements" then all values between value1*8+1 and value1*8+7 are potential candidates to give the third last correct "program element"
#since (value1*8+1)//8=(value1*8+7)//8=value1, only values within this range can produce value1 that is necessary to produce the last correct "program elements"!
#the idea is therefore to start from the integer values that were obtained from the loop above, multiply them by 8 and add values between 1 to 7 and run the program for each of these new integer values
#the resulting output strings will then be compared to the correct "program element" that preceedes the last two (that were used for hunt_str to get the indices from the loop above)
#for output strings that match, those integer values will be saved in a list that will be used in the same manner for the subsequent preceeding "program element"
#this is repeated until all of the "program elements" have been accounted for
#the final answer is then obtained by taking the minimum value of the integer values that were saved during the last iteration
next_values=it_ok
target_str=hunt_str
remaining_elements=program[:-2]
while remaining_elements:
    values=next_values
    new_element=remaining_elements.pop()
    target_str=f"{new_element},{target_str}"
    next_values=[]
    while values:
        value=values.pop()
        for i in range(8):
            test_value=value*8+i       
            register_dict['A']=test_value
            register_dict['B']=0
            register_dict['C']=0
            out_str=run_program(register_dict,program)
            if out_str==target_str:
                next_values.append(test_value)
print('2nd:',min(next_values))