import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n\n')

def verticalCheck(patternGrid,refelctionIndices):
    patternSums=[]
    comparisonSums=[]
    smudgeIndex=[]
    for refelctionIndex0 in refelctionIndices:
        upperPart=patternGrid[:refelctionIndex0+1,:]
        lowerPart=patternGrid[refelctionIndex0+1:,:]
        us0=upperPart.shape[0]
        ls0=lowerPart.shape[0]
        upperPart=upperPart[::-1,:]
        if us0>ls0:        
            upperPart=upperPart[:ls0]
        elif us0<ls0:
            lowerPart=lowerPart[:us0,:]
        patternSums.append(100*(refelctionIndex0+1))
        diffMatrix=np.abs(upperPart-lowerPart)        
        comparisonSum=np.sum(diffMatrix)
        comparisonSums.append(comparisonSum)
        if comparisonSum==1:
            upperProduct=diffMatrix*upperPart
            if np.sum(upperProduct)==1:
                smudgeIndex=np.argwhere(upperProduct==1)[0]
                smudgeIndex[0]=refelctionIndex0-smudgeIndex[0]
            else:
                lowerProduct=diffMatrix*lowerPart
                smudgeIndex=np.argwhere(lowerProduct==1)[0]
                smudgeIndex[0]+=refelctionIndex0+1
    return patternSums,comparisonSums,smudgeIndex
def scorePattern(patternGrid):   
    patternSum=0    
    try:
        rowSums=np.sum(np.abs(np.diff(patternGrid,axis=0)),axis=1)
        refelctionIndices=np.argwhere(rowSums==0).flatten()
        patternSums,comparisonSums,_=verticalCheck(patternGrid,refelctionIndices)
        reflectionMatch=np.argwhere(np.array(comparisonSums)==0).flatten()
        if len(reflectionMatch)!=0:
            patternSum+=patternSums[reflectionMatch[0]]
    except:
        pass
    colSums=np.sum(np.abs(np.diff(patternGrid,axis=1)),axis=0)
    refelctionIndices=np.argwhere(colSums==0).flatten()
    patternSums,comparisonSums,_=verticalCheck(patternGrid.T,refelctionIndices)
    reflectionMatch=np.argwhere(np.array(comparisonSums)==0).flatten()
    if len(reflectionMatch)!=0:
        patternSum+=patternSums[reflectionMatch[0]]/100
    
    return patternSum
patternSum=0
for pattern in inputStrList:
    patternList=pattern.split('\n')
    patternGrid=np.zeros((len(patternList),len(patternList[0])))
    for ir,row in enumerate(patternList):
        for ic,col in enumerate(row):
            if col=='#':
                patternGrid[ir,ic]=1
    patternSum+=scorePattern(patternGrid)
print('1st:',patternSum)

#part2
patternSum2=0
patternSum2_=0
for pattern in inputStrList:
    patternList=pattern.split('\n')
    patternGrid=np.zeros((len(patternList),len(patternList[0])))
    for ir,row in enumerate(patternList):
        for ic,col in enumerate(row):
            if col=='#':
                patternGrid[ir,ic]=1
    patternSums_vertical,comparisonSums_vertical,smudge_vertical=verticalCheck(patternGrid,[i for i in range(patternGrid.shape[0])])
    patternSums_horizontal,comparisonSums_horizontal,smudge_horizontal=verticalCheck(patternGrid.T,[i for i in range(patternGrid.shape[1])])
    if len(smudge_vertical)>0:
        if patternGrid[smudge_vertical[0],smudge_vertical[1]]==1:
            patternGrid[smudge_vertical[0],smudge_vertical[1]]=0
        else:
            patternGrid[smudge_vertical[0],smudge_vertical[1]]=1
    if len(smudge_horizontal)>0:
        smudge_horizontal[0],smudge_horizontal[1]=smudge_horizontal[1],smudge_horizontal[0]
        if patternGrid[smudge_horizontal[0],smudge_horizontal[1]]==1:
            patternGrid[smudge_horizontal[0],smudge_horizontal[1]]=0
        else:
            patternGrid[smudge_horizontal[0],smudge_horizontal[1]]=1
    patternSums_vertical2,comparisonSums_vertical2,smudge_vertical2=verticalCheck(patternGrid,[i for i in range(patternGrid.shape[0])])
    patternSums_horizontal2,comparisonSums_horizontal2,smudge_horizontal2=verticalCheck(patternGrid.T,[i for i in range(patternGrid.shape[1])])
    csv=np.argwhere(np.array(comparisonSums_vertical)==0).flatten()
    csv2=np.argwhere(np.array(comparisonSums_vertical2)==0).flatten()
    for c in csv2:
        if c not in csv:
            patternSum2+=patternSums_vertical2[c]
    csh=np.argwhere(np.array(comparisonSums_horizontal)==0).flatten()
    csh2=np.argwhere(np.array(comparisonSums_horizontal2)==0).flatten()
    for c in csh2:
        if c not in csh:
            patternSum2+=patternSums_horizontal2[c]/100
    patternSum2_+=scorePattern(patternGrid)
print('2nd:',patternSum2)