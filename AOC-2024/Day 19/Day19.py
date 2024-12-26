import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
file='example.txt'
with open(file) as f:
    available_towel_str,designs_str=f.read().strip().split('\n\n')

# # available_towel_set={at.strip() for at in available_towel_str.split(',')}
# available_towels=[at.strip() for at in available_towel_str.split(',')]
# available_towels.sort(key=len,reverse=True)

# available_towel_set=set()
# available_towel_lens=set()
# for at in available_towel_str.split(','):
#     at=at.strip()
#     available_towel_set.add(at)
#     available_towel_lens.add(len(at))
# available_towel_lens=list(available_towel_lens)
# available_towel_lens.sort()

# possible_designs=0
# for design in designs_str.split('\n'):
#     towel_check_0=design.strip()
#     # towel_check=towel_check_0
#     # for towel in available_towels:
#     #     towel_check=towel_check.replace(towel,'')
#     #     if len(towel_check)==0:
#     #         possible_designs+=1
#     #         break
    
#     1
#     # print(towel_check_0,possible_designs)
#     # 1
# print(possible_designs)

towel_design_dict=dict()
towel_design_set_0=set()
for at in available_towel_str.split(','):
    towel_design_dict[at.strip()]=True
    towel_design_set_0.add(at.strip())

possible_combinations_dict=dict()
def recursive_check(towel_str):
    try:
        return towel_design_dict[towel_str]
    except:
        N=len(towel_str)
        if N==1 or N==0:
            return False
        elif N==2:
            check1=recursive_check(towel_str[0])
            check2=recursive_check(towel_str[1])
            # if check1 and check2:
            #     possible_combinations_dict[towel_str]={f"{towel_str[0]},{towel_str[1]}"}
            return check1 and check2
        possible_design_bool=False
        # possible_combinations=set()
        possible_combinations=0
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
                possible_combinations+=1
        #         if towel_str_1 in towel_design_set_0 and towel_str_2 in towel_design_set_0:
        #             possible_combinations.add(f"{towel_str_1},{towel_str_2}")
        #         elif (towel_str_1 in towel_design_set_0 and not towel_str_2 in towel_design_set_0):
        #             for combination in possible_combinations_dict[towel_str_2]:
        #                 possible_combinations.add(f"{towel_str_1},{combination}")
        #         elif (towel_str_1 not in towel_design_set_0 and towel_str_2 in towel_design_set_0):
        #             for combination in possible_combinations_dict[towel_str_1]:
        #                 possible_combinations.add(f"{combination},{towel_str_2}")
        #         else:
        #             for combination_2 in possible_combinations_dict[towel_str_2]:
        #                 for combination_1 in possible_combinations_dict[towel_str_1]:
        #                     possible_combinations.add(f"{combination_1},{combination_2}")
        #         # break
        possible_combinations_dict[towel_str]=possible_combinations
        return possible_design_bool

possible_designs=0
combinations=0
N_loop=len(designs_str.split('\n'))
for iter,design in enumerate(designs_str.split('\n')):
    # print(f"{iter}/{N_loop}")
    possible_designs+=recursive_check(design)
    combinations+=possible_combinations_dict[design]
    print(possible_combinations_dict[design])
    1
print(possible_designs)
print(combinations)

#varje ok-kombination utgörs av ett par av strängar => bildar 2-grenande träd
#då använder nod högt upp i träd kommer ha använt alla kombinationer i noder nedanför
#om trackar vilka nedre noder som används bör kunna undvika att de räknas flera ggr
#måste köra från aktuellt index och vidare / från 0 till aktuellt index, för noder
#ska kunna användas på olika ställen i sträng -men ej flera ggr i följd på samma ställe
#vill ha m siffra för kombinationer av underliggande noder då lägger till ny
#noden själv + samtliga underliggande ska deaktiveras/ej räknas om använder samma nod igen