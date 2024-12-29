import os
from bisect import insort
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    codes=f.read().strip().split('\n')

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
keypad_numeric=[['7','8','9'],['4','5','6'],['1','2','3'],[None,'0','A']]
"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
keypad_directional=[[None,'^','A'],['<','v','>']]
directions=[(1,0),(-1,0),(0,1),(0,-1)]
direction_strs=['v','^','>','<']

def get_movement_dict(keypad):
    row_max=len(keypad)-1
    col_max=len(keypad[0])-1
    movement_dict=dict()
    for i0,key_row in enumerate(keypad):
        for i1,start_key in enumerate(key_row):
            if start_key:
                for key_row_2 in keypad:
                    for end_key in key_row_2:
                        if end_key:
                            if start_key==end_key:
                                movement_dict[start_key+start_key]=[(0,'')]
                            else:
                                visited={(i0,i1)}
                                queue=[((i0,i1),start_key,'')]
                                paths=[]
                                while True:
                                    try:
                                        position,key,path_str=queue.pop(0)
                                    except: #if all valid keys have been visited
                                        break
                                    if key!=end_key:
                                        visited.add(position)
                                    if key==end_key:
                                        if len(paths)==0:
                                            path_length_to_match=len(path_str)
                                        if len(path_str)==path_length_to_match:
                                            change_sum=0
                                            last_key=path_str[0]
                                            try:
                                                for key_ in path_str[1:]:
                                                    if key_!=last_key:
                                                        change_sum+=1
                                                    last_key=key_
                                            except:
                                                pass
                                            insort(paths,(change_sum,path_str))
                                    else:
                                        for d,ds in zip(directions,direction_strs):
                                            new_position=(position[0]+d[0],position[1]+d[1])                                
                                            if 0<=new_position[0]<=row_max and 0<=new_position[1]<=col_max and new_position not in visited:
                                                new_key=keypad[new_position[0]][new_position[1]]
                                                if new_key!=None:
                                                    queue.append((new_position,new_key,path_str+ds))
                                movement_dict[start_key+end_key]=paths
    return movement_dict

numeric_dict=get_movement_dict(keypad_numeric)
directional_dict=get_movement_dict(keypad_directional)

def get_paths_2(possible_paths,move_dict,move):
    new_paths=[]
    minimum_moves=move_dict[move][0][0]
    while possible_paths:
        move_str=possible_paths.pop(0)
        for moves_,path_ in move_dict[move]:
            if moves_==minimum_moves:
                new_paths.append(move_str+path_+'A')
    return new_paths

complexity_sum_3=0
for code_ in codes:
    code='A'+code_
    possible_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1]
        possible_paths=get_paths_2(possible_paths,numeric_dict,move)
    all_possible_paths=[x for x in possible_paths]
    it_dicts=[]
    for _ in range(2):
        all_possible_paths_=[]
        it_dict=dict()
        while all_possible_paths:
            directional_input=all_possible_paths.pop(0)
            all_possible_paths_iter=['A']
            for i in range(len(directional_input)-1):
                move=directional_input[i]+directional_input[i+1]
                all_possible_paths_iter=get_paths_2(all_possible_paths_iter,directional_dict,move)
            all_possible_paths_+=all_possible_paths_iter
            it_dict[directional_input]=all_possible_paths_iter
        all_possible_paths=all_possible_paths_
        it_dicts.append(it_dict)
    cs=[]
    L=[]
    for p in all_possible_paths:
        cs.append(len(p[1:])*int(code_.strip('0').strip('A')))
        L.append(len(p))
    complexity_sum_3+=min(cs)
print(complexity_sum_3)


#part 2
def count_dict_to_character_count(count_dict):
    charachter_count=0
    for A_str_iter,count_iter in count_dict.items():
        charachter_count+=count_iter*(len(A_str_iter)-1)
    return charachter_count

# #verification of correct characters when propagating dictionary representation of movement strings
# def get_next_Astr(A_str,move_dict):
#     new_move_str=''
#     for i in range(len(A_str)-1):
#         new_move_str+=move_dict[A_str[i:i+1+1]][0][1]+'A'
#     return 'A'+new_move_str
# A_str_start=possible_paths[0]
# A_str_=A_str_start
# count_dict_iter=get_count_dict(A_str_start)
# for ii in range(10):
#     count_dict_iter=iterate_count_dict(count_dict_iter)
#     A_str_=get_next_Astr(A_str_,directional_dict)
#     count_dict_ref=get_count_dict(A_str_)
#     print(ii,count_dict_iter==count_dict_ref,len(A_str_[1:]),count_dict_to_character_count(count_dict_iter))

