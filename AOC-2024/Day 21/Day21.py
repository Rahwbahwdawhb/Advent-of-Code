import os
from bisect import insort
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    codes=f.read().strip().split('\n')

#stuff that I found made the problem tricky:
#*it was a bit involved (not too hard but fiddly) to set up set up dictionaries for movement on numeric and directional keypads
#*the differences between key combinations that had the same path lengths and gave the same path lengths for one iteration would start diverging after several iterations
# this made it difficult to remove them in a simple way for part 2
#*the shortest path for multiple iterations might result from a string that did not necesserily give the shortest path for a lower number of iterations (from the numeric keypad dict)

#initially looked at number of direction changes to differentiate propagation strings, but the importance was how many more keys those direction changes (different moves) those moves resulted in after several iterations
#-it was better to track number characters in future strings after several iterations to differentiate
#-to come to the solution, it was helpful to check how strings from the numeric dict evolved after the 2 first iterations
#--first to see the difference that equal length strings could result in after some iterations, especially with different possible variants (hinted about the need of filtering them)
#--second to use for verification when propagating count_dicts


def get_movement_dict(keypad):
    #take list of lists inputs where each "inner" list corresponds to keys on a row, topmost row comes first
    #return dictionary with keys=move from one key to another, values=shortest paths to go between those keys
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    direction_strs=['v','^','>','<']
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
                                            path_length_to_match=len(path_str) #shortest path reaches the target key first, so match for other paths
                                        if len(path_str)==path_length_to_match:
                                            change_sum=0 #changing directions means more moves for controlling keypad to adjust, so differentiate paths of equal steps by number of direction changes
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
numeric_dict=get_movement_dict(keypad_numeric)
directional_dict=get_movement_dict(keypad_directional)

def get_all_possible_paths(possible_paths,move_dict,move):
    new_paths=[]
    minimum_moves=move_dict[move][0][0]
    while possible_paths:
        move_str=possible_paths.pop(0)
        for moves_,path_ in move_dict[move]:
            if moves_==minimum_moves:
                new_paths.append(move_str+path_+'A')
    return new_paths

# #1st solution to part 1: look at all paths for 2 iterations and find the shortest among them
# complexity_sum_1=0
# for code_ in codes:
#     code='A'+code_
#     possible_paths=['A']
#     for i in range(4):
#         move=code[i]+code[i+1]
#         possible_paths=get_all_possible_paths(possible_paths,numeric_dict,move)
#     all_possible_paths=[x for x in possible_paths]
#     for _ in range(2):
#         all_possible_paths_=[]
#         while all_possible_paths:
#             directional_input=all_possible_paths.pop(0)
#             all_possible_paths_iter=['A']
#             for i in range(len(directional_input)-1):
#                 move=directional_input[i]+directional_input[i+1]
#                 all_possible_paths_iter=get_all_possible_paths(all_possible_paths_iter,directional_dict,move)
#             all_possible_paths_+=all_possible_paths_iter
#         all_possible_paths=all_possible_paths_
#     cs=[]
#     L=[]
#     for p in all_possible_paths:
#         cs.append(len(p[1:])*int(code_.strip('0').strip('A')))
#         L.append(len(p))
#     complexity_sum_1+=min(cs)
# print(complexity_sum_1)


