import os
from bisect import insort
from copy import deepcopy
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example_short.txt'
# file='example_long.txt'
with open(file) as f:
    wire_part,gate_part=f.read().strip().split('\n\n')

def and_operator(wire_dict,wire_1,wire_2,wire_output):
    wire_dict[wire_output]=wire_dict[wire_1] and wire_dict[wire_2]
def or_operator(wire_dict,wire_1,wire_2,wire_output):
    wire_dict[wire_output]=wire_dict[wire_1] or wire_dict[wire_2]
def xor_operator(wire_dict,wire_1,wire_2,wire_output):
    wire_dict[wire_output]=wire_dict[wire_1] ^ wire_dict[wire_2]
operator_dict={'AND':and_operator,'OR':or_operator,'XOR':xor_operator}

class GATE:
    def __init__(self,wire_1,wire_2,wire_output,operator,wire_dict,gate_queuer):        
        self.wire_1=wire_1
        self.wire_2=wire_2
        self.wire_output=wire_output
        self.operator_function=operator_dict[operator]
        self.operator=operator
        self.wire_dict=wire_dict
        self.gate_queuer=gate_queuer
    def operate(self):
        self.operator_function(self.wire_dict,self.wire_1,self.wire_2,self.wire_output)
        self.gate_queuer.output_notificate(self.wire_output)
    def check_for_inputs(self):
        return self.wire_dict[self.wire_1] is not None and self.wire_dict[self.wire_2] is not None
    def assign_wire_dict(self,new_wire_dict):
        self.wire_dict=new_wire_dict

class GATE_QUEUER:
    def __init__(self,gate_queue,waiting_gates_dict):
        self.gate_queue=gate_queue
        self.waiting_gates_dict=waiting_gates_dict
        self.queued_gates=set()
    def new_output_wire(self,wire_output,gate_to_give_output):
        self.waiting_gates_dict[wire_output]=[gate_to_give_output]
    def assign_waiting_gates_dict(self,new_waiting_gates_dict):
        self.waiting_gates_dict=new_waiting_gates_dict
    def output_notificate(self,wire_output):
        for gate_ in self.waiting_gates_dict[wire_output]:
            if not wire_output.startswith('z') and gate_.check_for_inputs():
                self.gate_queue.append(gate_)
                self.queued_gates.add(gate_)
        del self.waiting_gates_dict[wire_output]

def reset(wire_part,gate_part):
    wire_dict=dict()
    wire_combo_dict=dict()
    initial_wires=set()
    for wire in wire_part.split('\n'):
        wire_name,wire_value=wire.split(': ')
        wire_dict[wire_name]=bool(int(wire_value))
        initial_wires.add(wire_name)

    waiting_gates_dict=dict()
    gate_queue=[]
    gate_queuer=GATE_QUEUER(gate_queue,waiting_gates_dict)

    adjacency_dict=dict()
    gate_dict=dict()
    output_wires=[]
    for gate_str in gate_part.split('\n'):
        inputs,wire_output=gate_str.split(' -> ')
        wire_1,operator,wire_2=inputs.split()
        gate_=GATE(wire_1,wire_2,wire_output,operator,wire_dict,gate_queuer)
        gate_dict[wire_output]=gate_
        try:
            wire_combo_dict[tuple(sorted([wire_1,wire_2]))].append(wire_output)
        except:
            wire_combo_dict[tuple(sorted([wire_1,wire_2]))]=[wire_output]
        waiting_bool=True
        if wire_1 in initial_wires and wire_2 in initial_wires:
            gate_queue.append(gate_)
            waiting_bool=False
        if waiting_bool:
            try:
                waiting_gates_dict[wire_1].append(gate_)
            except:
                waiting_gates_dict[wire_1]=[gate_]
            try:
                waiting_gates_dict[wire_2].append(gate_)
            except:
                waiting_gates_dict[wire_2]=[gate_]
        for wire_ in [wire_1,wire_2,wire_output]:
            if wire_ not in wire_dict:
                wire_dict[wire_]=None
            if wire_.startswith('z'):
                insort(output_wires,(int(wire_[1:]),wire_))
                gate_queuer.new_output_wire(wire_,gate_)
            if wire_!=wire_output:
                try:
                    adjacency_dict[wire_].append(wire_output)
                except:
                    adjacency_dict[wire_]=[wire_output]
    return gate_queue,output_wires,wire_dict,initial_wires,gate_dict,adjacency_dict,wire_combo_dict

