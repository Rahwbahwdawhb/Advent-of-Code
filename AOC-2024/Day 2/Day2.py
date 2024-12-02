import os
import numpy as np
os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'
with open(file) as f:
    dataList=f.read().strip().split('\n')

def checkLevels(levels):
    dlevels=np.diff(levels)
    adlevels=np.abs(dlevels)
    sign_check=np.abs(np.diff(np.sign(dlevels)))    
    if np.max(sign_check)==0 and np.max(adlevels)<=3 and np.min(adlevels)>0:
        safe=True
    else:
        safe=False
    return safe

safeCounter=0
safeCounter2=0
for row in dataList:
    levels=[int(x) for x in row.split()]
    if checkLevels(levels):
        safeCounter+=1
    else:
        for i,_ in enumerate(levels):
            try_levels=levels[:i]+levels[i+1:]
            if checkLevels(try_levels):
                safeCounter2+=1
                break

print('1st:',safeCounter)
print('2nd:',safeCounter2+safeCounter)