#part 2 + part 1 again
#robot fingerse always start from A, and whenever a press is to be made an A is pressed
#thus, each command from a robot to tell another robot to move will be of the form A...A where ... are arrow-directions
#each move sequence be split into its A_str components (the A...A that make it up)
#each A_str will give rise to new A_strs for every iteration (when one robot tells another robot how to move)
#1. construct a dictionary that has keys=A_strs and values=A_strs that the key-A_str spawns during one iteration
#2. represent a given sequence of A_strs by a ditionary with keys=A_str and values=number of times the key-A_str occurs (only the number of chacarcters is of interest and the A_strs-evoluations can be checked independently)
#3. use the dictionary in 1. to propagate a dictionary in 2.
#4. the dictionary in 1. contains several different possible evolutions (in 1 iteration a general A_str can can be synthesized in diffrent ways that have the same number of characters/steps)
#   one must therefore filter the possibilities by iterating the A_strs until a difference between the options is obtained.
#   setting the number of iterations high from the beginning does not work because there are too many possibilites
#   the trick is to start with an iteration of 1 and remove the options that generate longer sequences (the summation of all the items in the dict from 2.)
#   and then increase the iteration and removing options in the same way until only one option remains for each A_str-key in the dict from 2.
#5. obtain direction/A_str represantations of the codes and use the dict from 4. to propagate them 2 times for part 1 and 25 times for part 2

def get_count_dict(check_str): #generate a dict from 4. from an input string
    count_dict=dict()
    for _str in check_str.split('A')[1:-1]:
        A_str=f"A{_str}A"
        try:
            count_dict[A_str]+=1
        except:
            count_dict[A_str]=1
    return count_dict
def count_dict_to_character_count(count_dict): #return the character count=length of a count_dict
    charachter_count=0
    for A_str_iter,count_iter in count_dict.items():
        charachter_count+=count_iter*(len(A_str_iter)-1) #subtract 1 because the starting A is not a key-press and each "ending" A is shared between two A_strs, subtracting 1 gets rid of all these extra counts
    return charachter_count

#generate dict from 1.
A_str_spawn_dict=dict()
loop_queue=[]
for numeric_move,move_list in numeric_dict.items(): #loop through all possible shortest paths between keys on the numeric keypad and turn them into A_strs
    for _,move_str in move_list:
        if move_str=='':
            new_move_strs=['A'] #move from a given button to itself means pressing A
        else:
            move_str_=f"A{move_str}" #start from A key and add on future sequence
            new_move_strs=['']
            for i in range(len(move_str_)-1): #check how each move between two keys can be achieved with the directional keypad
                variations=directional_dict[move_str_[i:i+1+1]]                
                temp=[]
                while new_move_strs: #append all variations to the currently obtained A_str (from the directional keypad)
                    new_move_str_0=new_move_strs.pop(0)
                    for _,variation in variations:
                        temp.append(new_move_str_0+variation+'A') #add an A after each direction sequence to mark a key press on the A-key
                new_move_strs=temp
        for new_move_str in new_move_strs: #loop through all variations of the full A_strs
            spawned_str_snippets=new_move_str.split('A')[:-1] #find the "building block" A_strs and loop through them, last one is removed since that's a trailing '' representing that nothing exists after the last A...
            for _str in spawned_str_snippets+[move_str]:
                A_str=f"A{_str}A"
                if A_str not in A_str_spawn_dict: #add the "building block" A_strs as keys to the spawn dict
                    A_str_spawn_dict[A_str]=set()
                    loop_queue.append(A_str) #also add them to a loop queue to populate values for these keys in the loop below

while loop_queue:
    A_str=loop_queue.pop(0)
    new_move_strs=['']
    #generate full move-strings = concatenated A_strs for all variations
    for i in range(len(A_str)-1):
        variations=directional_dict[A_str[i:i+1+1]] 
        temp=[]
        while new_move_strs:
            new_move_str_0=new_move_strs.pop(0)
            for _,variation in variations:
                temp.append(new_move_str_0+variation+'A')
        new_move_strs=temp
    #go through all the move-strings from above and split them into A_strs
    for new_move_str in new_move_strs:
        spawned_str_snippets=new_move_str.split('A')[:-1]
        spawned_Astrs=[]
        for _str in spawned_str_snippets: #go through the A_strs and add them to a list to be stored as the value for the key-A_str, i.e. the A_strs that the key-A_str generate
            A_str_=f"A{_str}A"
            spawned_Astrs.append(A_str_)
            if A_str_ not in A_str_spawn_dict: #if a new A_str pops up that wasn't covered before, add it to the loop queue so that the same procedure can be repeated for it, just an extra precaution it did not trigger for me
                A_str_spawn_dict[A_str_]=set()
                loop_queue.append(A_str_)
        A_str_spawn_dict[A_str].add(tuple(sorted(spawned_Astrs))) #turn the A_strs from one variation into a tuple and sort it so that it can uniquely be added to a set to avoid duplicates

