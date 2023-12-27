import os
import numpy as np

os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
# print(inputStrList)

#just created a set with moves positions that were not allowed and checked that new steps were not to one of them
#for each step number, a set was created with visited positions that was only used for that specific step number, a new such set was created for the next one and so on
#just counted the number of possible moves for each step number and appended to list, first part could be solved by just looking in the list for a specific number of steps
#2nd part really sucked, 1st required to find a convoluted increasing differences (it could be seen by having enough iterations and plotting the difference for the listed with possible moves for each step number)
#the differences had a periodic shape but the magnitudes of the differences was increasing for each period. One could find this increase from period to period and use that to find a formula to express the number of possible steps
#-although this in and of itself was kind of annoying, it was not this that made this problem suck but that one had to run so many iterations to see and be able to verify the pattern (found an erroneous period length with the same procedure but an insufficient number of iterations, eventually used 700 so had to wait for quite some time..the actual solution of the problem did not change)

charGrid=[]
rocksOrVisited=set()
for ir,row in enumerate(inputStrList):
    rowChars=[]
    for ic,col in enumerate(row):
        if col=='#':
            rocksOrVisited.add((ir,ic))
        elif col=='S':
            startPosition=(ir,ic)
        rowChars.append(col)
    charGrid.append(rowChars)

maxRow=len(inputStrList)-1
maxCol=len(inputStrList[0])-1

stepMax=700 #did not find the full period when putting to 400, a bit of overkill here but the same procedure worked as for the example..
# stepMax=64 #sufficient for part 1
stepQueue=[(startPosition,startPosition)]
possibleStepsDict={0:startPosition}
NstepQueues=[]
for i in range(stepMax):
    print(i)
    nextStepQueue=[]
    newSteps=set()
    for rockstep,step in stepQueue:
        for dRow,dCol in [(1,0),(-1,0),(0,1),(0,-1)]:
            nextRow=step[0]+dRow
            nextCol=step[1]+dCol
            nextRockstepRow=rockstep[0]+dRow #necessary to have a dedicated rock position to check for valid moves when having the infinite grid (just adjusting positions when walking outside for the rocks to only look in the same grid)
            nextRockstepCol=rockstep[1]+dCol
            if nextRockstepRow<0:
                nextRockstepRow=maxRow
            elif nextRockstepRow>maxRow:
                nextRockstepRow=0
            if nextRockstepCol<0:
                nextRockstepCol=maxCol
            elif nextRockstepCol>maxCol:
                nextRockstepCol=0
            proposedPosition=(nextRow,nextCol)
            nextRockPosition=(nextRockstepRow,nextRockstepCol)
            if (nextRockPosition not in rocksOrVisited) and (proposedPosition not in newSteps):
                nextStepQueue.append((nextRockPosition,proposedPosition))
                newSteps.add(proposedPosition)
    stepQueue=nextStepQueue
    NstepQueues.append(len(stepQueue))

print('1st:',NstepQueues[63])

#part 2
referenceIndex=len(NstepQueues)-1
n=np.array(NstepQueues)
cycleLength=0
check1=0
check2=1
while check1!=check2: #check that the "characteristic differences" give rise to the same value when evaluating the last cycle and the second last cycle
    cycleLength+=1
    check1=(n[referenceIndex]-n[referenceIndex-cycleLength])-(n[referenceIndex-cycleLength]-n[referenceIndex-2*cycleLength])
    check2=(n[referenceIndex-cycleLength]-n[referenceIndex-2*cycleLength])-(n[referenceIndex-2*cycleLength]-n[referenceIndex-3*cycleLength])
# print(cycleLength)
nextStepCount=26501365
stepsToGo=nextStepCount-len(NstepQueues)
completecycles=stepsToGo//cycleLength
remainder=stepsToGo%cycleLength
# print(completecycles,remainder)
patternDifference=check1
referenceIndex2=referenceIndex-cycleLength+remainder
m=completecycles+1
nextEstimate=int(m)*int((n[referenceIndex2]-n[referenceIndex2-cycleLength]))+n[referenceIndex2]+int(patternDifference)*int(m*(m+1)/2)
print('2nd:',nextEstimate)

# #re-checked cycles and pattern difference for the reference position within the cycle
# check1_=(n[referenceIndex2]-n[referenceIndex2-cycleLength])-(n[referenceIndex2-cycleLength]-n[referenceIndex2-2*cycleLength])
# check2_=(n[referenceIndex2-cycleLength]-n[referenceIndex2-2*cycleLength])-(n[referenceIndex2-2*cycleLength]-n[referenceIndex2-3*cycleLength])
# print(check1_,check2_,check1,check2)
# #checked that previous values could be estimated
# m=-1
# estimate=m*(n[referenceIndex2]-n[referenceIndex2-cycleLength])+n[referenceIndex2]+patternDifference*m*(m+1)/2
# actual=n[referenceIndex2+cycleLength*m]
# print(estimate,actual)
# #checked that later values could be estimated, worked up to m=3 when having 700 iterations in the loop
# m=1
# referenceIndex3=referenceIndex2-cycleLength*m
# estimate=m*(n[referenceIndex3]-n[referenceIndex3-cycleLength])+n[referenceIndex3]+patternDifference*m*(m+1)/2
# actual=n[referenceIndex3+cycleLength*m]
# print(estimate,actual)

# #initial stuff to find pattern with example input
# import matplotlib.pyplot as plt
# plt.plot(np.diff(NstepQueues))
# plt.show()
# n=np.array(NstepQueues)
# cycleLength=11
# startIndex=len(n)-1
# diff_1=n[startIndex]-n[startIndex-cycleLength]
# diff_2=n[startIndex-cycleLength]-n[startIndex-cycleLength*2]
# diff_3=n[startIndex-cycleLength*2]-n[startIndex-cycleLength*3]
# print(diff_1-diff_2,diff_2-diff_3)

# referenceIndex=52
# e1=(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162
# n[referenceIndex+cycleLength]
# e2=e1-n[referenceIndex]+e1+162
# n[referenceIndex+cycleLength*2]
# e3=e2-e1+e2+162
# n[referenceIndex+cycleLength*3]
# e4=e3-e2+e3+162
# n[referenceIndex+cycleLength*4]

# print(e1,n[referenceIndex+cycleLength])
# print(e2,n[referenceIndex+cycleLength*2])
# print(e3,n[referenceIndex+cycleLength*3])
# print(e4,n[referenceIndex+cycleLength*4])

# referenceIndex=47
# (n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162,n[referenceIndex+cycleLength] #e1
# 2*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162+2*162 #e2
# 3*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162+2*162+3*162 #e3
# 4*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162+2*162+3*162+4*162 #e4

# m=1
# print(m*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*m*(m+1)/2)

# 2*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*2,n[referenceIndex+cycleLength*2] #e2,funkar ej

# 3*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*3*2,n[referenceIndex+cycleLength*3]
# 4*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*4*3*2,n[referenceIndex+cycleLength*4] #funkar ej
# 5*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*5*4*3*2,n[referenceIndex+cycleLength*5] #funkar ej

# e2-e1+e2+162
# 2*(2*(n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162*3)-((n[referenceIndex]-n[referenceIndex-cycleLength])+n[referenceIndex]+162)+162