#ny spawned_dict
directional_dict.keys()
spawn_Adelimited_move_strs_dict_3=dict()
loop_queue=[]
for numeric_move,move_list in numeric_dict.items():
    for _,move_str in move_list:
        if move_str=='':
            new_move_strs=['A']
        else:
            move_str_=f"A{move_str}"
            new_move_strs=['']
            for i in range(len(move_str_)-1):
                variations=directional_dict[move_str_[i:i+1+1]]                
                temp=[]
                while new_move_strs:
                    new_move_str_0=new_move_strs.pop(0)
                    for _,variation in variations:
                        temp.append(new_move_str_0+variation+'A')
                new_move_strs=temp
        for new_move_str in new_move_strs:
            spawned_Adelimited_move_strs=new_move_str.split('A')[:-1]
            for _str in spawned_Adelimited_move_strs+[move_str]:
                A_str=f"A{_str}A"
                if A_str not in spawn_Adelimited_move_strs_dict_3:
                    spawn_Adelimited_move_strs_dict_3[A_str]=set()
                    loop_queue.append(A_str)

while loop_queue:
    A_str=loop_queue.pop(0)
    new_move_strs=['']
    for i in range(len(A_str)-1):
        variations=directional_dict[A_str[i:i+1+1]]                
        temp=[]
        while new_move_strs:
            new_move_str_0=new_move_strs.pop(0)
            for _,variation in variations:
                temp.append(new_move_str_0+variation+'A')
        new_move_strs=temp

    for new_move_str in new_move_strs:
        spawned_Adelimited_move_strs=new_move_str.split('A')[:-1]
        spawned_Astrs=[]
        for _str in spawned_Adelimited_move_strs:
            A_str_=f"A{_str}A"
            spawned_Astrs.append(A_str_)
            if A_str_ not in spawn_Adelimited_move_strs_dict_3:
                spawn_Adelimited_move_strs_dict_3[A_str_]=set()
                loop_queue.append(A_str_)
        spawn_Adelimited_move_strs_dict_3[A_str].add(tuple(sorted(spawned_Astrs)))

def get_count_dict_2(check_str):
    count_dict=dict()
    for _str in check_str.split('A')[1:-1]:
        A_str=f"A{_str}A"
        try:
            count_dict[A_str]+=1
        except:
            count_dict[A_str]=1
    return count_dict
def iterate_count_dict_2(count_dict,spawn_dict,step_dict):
    iterated_count_dicts=[dict()]
    for A_str,count in count_dict.items():
        new_iterated_count_dicts=[]
        spawn_variant_counts=[]
        spawn_changes_sums=[]
        while iterated_count_dicts:
            previous_iterated_count_dict=iterated_count_dicts.pop(0)            
            for spawn_distribution in spawn_dict[A_str]:
                iterated_count_dict={key:value for key,value in previous_iterated_count_dict.items()}
                iterated_count_dict=dict()
                spawn_variant_count=0
                spawn_changes_sum=0
                for key,value in previous_iterated_count_dict.items():
                    iterated_count_dict[key]=value
                    spawn_variant_count+=value*(len(key)-1)
                for A_str_spawned in spawn_distribution:
                    try:
                        iterated_count_dict[A_str_spawned]+=count
                    except:
                        iterated_count_dict[A_str_spawned]=count
                    spawn_variant_count+=(len(A_str_spawned)-1)*count
                    ch_o=A_str_spawned[0]
                    for ch in A_str_spawned[1:]:
                        spawn_changes_sum+=step_dict[ch_o+ch]
                        ch_o=ch
                new_iterated_count_dicts.append(iterated_count_dict)
                spawn_variant_counts.append(spawn_variant_count)
                spawn_changes_sums.append(spawn_changes_sum)
        iterated_count_dicts=new_iterated_count_dicts
    return iterated_count_dicts,spawn_variant_counts,spawn_changes_sums

possible_paths=['A']
for i in range(4):
    move=code[i]+code[i+1]
    possible_paths=get_paths_2(possible_paths,numeric_dict,move)
A_str_code=possible_paths[0]
_str_blocks=A_str_code.split('A')[1:-1]
for _str_block in _str_blocks:
    A_str_block=f"A{_str_block}A"
A_str_count_dict=get_count_dict_2(A_str_block)

directional_step_dict={key:len(info[1]) for key,value in directional_dict.items() for info in value}


def A_str_iter_min(A_str,N_iter,spawn_dict):
    iterated_count_dicts_0=[get_count_dict_2(A_str)]
    if N_iter<=2:
        for _ in range(N_iter):
            min_spawn_variant_counts=[]
            while iterated_count_dicts_0:
                _count_dict=iterated_count_dicts_0.pop(0)
                iterated_count_dicts,spawn_variant_counts,_=iterate_count_dict_2(_count_dict,spawn_dict,directional_step_dict)
                min_spawn_variant_counts.append(min(spawn_variant_counts))
            iterated_count_dicts_0=iterated_count_dicts
    else:
        for _ in range(N_iter):
            min_spawn_variant_counts=[]
            next_iterated_count_dicts=[]
            while iterated_count_dicts_0:
                _count_dict=iterated_count_dicts_0.pop(0)
                iterated_count_dicts,spawn_variant_counts,_=iterate_count_dict_2(_count_dict,spawn_dict,directional_step_dict)
                min_spawn_variant_counts.append(min(spawn_variant_counts))
                next_iterated_count_dicts+=iterated_count_dicts
            iterated_count_dicts_0=next_iterated_count_dicts
    current_min=min(min_spawn_variant_counts)
    return current_min

