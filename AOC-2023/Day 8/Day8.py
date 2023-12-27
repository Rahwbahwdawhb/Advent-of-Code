import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
# fileName='example2.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
moveSequence,mapStr=inputStr.split('\n\n')
moveSequence=moveSequence.replace('R','1').replace('L','0')
moveSequence=[int(move) for move in list(moveSequence)]
mapList=mapStr.split('\n')

mapDict={}
startNodes_p2=[]
stopNodes_p2=[]
for entry in mapList:
    location,directions=entry.split('=')
    location=location.strip()
    directions=directions.replace(' ','').strip('()').split(',')    
    mapDict[location]=directions
    if location.endswith('A'):
        startNodes_p2.append(location)
    if location.endswith('Z'):
        stopNodes_p2.append(location)

moveCap=len(moveSequence)
#part 1
if 'AAA' in mapDict.keys(): #to be able to run example2.txt
    node='AAA'    
    moveCounter=0
    moveIndex=0
    while node!='ZZZ':
        move=moveSequence[moveIndex]
        node=mapDict[node][move]
        moveCounter+=1
        moveIndex+=1
        if moveIndex==moveCap:
            moveIndex=0
    print('1st:',moveCounter)

#part 2
def findPeriods(startNodes,mapDict,moveSequence,moveIndex=0):
    moveCounter=0
    periodcities=[]
    firstZs=[]
    for node in startNodes:
        visitedNodes=set()
        history=[]     
        moveCounter=0
        moveIndex=0
        move=moveSequence[moveIndex]
        while (node,move,moveIndex) not in visitedNodes or moveCounter==0:
            visitedNodes.add((node,move,moveIndex))
            history.append((node,move,moveIndex))
            move=moveSequence[moveIndex]
            node=mapDict[node][move]        
            moveCounter+=1
            moveIndex+=1
            if moveIndex==moveCap:
                moveIndex=0
        history.append((node,move,moveIndex))
        periodStartIndex=history.index(history[-1])
        periodcities.append(len(history)-1-periodStartIndex)
        zIndices=[i for i,(node,_,_) in enumerate(history) if node.endswith('Z')]
        # zIndices=[i for i in zIndices if i<=zIndices[0]+periodcities[-1]-1] #for input, only one index here  for all periods => simple repeating cycle, only need to account for one end-z occurrence per cycle!
        firstZs.append(zIndices[0])
    return periodcities,firstZs

periodcities,firstZs=findPeriods(startNodes_p2,mapDict,moveSequence)
#for puzzle input, the first Zs was the same as the periodicites (i.e no relative offsets at start), so just need to multiply the periods to find the required number of steps for them all to intersect (i.e. next occurrence of no relative offsets)
periodcities=np.array(periodcities)
#to avoid overflow during multiplication, setting relativePeriods_product=np.float64(1) before loop also produces wrong output
commonFactor=np.gcd.reduce(periodcities)
relativePeriods=periodcities/commonFactor
relativePeriods_product=1
for rp in relativePeriods:
    relativePeriods_product*=rp
nextCommonIntersection=relativePeriods_product*commonFactor
print('2nd:',int(nextCommonIntersection))

#extra
def runAround(startNodes,mapDict,moveSequence,moveIndex,movesToMake):
    moveIndex=0+moveIndex
    currentNodes=[]+startNodes
    for _ in range(movesToMake): 
        newNodes=[]       
        for node in currentNodes:
            move=moveSequence[moveIndex]
            node=mapDict[node][move]   
            moveIndex+=1
            if moveIndex==moveCap:
                moveIndex=0
            newNodes.append(node)
        currentNodes=[]+newNodes
    return currentNodes,moveIndex

currentNodes,moveIndex=runAround(startNodes_p2,mapDict,moveSequence,0,periodcities[3]+25)
periodcities2,firstZs2=findPeriods(currentNodes,mapDict,moveSequence,moveIndex=moveIndex)

periodOrder=np.argsort(periodcities2)
firstZs=np.array(firstZs2)
periodcities_ordered=periodcities[periodOrder]
firstZs_ordered=firstZs[periodOrder]
firstZs_ordered_shifted=firstZs_ordered-firstZs_ordered[0]

commonFactor=np.gcd.reduce(periodcities2)
(firstZs_ordered[0]-firstZs_ordered[1])/commonFactor

ns=[]
ls=[]
for po,fo in zip(periodcities_ordered,firstZs_ordered):
    n=0
    while True:
        n+=1
        l=(periodcities_ordered[0]*n+firstZs_ordered[0]-fo)/po
        if l%1==0:
            break
    ns.append(n)
    ls.append(l)

n=0
while True:
    n+=1
    l=(periodcities_ordered[0]*n+firstZs_ordered[0]-firstZs_ordered[1])/periodcities_ordered[1]
    if l%1==0:
        break
    1
print(periodcities_ordered[0]*n+firstZs_ordered[0])
print(periodcities_ordered[1]*l+firstZs_ordered[1])

ex=1 #extra common cycles
print(periodcities_ordered[0]*n+firstZs_ordered[0]+ex*(periodcities_ordered[0]*periodcities_ordered[1]))
print(periodcities_ordered[1]*l+firstZs_ordered[1]+ex*(periodcities_ordered[0]*periodcities_ordered[1]))

oneSolution_coeff_0=n
oneSolution_coeff_1=l
#måste hitta en lösning till ekvationen först innan kan skriva allmänna, har bara lösn. när högerledet=0
f0=oneSolution_coeff_0-1*periodcities2[1]/commonFactor
f1=oneSolution_coeff_1+1*periodcities2[0]/commonFactor
print(f0*periodcities2[0]+firstZs_ordered[0])
print(f1*periodcities2[1]+firstZs_ordered[1])


periodOrder=np.argsort(periodcities)
firstZs=np.array(firstZs)
offset=100
firstZs=firstZs-offset
periodcities_ordered=periodcities[periodOrder]
firstZs_ordered=firstZs[periodOrder]
firstZs_ordered_shifted=firstZs_ordered-firstZs_ordered[0]
m=0
lastIntersection=firstZs_ordered_shifted[m]-periodcities_ordered[m]+firstZs_ordered[0]

(firstZs_ordered)[m]-periodcities_ordered[m]

lastIntersection+relativePeriods_product*commonFactor
print(lastIntersection+nextCommonIntersection+offset)
m=0;print(firstZs_ordered_shifted[m]-periodcities_ordered[m])

period_ref=periodcities_ordered[0]
#pair-wise checks
period_refs=[periodcities_ordered[0]]
for i,(fzos,po) in enumerate(zip(firstZs_ordered_shifted[1:],periodcities_ordered[1:])):
    period_refs.append(np.gcd.reduce([period_refs[i],po]))
    print((fzos+period_ref)/po)
    1
1
