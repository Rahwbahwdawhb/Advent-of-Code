import os
from bisect import insort
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    dataList=f.read().strip().split('\n')

plant_dict=dict()
for ir,row in enumerate(dataList):
    for ic,ch in enumerate(row):
        try:
            plant_dict[ch].add((ir,ic))
        except:
            plant_dict[ch]=set()
            plant_dict[ch].add((ir,ic))

def insort_to_dict_key(_dict,key,value):
    try:
        insort(_dict[key],value)
    except:
        _dict[key]=[value]
max_row=ir
max_col=ic
plant_region_dict=dict()
for plant in plant_dict.keys():
    plant_positions=plant_dict[plant]    
    while plant_positions:
        region_set=set()
        position_queue=[plant_positions.pop()]
        region_fences=0
        region_sides_dict={'top':{},'bot':{},'left':{},'right':{}}
        while position_queue:
            position=position_queue.pop(0)
            region_set.add(position)
            position_fences=4 #assume plant in position has no adjacent similar plants => has 4 fences, subtract 1 for every it does have
            direction_bools=[]
            for it,d in enumerate([(1,0),(-1,0),(0,1),(0,-1)]):
                adjacent_position=(position[0]+d[0],position[1]+d[1])                
                if 0<=adjacent_position[0]<=max_row and 0<=adjacent_position[1]<=max_col:                    
                    if adjacent_position in plant_positions:
                        position_queue.append(adjacent_position)
                        region_set.add(adjacent_position)
                        plant_positions.remove(adjacent_position)
                        position_fences-=1
                        direction_bool=True
                    elif adjacent_position in region_set:
                        position_fences-=1
                        direction_bool=True
                    else:
                        direction_bool=False
                else:
                    direction_bool=False
                #adding row/column indices to sorted lists in a dictonary with column/row indices as keys for each possible fence orientation
                #the lists for each column/row will then be looped over and checked for if consecutive indices differ by more than 1 (i.e. a there are gaps between fences=>+1 side)
                if not direction_bool:
                    if it==0:
                        insort_to_dict_key(region_sides_dict['bot'],position[0],position[1])
                    if it==1:
                        insort_to_dict_key(region_sides_dict['top'],position[0],position[1])
                    if it==2:
                        insort_to_dict_key(region_sides_dict['right'],position[1],position[0])
                    if it==3:
                        insort_to_dict_key(region_sides_dict['left'],position[1],position[0])            
            region_fences+=position_fences
        #part 2
        sides=0
        for orientation in region_sides_dict.keys():
            for row_col in region_sides_dict[orientation]:
                col_row=region_sides_dict[orientation][row_col]
                io=col_row.pop(0)
                sides+=1
                for i in col_row:
                    if i-io!=1:
                        sides+=1
                    io=i
        try:
            plant_region_dict[plant].append([region_set,region_fences,sides])
        except:
            plant_region_dict[plant]=[[region_set,region_fences,sides]]

fence_price=0
fence_price_2=0
for plant in plant_region_dict.keys():
    for region in plant_region_dict[plant]:
        region_area=len(region[0])
        fence_price+=region_area*region[1] #part 1
        fence_price_2+=region_area*region[2] #part 2
print('1st:',fence_price)
print('2nd:',fence_price_2)