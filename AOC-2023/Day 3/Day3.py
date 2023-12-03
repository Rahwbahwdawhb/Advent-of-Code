import os
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read()
inputList=inputStr.split('\n')
inputList=['.'+rowStr+'.' for rowStr in inputList]
N1=len(inputList[0])
N2=len(inputList)
inputList=['.'*N1]+inputList+['.'*N1]
rowRange=[i for i in range(1,N2+1)]

partNumberSum=0
gearDict={}
for i,row in zip(rowRange,inputList[1:N2+1]):
    # print(i,row)
    haveNumber=False
    numberIndices=[]
    partNumberStr=''
    for ii,ch in enumerate(row[1:N2+1]):
        if ch.isdigit():
            numberIndices.append(ii+1)
            partNumberStr+=ch
        else:
            if numberIndices!=[]:
                partNumber=int(partNumberStr)
                #part 1
                upperRowToCheck=inputList[i-1][numberIndices[0]-1:numberIndices[-1]+2]
                lowerRowToCheck=inputList[i+1][numberIndices[0]-1:numberIndices[-1]+2]
                leftToCheck=inputList[i][numberIndices[0]-1]
                rightToCheck=inputList[i][numberIndices[-1]+1]
                checkStr=upperRowToCheck+lowerRowToCheck+leftToCheck+rightToCheck
                #part 2
                upperIndices=[(i-1,iii) for iii in range(numberIndices[0]-1,numberIndices[-1]+2)]
                lowerIndices=[(i+1,iii) for iii in range(numberIndices[0]-1,numberIndices[-1]+2)]
                leftIndex=[(i,numberIndices[0]-1)]
                rightIndex=[(i,numberIndices[-1]+1)]
                checkStr_indices=upperIndices+lowerIndices+leftIndex+rightIndex
                for ch_indices,ch_ in zip(checkStr_indices,checkStr): #part 2
                    if ch_=='*':
                        if ch_indices not in gearDict:
                            gearDict[ch_indices]=[partNumber]
                        else:
                            gearDict[ch_indices].append(partNumber)
                
                if len(checkStr.replace('.',''))!=0: #part 1
                    partNumberSum+=partNumber
                numberIndices=[]
                partNumberStr=''
gearRatioSum=0
for key in gearDict.keys():
    if len(gearDict[key])==2:
        gearRatioSum+=gearDict[key][0]*gearDict[key][1]
print('1st:',partNumberSum)
print('2nd:',gearRatioSum)
                