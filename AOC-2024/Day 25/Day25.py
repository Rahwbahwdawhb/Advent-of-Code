import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    key_lock_list=f.read().strip().split('\n\n')

def add_to_dict(_dict,heights_tuple):
    try:
        _dict[heights_tuple]+=1
    except:
        _dict[heights_tuple]=1

keys_dict=dict()
locks_dict=dict()
for key_lock in key_lock_list:
    heights=[]
    for ir,row in enumerate(key_lock.split('\n')):
        if ir==0:
            for ch in row:
                if ch=='#':
                    heights.append(1)
                else:
                    heights.append(0)
        else:
            for ic,ch in enumerate(row):
                if ch=='#':
                    heights[ic]+=1
    heights_tuple=tuple([h-1 for h in heights])
    if key_lock[0]=='#':        
        add_to_dict(locks_dict,heights_tuple)
    else:
        add_to_dict(keys_dict,heights_tuple)

if len(keys_dict.keys())>len(locks_dict.keys()):
    dict_1=keys_dict
    dict_2=locks_dict
else:
    dict_2=keys_dict
    dict_1=locks_dict

fit_sum=0
for heights,number in dict_1.items():
    for heights_,number_ in dict_2.items():
        fit_bool=True
        for h1,h2 in zip(heights,heights_):
            if h1+h2>5:
                fit_bool=False
                break
        if fit_bool:
            fit_sum+=1
print(fit_sum)