def wire_list_to_bit_str(wire_dict,wire_list):
    binary_str=''
    bool_list=[]
    for _,wire_ in wire_list:
        binary_str+=str(int(wire_dict[wire_]))
        bool_list.append(wire_dict[wire_])
    return binary_str,bool_list

def get_output_bits(gate_queue,output_wires,wire_dict):
    while gate_queue:
        gate_=gate_queue.pop(0)
        gate_.operate()
    binary_output_str,binary_output_bools=wire_list_to_bit_str(wire_dict,output_wires)
    return binary_output_str,binary_output_bools

gate_queue,output_wires,wire_dict,initial_wires,gate_dict,adjacency_dict,wire_combo_dict=reset(wire_part,gate_part)
binary_output_str,binary_output_bools=get_output_bits(gate_queue,output_wires,wire_dict)
print('1st:',int(binary_output_str[::-1],2))

#part 2
#Rabbit holes, trying to plot grah and make sense of it, checking recursion depths
#Needed to dig into the details about what went on with the gate/wires
#Very convoluted and time consuming to check gate/wire combinations, felt like detective work
xs=[]
ys=[]
for wire_ in initial_wires:
    if wire_.startswith('x'):
        insort(xs,(int(wire_[1:]),wire_))
    else:
        insort(ys,(int(wire_[1:]),wire_))
x_binary,_=wire_list_to_bit_str(wire_dict,xs[::-1])
x_in=int(x_binary,2)
y_binary,_=wire_list_to_bit_str(wire_dict,ys[::-1])
y_in=int(y_binary,2)
correct_output=x_in+y_in
correct_binary_output_str=bin(correct_output)[2:]

correct_output_wires=[bool(int(bit)) for bit in correct_binary_output_str[::-1]]

incorrect_bit_indices=[]
for i,(correct_i,incorrect_i) in enumerate(zip(correct_output_wires,binary_output_bools)):
    if correct_i!=incorrect_i:
        incorrect_bit_indices.append(i)

#checking input validity
incorrect_inputs=[] #looks ok, could also verify that they go to and operator
first_gates_to_outputs=[]
deviating_first_gates=[]
for xi_,yi_ in zip(xs,ys):
    if adjacency_dict[xi_[1]]!=adjacency_dict[yi_[1]]: #initial addition should between x and y bits should go to the same gate
        incorrect_inputs.append((xi_[1],yi_[1]))
    else:
        sum_AND=0
        sum_XOR=0
        for wire_ in adjacency_dict[xi_[1]]:
            gate_operator=gate_dict[wire_].operator #each input pair x and y should go to an AND and an XOR gate (for carry over) -checked some manually to confirm
            if gate_operator=='XOR':
                sum_XOR+=1
            if gate_operator=='AND':
                sum_AND+=1
            if wire_[0]=='z' and wire_!='z00': #saw that except for z00, the other outputs get their values from an XOR-gate that comes after the first XOR-gate that the x and y values are sent to
                first_gates_to_outputs.append((wire_,int(wire_[1:])))
        if sum_AND!=1 and sum_XOR!=1:
            deviating_first_gates.append(wire_)
assert len(incorrect_inputs)==0, "Assumption that all x.. and y.. wires go to the same gates is not fulfilled" #this is assumed to hold from here on
#above checks caught z12 in deviating_outputs and gate_dict['z12'].operator showed AND => z12 needs to be swapped with the XOR-output after the XOR-gate that x12 and y12 are sent to
def find_XOR_to_output(output_wire,gate_dict):
    output_wire_int=int(output_wire[1:])
    if output_wire_int<10:
        output_wire_str=f"0{output_wire_int}"
    else:
        output_wire_str=str(output_wire_int)
    wires_to_check=[w for w in adjacency_dict[f"x{output_wire_str}"] if w!=output_wire] #get output_wires that x.. give rise to but remove the output wire z.. if it is listed (i.e. input goes to output after first gate)
    xor_outputs=[] #XOR-gates connected to x.. input
    for wire_ in wires_to_check:
        if gate_dict[wire_].operator=='XOR':
            xor_outputs.append(wire_)
    wires_out_from_xor=[]
    for wire_ in xor_outputs:
        next_output_wires=adjacency_dict[wire_] #output wires that follow after the gates after the first XOR-gate
        for wire__ in next_output_wires:
            if gate_dict[wire__].operator=='XOR':
                wires_out_from_xor.append(wire__)
    return wires_out_from_xor
