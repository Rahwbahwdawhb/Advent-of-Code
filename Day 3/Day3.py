from preload import input
import string

# input='vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw'
# print(input)

#1st problem
lowCase=string.ascii_lowercase
uppCase=string.ascii_uppercase
valDict={}
for iter in range(52):
    if iter<26:
        key=lowCase[iter]
    else:
        key=uppCase[iter-26]
    valDict[key]=iter+1
# print(valDict)

inpList=input.split('\n')
prioSumTot=0
for row in inpList:
    rowLenHalf=round(len(row)/2)
    row1=row[0:rowLenHalf]
    row2=row[rowLenHalf:]
    # print(row1+','+row2)
    commonItems=[]
    prioSum=0
    for iter in range(rowLenHalf):
        if row1[iter] in row2 and row1[iter] not in commonItems:
            commonItems.append(row1[iter])
            prioSum+=valDict[row1[iter]]
    # print(commonItems,prioSum)
    prioSumTot+=prioSum
print('1st: ',prioSumTot)

#2nd problem
# print(len(inpList),inpList[0],':',inpList[-1])
rowIter=0
currentGroup=[]
badgePrioSum=0
while rowIter<len(inpList):
    if len(currentGroup)<3:
        currentGroup.append(inpList[rowIter])
    if len(currentGroup)==3:
        uItems=[]
        nU=[]
        for elf in currentGroup:
            uIelf=list(set(elf))
            uItems.append(uIelf)
            nU.append(len(uIelf))
        uItemsSort=[x for _,x in sorted(zip(nU,uItems),reverse=True)]
        
        # for i in range(3):
        #     print(len(uItems[i]),',',len(uItemsSort[i]))

        for item in uItemsSort[0]:
            if item in uItemsSort[1] and item in uItemsSort[2]:
                badgePrio=valDict[item]
                break
        badgePrioSum+=badgePrio
        currentGroup=[]
    rowIter+=1
print('2nd: ',badgePrioSum)