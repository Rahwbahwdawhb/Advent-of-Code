import os
from time import time
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    id_ranges=f.read().strip().split(',')
t0=time()
invalid_id_sum_1=0
invalid_id_sum_2=0
for id_range in id_ranges:
    low_,high_=id_range.split('-')
    low,high=int(low_),int(high_)
    i=low
    while i<=high:
        i_str=str(i)
        #part 1
        _len=len(i_str)
        valid=True
        even_length=False
        if _len%2==0:
            even_length=True
            half=_len//2
            if i_str[:half]==i_str[half:]:
                invalid_id_sum_1+=i
                valid=False
        if valid:
            #part 2
            ch_0=i_str[0]
            test_step=1
            potential_steps=[]
            try:
                while test_step<_len:
                    it=test_step
                    failed=False
                    while it<_len:
                        if i_str[it]!=ch_0:
                            failed=True
                            break
                        it+=test_step
                    if not failed:
                        potential_steps.append(test_step)
                    while test_step<_len:
                        test_step+=1
                        if _len%test_step==0:
                            break
            except:
                pass
            for step in potential_steps:
                failed=False
                for index,ch_ref in enumerate(i_str[1:]):
                    try:
                        it=index+1+step
                        while it<_len:
                            if i_str[it]!=ch_ref:
                                failed=True
                                break
                            it+=step
                    except:
                        failed=True
                if not failed:
                    invalid_id_sum_2+=i
                    break
        i+=1
invalid_id_sum_2+=invalid_id_sum_1
print("1st:",invalid_id_sum_1)
print("2nd:",invalid_id_sum_2)
print(time()-t0)