swap_wire_dict=dict()
for dvo in first_gates_to_outputs:
    wires_out_from_xor=find_XOR_to_output(dvo[0],gate_dict)
    try:
        swap_wire_dict[dvo[0]]+=wires_out_from_xor
    except:
        swap_wire_dict[dvo[0]]=wires_out_from_xor
#at this point the output wires z12-kwb were matched as a swap

#checking output validity
deviating_output=[] #output wires that don't follow from an XOR-gate
misconnected_io=[] #output wires that is not connected to the corresponding bit inputs through 2 XOR-gates
for _,wire_ in output_wires[:-1]:
    if gate_dict[wire_].operator!='XOR':
        deviating_output.append((wire_,gate_dict[wire_].operator))
        wires_out_from_xor=find_XOR_to_output(wire_,gate_dict)
        try:
            swap_wire_dict[wire_]+=wires_out_from_xor
        except:
            swap_wire_dict[wire_]=wires_out_from_xor
    #kolla att XOR-på output är ansluten till 2a XOR från inputs
    else:
        if wire_!='z00':
            wires_out_from_xor=find_XOR_to_output(wire_,gate_dict)
            if len(wires_out_from_xor)==0 or wires_out_from_xor[0]!=wire_: #if there are no wires from the first XOR-gate that the inputs are connected to that lead to a second XOR-gate or if the output wire is the same as the output wire that is being checked
                wire_int=int(wire_[1:])
                if wire_int<10:
                    wire_int_str=f'0{wire_int}'
                else:
                    wire_int_str=str(wire_int)
                swappable_output_wires=[]
                for wire__ in adjacency_dict[f"x{wire_int_str}"]: #start from x input and the output wire from the XOR-gate connected to the x input, the input to the XOR-gate connected to the output (that is should be connected to the x input's XOR-gate) can be swapped with the output wire of the input's first XOR-gate
                    if gate_dict[wire__].operator=='XOR':
                        swappable_output_wires.append(wire__)
                        break
                misconnected_io.append((wire_,swappable_output_wires))
#at this point, 2 more swappable output wires: z16-qkf and z24-tgr had been found. a misconnected input-output was also found z29, which the output port from ths first XOR-gate needs to be matched with an input port to an XOR-gate connected to z29 -this is done in the loop below
for o_,i_list in misconnected_io:
    input_wires_to_output=[gate_dict[o_].wire_1,gate_dict[o_].wire_2]
    for i_ in i_list:
        try:
            swap_wire_dict[i_]+=input_wires_to_output
        except:
            swap_wire_dict[i_]=input_wires_to_output
assert len(swap_wire_dict)==4, f"There should be 4 wire pairs to swap, found at least {len(swap_wire_dict)} potential pairs" #assume that 4 have been found from here on
individual_combinations=[]
for wire_to_swap,swappable_alternatives in swap_wire_dict.items():
    individual_combinations.append([(wire_to_swap,sa) for sa in set(swappable_alternatives)])
overall_combinations=[]
for combination_0 in individual_combinations[0]:
    for combination_1 in individual_combinations[1]:
        for combination_2 in individual_combinations[2]:
            for combination_3 in individual_combinations[3]:
                overall_combinations.append(sorted([combination_0,combination_1,combination_2,combination_3]))

#reference dictionary with input->output strings to modify
gate_str_dict=dict()
for gate_str in gate_part.split('\n'):
    _,wire_output=gate_str.split(' -> ')
    gate_str_dict[wire_output]=gate_str