def iterate_count_dict_first_grab(count_dict,spawn_dict):
    iterated_count_dict=dict()
    for A_str,count in count_dict.items():
        if count>0:
            next_pick=spawn_dict[A_str][0]
            for A_str_spawned in next_pick:
                try:
                    iterated_count_dict[A_str_spawned]+=count
                except:
                    iterated_count_dict[A_str_spawned]=count
    return iterated_count_dict

def filter_spawn_dict(spawn_Adelimited_move_strs_dict_to_filter,spawn_Adelimited_move_strs_dict,N_iter):
    spawn_Adelimited_move_strs_dict_3_filtered=dict()
    next_iteration_dict=dict()
    for A_str_key,A_str_spawn_variations in spawn_Adelimited_move_strs_dict_to_filter.items():
        if len(A_str_spawn_variations)>1:
            spawns_dict=dict()      
            min_spawns_value=10**18
            for spawns in A_str_spawn_variations:
                actual_A_str='A'
                for _A_str in spawns:
                    actual_A_str+=_A_str[1:]
                current_min=A_str_iter_min(actual_A_str,N_iter,spawn_Adelimited_move_strs_dict)
                min_spawns_value=min([min_spawns_value,current_min])
                try:
                    spawns_dict[current_min].append(spawns)
                except:
                    spawns_dict[current_min]=[spawns]
            spawn_Adelimited_move_strs_dict_3_filtered[A_str_key]=spawns_dict[min_spawns_value]
            if len(spawns_dict[min_spawns_value])>1:
                next_iteration_dict[A_str_key]=spawns_dict[min_spawns_value]
        else:
            spawn_Adelimited_move_strs_dict_3_filtered[A_str_key]=A_str_spawn_variations
    for A_str_key,A_str_spawn_variations in  spawn_Adelimited_move_strs_dict.items():
        if A_str_key not in spawn_Adelimited_move_strs_dict_3_filtered:
            spawn_Adelimited_move_strs_dict_3_filtered[A_str_key]=A_str_spawn_variations
    return spawn_Adelimited_move_strs_dict_3_filtered,next_iteration_dict

for key,value in spawn_Adelimited_move_strs_dict_3.items():
    spawn_Adelimited_move_strs_dict_3[key]=list(value)
N_iter=1
left_to_filter=spawn_Adelimited_move_strs_dict_3
filtered_spawn_dict=spawn_Adelimited_move_strs_dict_3
while True:
    filtered_spawn_dict,left_to_filter=filter_spawn_dict(left_to_filter,filtered_spawn_dict,N_iter)
    if len(left_to_filter)==0:
        break
    N_iter+=1


1
complexity_sum_1=0
complexity_sum_2=0
for code_ in codes:
    code='A'+code_
    numeric_keypad_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1] #move=from a key to the following key
        numeric_keypad_paths=get_paths_2(numeric_keypad_paths,numeric_dict,move) #return all different shortest paths between the keys specified in the move above, if new options appear all previous paths are prepended to these new options and all the resulting paths are returned
    min_iter_count=10**18
    sum_1_counts=[] #counts of path lengths after 2 iterations for the different numeric keypads from above, the minimum value will be used to calculate the complexity sum
    for key_path in numeric_keypad_paths:
        key_path_count_dict=get_count_dict_2(key_path) #convert the key path to a dictionary with key=A-strings and values=count of how many times the A-strings appear in the key path
        for iter in range(25): #run one loop to cover both part 1 and part 2
            # key_path_count_dict=iterate_count_dict_first_grab(key_path_count_dict,spawn_Adelimited_move_strs_dict_3_filtered_2)
            key_path_count_dict=iterate_count_dict_first_grab(key_path_count_dict,filtered_spawn_dict)
            if iter==1: #part 1 only has 2 iterations
                iter_count=count_dict_to_character_count(key_path_count_dict)
                sum_1_counts.append(iter_count)
        iter_count=count_dict_to_character_count(key_path_count_dict)
        if iter_count<min_iter_count:
            min_iter_count=iter_count
    code_integer=int(code_.strip('0').strip('A'))
    complexity_sum_1+=min(sum_1_counts)*code_integer
    complexity_sum_2+=min_iter_count*code_integer
print('1st:',complexity_sum_1,complexity_sum_1==157908)
print('2nd:',complexity_sum_2,complexity_sum_2==196910339808654)