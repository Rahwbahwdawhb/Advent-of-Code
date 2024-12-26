import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
# file='example2.txt'
with open(file) as f:
    initial_secret_numbers=f.read().strip().split('\n')

def new_secret_number(secret_number):
    step_1=((secret_number*64)^secret_number)%16777216
    step_2=((step_1//32)^step_1)%16777216
    step_3=((step_2*2048)^step_2)%16777216
    return step_3

secret_number_sum=0
secret_iterations=2000
max_iteration_check=secret_iterations
change_dict=dict()
change_dict_2=dict()
for sn in initial_secret_numbers:
    sn=int(sn)
    sn_0=sn
    change_buffer=[]
    last_price=int(str(sn)[-1])
    previous_change_strs=set()
    all_str=''
    for i in range(secret_iterations):
        sn=new_secret_number(sn) #part 1
        #part 2
        price=int(str(sn)[-1])
        change_buffer.append(price-last_price)
        last_price=price        
        if i>2:
            change_str=str(change_buffer)
            if change_str not in previous_change_strs:
                previous_change_strs.add(change_str)             
                try:
                    change_dict[change_str]+=price
                    change_dict_2[change_str].append([sn_0,price])
                except:
                    change_dict[change_str]=price
                    change_dict_2[change_str]=[[sn_0,price]]
            del change_buffer[0]
    secret_number_sum+=sn
print('1st:',secret_number_sum)

max_bananas=0
for change_str in change_dict.keys():
    if change_dict[change_str]>max_bananas:
        max_bananas=change_dict[change_str]
        best_change_str=change_str
print('2nd:',max_bananas)