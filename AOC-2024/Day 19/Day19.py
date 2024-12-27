import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    available_towel_str,designs_str=f.read().strip().split('\n\n')

towel_design_dict=dict() #keep track of designs that can be done, keys=towel designs and values=bool
base_towel_dict=dict() #for 2nd part, keys=first letter of available towel string values=available towel strings starting with the first letter specified by the key
for at in available_towel_str.split(','):
    towel_design_dict[at.strip()]=True
    at=at.strip()
    try:
        base_towel_dict[at[0]].add(at)
    except:
        base_towel_dict[at[0]]={at}
#recursively check snippets (one from the left and one from the right, one at a time) of the towel string that grow in length
#check if the snippet is in the base_towel_dict, if so return its associated bool
#if not, split the snippet further and check the new snippets recursively
#ultimately one gets down to snippets with lengths of 1 and if these are not in the base_towel_dict they and the designs they are part of cannot be made so return false
#update base_towel_dict with the returned bools for each towel string that is investigated (since done recursively, this will also be made for snippets)
def recursive_check(towel_str):
    try:
        return towel_design_dict[towel_str]
    except:
        N=len(towel_str)
        if N==1:
            return False
        possible_design_bool=False
        for i in range(len(towel_str)-1):
            towel_str_1=towel_str[:i+1]
            towel_str_2=towel_str[i+1:]
            check1=recursive_check(towel_str_1)
            if i<N-1:
                check2=recursive_check(towel_str_2)
            else:
                check2=True
            towel_design_dict[towel_str_1]=check1
            towel_design_dict[towel_str_2]=check2
            if check1 and check2:
                possible_design_bool=True
        return possible_design_bool

possible_designs=0 #answer to part 1
possible_combinations=0 #answer to part 2
for design in designs_str.split('\n'):
    design_bool=recursive_check(design)
    possible_designs+=design_bool
    #part 2
    #for designs that are possible, start from the left of the string and check the base towel designs (in base_towel_dict) that can match
    #the string from the leftmost character onwards, for each onward match, add 1 to an index counter (one slot for each index of the towel design string +one extra, *commented below)
    #at an index that represents stepping the full length from the start character until after the full matching base towel design
    #go to the next position in the string and repeat this procedure IF the count at the index counter for the 2nd character (=1) is not 0
    #for each base towel design that matches now add the number in the current counter index slot to the counter index slot that matches stepping past the full length of the matching base towel design
    #if some base design would extend past the last index of the counter array, ignore it and try the next one
    #after the design towel string has been looped through, the number of possible combinations will be found in the last index slot of the counter array -so add this number to the sum total
    
    #*it was important to add 1 extra slot in the counter array because when stepping past the full length of the matching base towel string one ends up 1 index past the length of the towel design string!
    #if one just pushes these values back to the index slot in the counter array that matches the last index, then these counts will overlap the counts that represents steps that made it to the second last character!
    #-which will in general produce a summation that is incorrect (too large) unless there was a base towel string with a single character that matches that last step!

    #initially found all base towel strings that were used to match the design towel string (a subset of the base towel strings) and set up unique dictionaries for each design towel string to check combinations for
    #this setting up of new dictionaries proved much slower than just using a single dictionary with all base towel strings
    if design_bool:
        N_design=len(design)
        combination_counter=[0 for _ in range(N_design+1)] #*adding an extra slot to only count the steps that made it all the way to the end
        combination_counter[0]=1
        i=0
        while i<N_design:
            try:
                potential_base_designs_full=base_towel_dict[design[i]]
                for base_design in potential_base_designs_full:
                    N_bd=len(base_design)
                    try:
                        if design[i:i+N_bd]==base_design:
                            combination_counter[i+N_bd]+=combination_counter[i]
                    except:
                        pass
            except:
                pass
            i+=1
        possible_combinations+=combination_counter[-1]
print('1st:',possible_designs)
print('2nd:',possible_combinations)