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
                for i2,key_row_2 in enumerate(keypad):
                    for i3,end_key in enumerate(key_row_2):
                        if end_key:
                            if start_key==end_key:
                                movement_dict[start_key+start_key]=[(0,'')]
                            else:
                                visited={(i0,i1)}
                                run=True
                                queue=[((i0,i1),start_key,'')]
                                paths=[]
                                while run:
                                    try:
                                        position,key,path_str=queue.pop(0)
                                    except: #if all adjacent valid keys have been visited
                                        break
                                    if key!=end_key:
                                        visited.add(position)
                                    if key==end_key:
                                        if len(paths)==0:
                                            path_length_to_match=len(path_str)
                                        if len(path_str)==path_length_to_match:
                                            # paths.append(path_str)
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

# complexity_sum=0
# for code_ in codes:
#     code='A'+code_
#     directional_input='A'
#     for i in range(4):
#         move=code[i]+code[i+1]
#         directional_input+=numeric_dict[move][0][1]+'A'
#         # print(numeric_dict[move][0]+'A',move,numeric_dict[move])
#         #02>^^AvvvA, 02^>^AvvvA, and 02^^>AvvvA, 029A
#     # print(directional_input in ['<A^A>^^AvvvA','<A^A^>^AvvvA','<A^A^^>AvvvA'])
#     directional_input_2='A'
#     for i in range(len(directional_input)-1):
#         move=directional_input[i]+directional_input[i+1]
#         directional_input_2+=directional_dict[move][0][1]+'A'
#     # print(len(directional_input_2)-1,len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A'))

#     # directional_input_2='Av<<A>>^A<A>AvA<^AA>A<vAAA>^A'
#     directional_input_3='A'
#     for i in range(len(directional_input_2)-1):
#         move=directional_input_2[i]+directional_input_2[i+1]
#         directional_input_3+=directional_dict[move][0][1]+'A'
#     # print(len(directional_input_3)-1,len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'))
#     complexity_sum+=(len(directional_input_3)-1)*int(code_.strip('0').strip('A'))
#     # print(code_,len(directional_input_3)-1,int(code_.strip('0').strip('A')))
# print(complexity_sum)
# #68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379







def get_paths(possible_paths,move_dict,move):
    new_paths=[]
    minimum_moves=move_dict[move][0][0]
    while possible_paths:
        change_sum,move_str,last_move=possible_paths.pop()
        for moves_,path_ in move_dict[move]:
            if moves_==minimum_moves:
                if path_=='':
                    change=0
                    last_move=''
                else:                    
                    if path_[0]==last_move:
                        change=0
                    else:
                        change=1
                    last_move=path_[-1]
                new_paths.append((change_sum+change,move_str+path_+'A',last_move))
    return new_paths
def get_paths_2(possible_paths,move_dict,move):
    new_paths=[]
    minimum_moves=move_dict[move][0][0]
    while possible_paths:
        move_str=possible_paths.pop()
        for moves_,path_ in move_dict[move]:
            if moves_==minimum_moves:
                new_paths.append(move_str+path_+'A')
    return new_paths

def get_dict_paths(possible_paths,move_dict,move):
    new_paths=[]
    minimum_moves=move_dict[move][0][0]
    while possible_paths:
        _,move_str=possible_paths.pop()
        for moves_,path_ in move_dict[move]:
            if moves_==minimum_moves:
                new_move_str=move_str+path_+'A'
                insort(new_paths,(len(new_move_str),new_move_str))
    return new_paths

# d2=dict()
# for move_0,paths in numeric_dict.items():
#     possible_paths=paths+[]
#     min_steps=paths[0][0]
#     while possible_paths:
#         steps,directional_input=possible_paths.pop()
#         if directional_input=='':
#                 d2[move_0]=[(0,'')]
#         else:
#             if steps==min_steps:
#                 for i in range(len(directional_input)-1):
#                     move=directional_input[i]+directional_input[i+1]
#                     new_paths=get_dict_paths(['A'],directional_dict,move)
#                 try:
#                     insort(d2[move_0],new_paths)
#                 except:
#                     d2[move_0]=new_paths
1
# d2=dict()
# for move_d2,paths in numeric_dict.items():
#     new_paths=get_dict_paths(paths+[],directional_dict,move)
#     try:
#         insort(d2[move],new_paths)
#     except:
#         d2[move]=new_paths

#nytt test

keys=['<','>','^','v','A']
combos=[]
combos_dict=dict()
for k1 in keys:
    for k2 in keys:
        for k3 in keys:
            combos.append(k1+k2+k3)
            paths=directional_dict[k1+k2]

move_dict=dict()
loop_dict=directional_dict
for _ in range(1):
    for move_0,path in loop_dict.items():
        for _,path_str in path:
            if path_str=='':
                move_dict[move_0]=[(0,'')]
            else:
                # directional_input='A'+path_str+'A'
                directional_input=''+path_str+'A'
                possible_paths_iter=['A']
                for i in range(len(directional_input)-1):
                    move=directional_input[i]+directional_input[i+1]
                    possible_paths_iter=get_paths_2(possible_paths_iter,directional_dict,move)
                if len(possible_paths_iter)>1:
                    Ns=[]
                    changes=[]
                    for ppi in possible_paths_iter:
                        last_ch=ppi[0]
                        change=0
                        for ch in ppi[1:]:
                            if ch!=last_ch:
                                change+=1
                            last_ch=ch
                        changes.append(change)
                        Ns.append(len(ppi))
                    print(Ns,changes)
                1
                move_dict[move_0]=[(len(x),x) for x in possible_paths_iter]
    loop_dict=move_dict

