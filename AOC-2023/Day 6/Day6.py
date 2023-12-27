import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
raceLists_p1=[]
raceList_p2=[]
for row in inputStrList:
    rowList=row.split(':')[1].strip().split(' ')
    rowNumberList=[]
    for entry in rowList:
        if len(entry)!=0:
            rowNumberList.append(int(entry))
    raceLists_p1.append(rowNumberList)
    raceList_p2.append(int(row.split(':')[1].replace(' ','')))
times=raceLists_p1[0]
distanceRecords=raceLists_p1[1]
#part 1
totalConfigurations=1
for t,d in zip(times,distanceRecords):
    speeds=np.linspace(1,t,t)
    timesLeft=t-speeds
    distances=speeds*timesLeft
    winningConfigurations=sum(distances>d)
    totalConfigurations*=winningConfigurations
print('1st:',totalConfigurations)
#part 2
speeds=np.linspace(1,raceList_p2[0],raceList_p2[0])
timesLeft=raceList_p2[0]-speeds
distances=speeds*timesLeft
winningConfigurations=sum(distances>raceList_p2[1])
print('2nd:',winningConfigurations)