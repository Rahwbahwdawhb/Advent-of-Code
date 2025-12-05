import os
import bisect
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    id_ranges_str,available_id_str=f.read().strip().split('\n\n')
lowers=[]
uppers=[]
ranges=[]
for id_ranges_str in id_ranges_str.split('\n'):
    lower,upper=id_ranges_str.split('-')
    lower=int(lower)
    upper=int(upper)
    lowers.append(lower)
    uppers.append(upper)
    bisect.insort(ranges,(lower,upper))

fresh_count_1=0
for id_str in available_id_str.split('\n'):
    id=int(id_str)
    fresh=False
    for lower,upper in zip(lowers,uppers):
        if id>=lower and id<=upper:
            fresh=True
            break
    if fresh:
        fresh_count_1+=1
print("1st:",fresh_count_1)

fresh_count_2=0
while ranges:
    lower,upper=ranges.pop(0)
    proceed=False
    while not proceed:
        for lower_,upper_ in ranges:
            if lower_<=upper:
                upper=max(upper,upper_)
                del ranges[0]
                break
            else:
                proceed=True
                fresh_count_2+=upper-lower+1
                break
        if not ranges:
            fresh_count_2+=upper-lower+1
            proceed=True
print("2nd:",fresh_count_2)