for o_c in overall_combinations:
    gate_str_dict_mod=deepcopy(gate_str_dict) #dictionary to modify with swaps
    #swap outputs
    for output_wire_1,output_wire_2 in o_c:
        input_part_1,_=gate_str_dict_mod[output_wire_1].split(' -> ')
        input_part_2,_=gate_str_dict_mod[output_wire_2].split(' -> ')
        gate_str_dict_mod[output_wire_1]=f"{input_part_2} -> {output_wire_1}"
        gate_str_dict_mod[output_wire_2]=f"{input_part_1} -> {output_wire_2}"
    #make new gate part (of input to run)
    gate_part_mod=''
    for _,gate_str_ in gate_str_dict_mod.items():
        gate_part_mod+=gate_str_+'\n'
    gate_part_mod=gate_part_mod[:-1] #remove last linebreak
    #reset/re-initiate the wire values
    gate_queue_mod,output_wires_mod,wire_dict_mod,initial_wires_mod,gate_dict_mod,adjacency_dict_mod,wire_combo_dict_mod=reset(wire_part,gate_part_mod)
    #run with swapped output wires
    binary_output_str_mod,binary_output_bools_mod=get_output_bits(gate_queue_mod,output_wires_mod,wire_dict_mod)
    #print all gates that should be swapped
    int_output=int(binary_output_str_mod[::-1],2)
    if int_output==correct_output:
        all_swapped_output_wires=[]
        for output_wires in o_c:
            for output_wire_ in output_wires:
                all_swapped_output_wires.append(output_wire_)
        print('2nd:',','.join(sorted(all_swapped_output_wires)))
#got two answers that gave the correct output, submitted the first and got the star
#cph,jqn,kwb,qkf,tgr,z12,z16,z24 (submitted)
#cph,kwb,qkf,rwq,tgr,z12,z16,z24


#some of the useful debugging checks that lead to the solution
# 1
# #för z29 leder ej XOR från x29 å y29 till XOR som går till z29
# #om kollar
# for ww in range(45):
#     if ww<10:
#         ww_str=f'0{ww}'
#     else:
#         ww_str=str(ww)
#     for w in adjacency_dict[f"x{ww_str}"]:
#         if w[0]!='z' and gate_dict[w].operator=='XOR':
#             print(ww,[gate_dict[w_].operator for w_ in adjacency_dict[w]])
# #shows that 29 has OR instead of AND,XOR like the others

# for _,zo in output_wires:
#     op_str=''
#     try:
#         for zo_inp_wire in [gate_dict[zo].wire_1,gate_dict[zo].wire_2]:
#             op_str+=gate_dict[zo_inp_wire].operator+','
#         print(zo,op_str[:-1])
#     except:
#         print(zo)
#     # h=[adjacency_dict[ss] for ss in g];print(g,h)

# wire_='z16'
# gate_input_wires=[gate_dict[wire_].wire_1,gate_dict[wire_].wire_2]
# input_wires_gate_operators=[gate_dict[wire_].operator for wire_ in gate_input_wires]
# adjacent_output_wires=[adjacency_dict[ss] for ss in gate_input_wires]
# print(gate_input_wires,adjacent_output_wires,input_wires_gate_operators)

# #problem: z_str='z24';g=[gate_dict[z_str].wire_1,gate_dict[z_str].wire_2];h=[adjacency_dict[ss] for ss in g];print(g,h)
# #gives ['vhm', 'wwd'] [['z24'], ['z24']], should be 2 wires in lists to the right
# #['vhm', 'wwd'] both have AND gates, via zs='vhm';print(gate_dict[zs].wire_1,gate_dict[zs].wire_2,gate_dict[zs].operator)
# #if one checks z_str='z14' => ['wmg', 'jqt'] [['pjp', 'z14'], ['pjp', 'z14']]
# # zs='wmg';print(gate_dict[zs].wire_1,gate_dict[zs].wire_2,gate_dict[zs].operator)
# # zs='jqt';print(gate_dict[zs].wire_1,gate_dict[zs].wire_2,gate_dict[zs].operator)
# #gives one OR and one XOR, same for z11

