import os
import bisect
import numpy as np
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    indicator_diagrams=f.read().strip().split('\n')

"""
Part 1 is super slow, idea for a strategy that might speed it up:
1. Represent the button states as a "system of equations", where the system matrix has the presses for each button as row elements
   The sums of the button presses on each row should add up to:
    an even number when the light should be off (an even number of toggles turns the light off)
    an odd number when the light should be on
2. Use a while loop to increment the sum total of all the presses
   For each iteration, create all permutations of the button coefficients that sum up to the current sum total
   For each permutation, check if the even/odd conditions for all rows are satisfied
    The first time this is satisfied the sum total will be the lowest number of presses
"""


total_minimum_toggles=0
# solve_1=False
solve_1=True
count=0
for indicator_diagram in indicator_diagrams:
    count+=1
    print(count)
    lights_,rest=indicator_diagram.split(']')
    goal_lights=[]
    lights=[]
    for light in lights_[1:]:
        lights.append(False)
        if light=='#':
            goal_lights.append(True)
        else:
            goal_lights.append(False)
    buttons_,joltage_requirements=rest.split('{')
    joltage_requirements=np.array([int(jr) for jr in joltage_requirements[:-1].split(',')])
    N=len(lights)
    buttons=[{int(b_) for b_ in b.strip('()').split(',')} for b in buttons_.strip().split(' ')] #used for part 1

    if solve_1: #to be optimized, super slow but works
        to_toggle_set=set()
        for i,(gl,l) in enumerate(zip(goal_lights,lights)):
            if gl!=l:
                to_toggle_set.add(i)
        from_prior_iteration=[(None,None,to_toggle_set,lights)]

        found_toggle_sequence=False
        it=0
        while not found_toggle_sequence:
            button_order=[]
            it+=1
            for fpi in from_prior_iteration:
                _,previous_button,to_toggle_set,lights=fpi
                for b in buttons:
                    if b==previous_button:
                        continue
                    non_desired_toggles=b-to_toggle_set
                    initial_desired_toggles_left=to_toggle_set-b
                    left_to_toggle=initial_desired_toggles_left.union(non_desired_toggles)
                    if len(left_to_toggle)==0:
                        found_toggle_sequence=True
                        break
                    temp=lights+[]
                    for b_ in b:
                        temp[b_]=not temp[b_]
                    bisect.insort(button_order,(len(non_desired_toggles),b,left_to_toggle,temp))
                if found_toggle_sequence:
                    break
            from_prior_iteration=button_order
        # print(it)
        total_minimum_toggles+=it
print("1st:",total_minimum_toggles)
# print("2nd:",total_minimum_presses)