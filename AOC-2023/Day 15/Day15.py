import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split(',')
#part 1
totalSum=0
for step in inputStrList:
    stepList=list(step)
    currentValue=0
    for ch in stepList:
        currentValue+=ord(ch)
        currentValue*=17
        currentValue%=256
    totalSum+=currentValue
print(totalSum)

#part 2
def hashMap(strIn):
    strList=list(strIn)
    currentValue=0
    for ch in strList:
        currentValue+=ord(ch)
        currentValue*=17
        currentValue%=256
    return currentValue

boxes_labels=[[] for _ in range(256)]
boxes_focalLengths=[[] for _ in range(256)]
for step in inputStrList:
    if '-' in step:
        label=step[:-1]
        removeLens=True
    else:
        label,focalLength=step.split('=')
        removeLens=False
    boxIndex=hashMap(label)
    if removeLens:
        try:
            indexToRemove=boxes_labels[boxIndex].index(label)
            del boxes_labels[boxIndex][indexToRemove]
            del boxes_focalLengths[boxIndex][indexToRemove]
        except:
            pass
    else:
        try:
            indexToRemove=boxes_labels[boxIndex].index(label)
            del boxes_labels[boxIndex][indexToRemove]
            del boxes_focalLengths[boxIndex][indexToRemove]
            boxes_labels[boxIndex].insert(indexToRemove,label)
            boxes_focalLengths[boxIndex].insert(indexToRemove,int(focalLength))
        except:
            boxes_labels[boxIndex].append(label)
            boxes_focalLengths[boxIndex].append(int(focalLength))
totalFocusingPower=0
for i,(boxLabels,boxFocalLengths) in enumerate(zip(boxes_labels,boxes_focalLengths)):
    for ii,(label,focalLength) in enumerate(zip(boxLabels,boxFocalLengths)):
        totalFocusingPower+=(i+1)*(1+ii)*focalLength
print(totalFocusingPower)