for key,value in A_str_spawn_dict.items(): #turn the A_str_spawn_dict value to lists instead of sets for easier future handling
    A_str_spawn_dict[key]=list(value)

def iterate_count_dict(count_dict,spawn_dict):
    iterated_count_dicts=[dict()]
    #loop through the input count_dict (its A_strs and their counts) and create new count_dicts that has the same counts for those A_strs +the counts (and possibly new A_str) that they key-A_strs in input count_dict generate after a new iteration (look up which A_strs that are generated for each key-A_str in the spawn_dict)
    for A_str,count in count_dict.items():
        new_iterated_count_dicts=[] #holds all count_dicts generated from the different variants supported by each A_str-key in the spawn_dict
        spawn_variant_counts=[] #holds the corresponding character counts, i.e. sum of A_str-length (-1 to avoid excess A:s) multiplied by number of occurences for each count_dict variant
        while iterated_count_dicts:
            previous_iterated_count_dict=iterated_count_dicts.pop(0)            
            for spawn_distribution in spawn_dict[A_str]:
                iterated_count_dict=dict()
                spawn_variant_count=0
                for key,value in previous_iterated_count_dict.items(): #initiates the count_dict and its character count from previous iterations, that new spawned A_strs will be added to due to the key-A_str spawn_dict[A_str]
                    iterated_count_dict[key]=value
                    spawn_variant_count+=value*(len(key)-1)
                for A_str_spawned in spawn_distribution: #go through each spawned A_str and add its count to the initiated count_dict and the corresponding character count to its count-tally
                    try:
                        iterated_count_dict[A_str_spawned]+=count
                    except:
                        iterated_count_dict[A_str_spawned]=count
                    spawn_variant_count+=(len(A_str_spawned)-1)*count
                new_iterated_count_dicts.append(iterated_count_dict) #add the updated (new counts added to it through above loop) to a list that holds the count_dict variants from the latest iteration
                spawn_variant_counts.append(spawn_variant_count) #add latest character counts to similar list
        iterated_count_dicts=new_iterated_count_dicts
    return iterated_count_dicts,spawn_variant_counts #return the last iterated count_dicts and the corresponding character counts

def A_str_iter_min(A_str,N_iter,spawn_dict): #return the least number of spawn_variants that A_str will generate after an iteration through spawn_dict
    iterated_count_dicts_0=[get_count_dict(A_str)] #A_str=>count_dict to iterate
    for _ in range(N_iter):
        min_spawn_variant_counts=[]
        next_iterated_count_dicts=[]
        while iterated_count_dicts_0:
            _count_dict=iterated_count_dicts_0.pop(0)
            iterated_count_dicts,spawn_variant_counts=iterate_count_dict(_count_dict,spawn_dict)
            min_spawn_variant_counts.append(min(spawn_variant_counts))
            next_iterated_count_dicts+=iterated_count_dicts
        iterated_count_dicts_0=next_iterated_count_dicts
    current_min=min(min_spawn_variant_counts)
    return current_min

def filtered_count_dict_iterate(count_dict,filtered_spawn_dict): #will grab the 1st entry in the spawn_dict and use to iterate A_strs, thus only suitable after filtering the spawn_dict to only have 1 entry for each A_str!
    iterated_count_dict=dict()
    for A_str,count in count_dict.items():
        if count>0:
            next_pick=filtered_spawn_dict[A_str][0]
            for A_str_spawned in next_pick:
                try:
                    iterated_count_dict[A_str_spawned]+=count
                except:
                    iterated_count_dict[A_str_spawned]=count
    return iterated_count_dict

