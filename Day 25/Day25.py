from preload import input

# input=open('ex.txt').read()
# print(input)

inpList=input.strip().split('\n')

#1st problem
snafuDecimalDict={'2':2,'1':1,'0':0,'-':-1,'=':-2}
decimalSum=0
for inp in inpList:
    decimalSum+=sum([5**i*snafuDecimalDict[ch] for i,ch in enumerate(inp[::-1])])
print(decimalSum)

diff=-decimalSum
trial=[]
iter=0
while diff<0:
    trial.append(2*5**iter)
    diff=sum(trial)-decimalSum
    iter+=1
N=len(trial)
coeffs=[2 for _ in range(N)]
base=[5**(N-1-i) for i in range(N)]

import numpy as np
coeffs=np.array(coeffs)
base=np.array(base)
# print(sum(trial))
# print(np.sum(coeffs*base))

stop=False
checkIndex=0
while not stop:
    print(diff)
    coeffs[checkIndex]-=1
    diff=sum(coeffs*base)-decimalSum
    if diff<0:
        coeffs[checkIndex]+=1
        checkIndex+=1
    elif diff==0:
        stop=True    
decimalSnafuDict={2:'2',1:'1',0:'0',-1:'-',-2:'='}
snafuSum=''
for coeff in coeffs:
    snafuSum+=decimalSnafuDict[coeff]
print('1st: ',snafuSum)

#2nd problem

