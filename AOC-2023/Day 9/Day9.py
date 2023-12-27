import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
extrapolatedValues_end=[] #for part 1
extrapolatedValues_start=[] #for part 2
for reading in inputStrList:
    valueHistory=[int(ch) for ch in reading.split(' ')]
    checkSum=1
    diff_str=np.array(valueHistory)
    toSum_end=[]
    toSum_start=[]
    while checkSum!=0:
        toSum_end.append(diff_str[-1])
        toSum_start.append(diff_str[0])
        diff_str=np.diff(diff_str)
        checkSum=sum(diff_str)
    extrapolatedValues_end.append(sum(toSum_end))
    
    toSum_start=toSum_start[::-1]
    startSum=0
    for value in toSum_start:
        startSum=value-startSum
    extrapolatedValues_start.append(startSum)
print('1st:',sum(extrapolatedValues_end))
print('2nd:',sum(extrapolatedValues_start))