complexity_sum_=0
for code_ in codes:
    code='A'+code_
    possible_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1]
        possible_paths=get_paths_2(possible_paths,numeric_dict,move)

    all_possible_paths=[x for x in possible_paths]
    all_possible_paths_=[]
    while all_possible_paths:
        # _,directional_input,_=all_possible_paths.pop()
        # all_possible_paths_iter=[(0,'A','')]
        # for i in range(len(directional_input)-1):
        #     move=directional_input[i]+directional_input[i+1]
        #     all_possible_paths_iter=get_paths(all_possible_paths_iter,directional_dict,move)
        directional_input=all_possible_paths.pop()
        all_possible_paths_iter=['A']
        for i in range(len(directional_input)-1):
            move=directional_input[i]+directional_input[i+1]
            all_possible_paths_iter=get_paths_2(all_possible_paths_iter,move_dict,move)
        all_possible_paths_+=all_possible_paths_iter
    cs=[]
    L=[]
    for p in all_possible_paths_:
        # cs.append(len(p[1][1:])*int(code_.strip('0').strip('A')))
        cs.append(len(p[1:])*int(code_.strip('0').strip('A')))
        L.append(len(p))
    print(min(L),max(L))
    complexity_sum_+=min(cs)
print(complexity_sum_)


#om ej får enklare idé, jfr typ A0 då loopar som nedan som ger rätt svar å m dict här ovan
#kan även testa mappa ex 01 å hitta minimumväg för 1 iteration, se om är minimum efter 2, 3 iterationer...

####



complexity_sum=0
complexity_sum_2=0
complexity_sum_3=0
for code_ in codes:
    code='A'+code_




    possible_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1]
        possible_paths=get_paths_2(possible_paths,numeric_dict,move)




    # possible_paths=[(0,'A','')]
    # for i in range(4):
    #     move=code[i]+code[i+1]
    #     possible_paths=get_paths(possible_paths,numeric_dict,move)
    possible_paths=['A']
    for i in range(4):
        move=code[i]+code[i+1]
        possible_paths=get_paths_2(possible_paths,numeric_dict,move)

    # all_possible_paths=[x for x in possible_paths]
    # all_possible_paths_=[]
    # while all_possible_paths:
    #     directional_input=all_possible_paths.pop()
    #     all_possible_paths_iter=['A']
    #     for i in range(len(directional_input)-1):
    #         move=directional_input[i]+directional_input[i+1]
    #         all_possible_paths_iter=get_paths_2(all_possible_paths_iter,d2,move)
    #     all_possible_paths_+=all_possible_paths_iter
    # cs=[]
    # L=[]
    # for p in all_possible_paths_:
    #     # cs.append(len(p[1][1:])*int(code_.strip('0').strip('A')))
    #     cs.append(len(p[1:])*int(code_.strip('0').strip('A')))
    #     L.append(len(p))
    # print(min(L),max(L))
    # complexity_sum_2+=min(cs)


    #kolla om path som är kortast efter iteration 2 var kortast i iteration 1
    #hitta den som håller sig kortast, mappa om dess moves flera ggr?
    #kan räkna hur många olika av varje move/tecken har före och efter och öka dessa m iterationer?
    all_possible_paths=[x for x in possible_paths]
    for _ in range(2):
        all_possible_paths_=[]
        while all_possible_paths:
            # _,directional_input,_=all_possible_paths.pop()
            # all_possible_paths_iter=[(0,'A','')]
            # for i in range(len(directional_input)-1):
            #     move=directional_input[i]+directional_input[i+1]
            #     all_possible_paths_iter=get_paths(all_possible_paths_iter,directional_dict,move)
            directional_input=all_possible_paths.pop()
            all_possible_paths_iter=['A']
            for i in range(len(directional_input)-1):
                move=directional_input[i]+directional_input[i+1]
                all_possible_paths_iter=get_paths_2(all_possible_paths_iter,directional_dict,move)
            all_possible_paths_+=all_possible_paths_iter
        all_possible_paths=all_possible_paths_
    cs=[]
    L=[]
    for p in all_possible_paths:
        # cs.append(len(p[1][1:])*int(code_.strip('0').strip('A')))
        cs.append(len(p[1:])*int(code_.strip('0').strip('A')))
        L.append(len(p))
    print(min(L),max(L))
    complexity_sum_3+=min(cs)
    # print(complexity_sum_3)
    1
    # all_possible_paths_2=[]
    # while possible_paths:
    #     _,directional_input,_=possible_paths.pop()
    #     possible_paths_2_=[(0,'A','')]
    #     for i in range(len(directional_input)-1):
    #         move=directional_input[i]+directional_input[i+1]
    #         possible_paths_2_=get_paths(possible_paths_2_,directional_dict,move)
    #     all_possible_paths_2+=possible_paths_2_

    # all_possible_paths_3=[]
    # while all_possible_paths_2:
    #     _,directional_input,_=all_possible_paths_2.pop()
    #     possible_paths_3=[(0,'A','')]
    #     for i in range(len(directional_input)-1):
    #         move=directional_input[i]+directional_input[i+1]
    #         possible_paths_3=get_paths(possible_paths_3,directional_dict,move)
    #     all_possible_paths_3+=possible_paths_3
    # cs=[]
    # for p in all_possible_paths_3:
    #     cs.append(len(p[1][1:])*int(code_.strip('0').strip('A')))
    # complexity_sum_3+=min(cs)

print(complexity_sum_3)











#161472 too high
#162784