#probably the most important function for this implementation of part 2 to work
def filter_spawn_dict(spawn_dict_to_filter,spawn_dict,N_iter):
    A_str_spawn_dict_filtered=dict()
    next_iteration_dict=dict()
    for A_str_key,A_str_spawn_variations in spawn_dict_to_filter.items():
        if len(A_str_spawn_variations)>1:
            spawns_dict=dict()      
            min_spawns_value=10**18
            for spawns in A_str_spawn_variations:
                actual_A_str='A'
                for _A_str in spawns: #concatenate A_strs that the current spawn has into one A_str (removing overlapping A:s)
                    actual_A_str+=_A_str[1:]
                #check minimum spawns that can be generated from the concatenated A_str and store the spawns in a dictionary with keys=least number of future spawns and values=spawns
                current_min=A_str_iter_min(actual_A_str,N_iter,spawn_dict)
                min_spawns_value=min([min_spawns_value,current_min])
                try:
                    spawns_dict[current_min].append(spawns)
                except:
                    spawns_dict[current_min]=[spawns]
            A_str_spawn_dict_filtered[A_str_key]=spawns_dict[min_spawns_value] #save the spawns that generated the fewest future spawns in the filtered dict
            if len(spawns_dict[min_spawns_value])>1: #if the current filter has more than 1 possible variant, put it in a dictionary that will be used for future filtering
                next_iteration_dict[A_str_key]=spawns_dict[min_spawns_value]
    for A_str_key,A_str_spawn_variations in  spawn_dict.items(): #Add A_str-keys that are already filtered down to have 1 variant to the filtered dict
        if A_str_key not in A_str_spawn_dict_filtered:
            A_str_spawn_dict_filtered[A_str_key]=A_str_spawn_variations
    return A_str_spawn_dict_filtered,next_iteration_dict

#filter A_str_spawn_dict
N_iter=1 #number of iterations to use for first filtering
left_to_filter=A_str_spawn_dict
filtered_spawn_dict=A_str_spawn_dict
#keep filtering until all A_str_spawn_dict values are lists with 1 entry, this is when the left_fo_filter dict has a length of 0
#when first solving it I manually filtered it in this manner by trying different values for N_iter
while True:
    filtered_spawn_dict,left_to_filter=filter_spawn_dict(left_to_filter,filtered_spawn_dict,N_iter)
    if len(left_to_filter)==0:
        break
    N_iter+=1

complexity_sum_1=0
complexity_sum_2=0
for code_ in codes:
    code='A'+code_
    numeric_keypad_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1] #move=from a key to the following key
        numeric_keypad_paths=get_all_possible_paths(numeric_keypad_paths,numeric_dict,move) #return all different shortest paths between the keys specified in the move above, if new options appear all previous paths are prepended to these new options and all the resulting paths are returned
    min_iter_count=10**18
    sum_1_counts=[] #counts of path lengths after 2 iterations for the different numeric keypads from above, the minimum value will be used to calculate the complexity sum
    for key_path in numeric_keypad_paths:
        key_path_count_dict=get_count_dict(key_path) #convert the key path to a dictionary with key=A-strings and values=count of how many times the A-strings appear in the key path
        for iter in range(25): #run one loop to cover both part 1 and part 2
            key_path_count_dict=filtered_count_dict_iterate(key_path_count_dict,filtered_spawn_dict)
            if iter==1: #part 1 only has 2 iterations
                iter_count=count_dict_to_character_count(key_path_count_dict)
                sum_1_counts.append(iter_count)
        iter_count=count_dict_to_character_count(key_path_count_dict)
        if iter_count<min_iter_count:
            min_iter_count=iter_count
    code_integer=int(code_.strip('0').strip('A'))
    complexity_sum_1+=min(sum_1_counts)*code_integer
    complexity_sum_2+=min_iter_count*code_integer
print('1st:',complexity_sum_1)
print('2nd:',complexity_sum_2)