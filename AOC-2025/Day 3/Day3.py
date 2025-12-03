import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    battery_banks=f.read().strip().split('\n')

def iterate_2(battery_bank):
    ref_2=""
    for i,_ in enumerate(battery_bank):
        temp=battery_bank[:i]+battery_bank[i+1:]
        if ref_2<temp:
            ref_2=temp
    return ref_2

joltage_1_sum=0
joltage_2_sum=0
N=len(battery_banks[0])-1
for battery_bank in battery_banks:
    max_1=[0,0]
    max_2=[0,0]
    for i,battery in enumerate(battery_bank):
        battery=int(battery)
        if battery>max_1[0]:
            if i<N:
                max_2[0]=0
                max_2[1]=0
            else:
                max_2[0]=max_1[0]
                max_2[1]=max_1[1]
            max_1[0]=battery
            max_1[1]=i
        elif battery>max_2[0]:
            max_2[0]=battery
            max_2[1]=i
    if max_1[1]>max_2[1]:
        joltage_1=10*max_2[0]+max_1[0]
    else:
        joltage_1=10*max_1[0]+max_2[0]
    joltage_1_sum+=joltage_1
    cut=battery_bank
    while len(cut)>12:
        cut=iterate_2(cut)
    joltage_2_sum+=int(cut)
print("1st:",joltage_1_sum)
print("2nd:",joltage_2_sum)