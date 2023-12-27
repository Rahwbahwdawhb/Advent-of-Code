import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n\n')
# print(inputStrList)
mapList=[]
seedsStrList=inputStrList[0].split(':')[1].strip().split(' ')
seeds=[int(seed) for seed in seedsStrList]
for mapStr in inputStrList[1:]:
    mapInfo=mapStr.split('\n')[1:]
    destination=[]
    source=[]
    for i,row in enumerate(mapInfo):
        i1,i2,step=row.split(' ')
        i1,i2,step=int(i1),int(i2),int(step)
        # if (i+1)%2!=0:
        destination.append([i1,i1+step-1])
        source.append([i2,i2+step-1])
        # else:
        #     destination.append([i2,i2+step-1])
        #     source.append([i1,i1+step-1])
    mapList.append([source,destination])
# for m in mapList:
#     print(m[0],m[1])
def seedConversion(seeds,mapList):
    locations=[]
    for seed in seeds:
        currentNumber=seed
        for m in mapList:
            source_m=m[0]
            destination_m=m[1]
            for i,numberRange in enumerate(source_m):
                if currentNumber>=numberRange[0] and currentNumber<=numberRange[1]:
                    stepInRange=currentNumber-numberRange[0]
                    currentNumber=destination_m[i][0]+stepInRange
                    break
        locations.append(currentNumber)
    return locations
locations=seedConversion(seeds,mapList)
print('1st',min(locations))

# # print(seeds)
# startSeedNumbers=seeds[::2]
# seedRanges=seeds[1::2]
# lowestLocations=[]
# for startSeedNumber,seedRange in zip(startSeedNumbers,seedRanges):
#     seeds=np.linspace(startSeedNumber,startSeedNumber+seedRange-1,seedRange).astype(int)
#     locations=seedConversion(seeds,mapList)
#     lowestLocations.append(min(locations))
# print(min(lowestLocations))

# print('')
# print(mapList[-1])

def locationConversion(location,mapList):
    currentNumber=location
    for m in mapList[::-1]:
        source_m=m[0]
        destination_m=m[1]
        for i,numberRange in enumerate(destination_m):
            if currentNumber>=numberRange[0] and currentNumber<=numberRange[1]:
                stepInRange=currentNumber-numberRange[0]
                currentNumber=source_m[i][0]+stepInRange
                break
    seed=currentNumber
    return seed

startSeedNumbers=seeds[::2]
seedRanges=seeds[1::2]
seedRangeList=[]
for startSeedNumber,seedRange in zip(startSeedNumbers,seedRanges):
    seedRangeList.append([startSeedNumber,startSeedNumber+seedRange-1])
minLows=[]
for source_m,destination_m in mapList:
    lows=[]
    for low_source,_ in source_m:
        lows.append(low_source)
    for low_destination,_ in destination_m:
        lows.append(low_destination)
    minLows.append(min(lows))
# brute force solution got the 2nd answer with after waiting quite some time
# guessLocation=min(minLows)-1
# # guessLocation=-1
# foundIt=False
# while not foundIt:
#     guessLocation+=1
#     seedNumber=locationConversion(guessLocation,mapList)
#     for seedNumberLower,seedNumberUpper in seedRangeList:
#         if seedNumber>=seedNumberLower and seedNumber<=seedNumberUpper:
#             foundIt=True
#             break
# guessLocation=min(minLows)-1
locationRange=[min(minLows),min(locations[::2])]
guessLocation=locationRange[-1]
lowerBound=locationRange[0]
lowerBound_old=lowerBound+1
currentLowestLocation_old=guessLocation+1
foundIt_1=False
while locationRange[0]!=locationRange[-1]:
    seedNumber=locationConversion(guessLocation,mapList) 
    foundIt_0=foundIt_1
    foundIt_1=False
    for seedNumberLower,seedNumberUpper in seedRangeList:
        if seedNumber>=seedNumberLower and seedNumber<=seedNumberUpper:
            currentLowestLocation=guessLocation
            lowestLocationSeedNumber=seedNumber            
            foundIt_1=True
            break
    print(guessLocation,seedNumber,foundIt_0,foundIt_1)
    # print(len(locationRange))
    if foundIt_0 and not foundIt_1:
        if currentLowestLocation==currentLowestLocation_old:
            currentLowestLocation-=1
        currentLowestLocation_old=currentLowestLocation
        locationRange=[lowerBound,currentLowestLocation]
        guessLocation_0=sum(locationRange)//2
        guessLocation=guessLocation_0
    elif not foundIt_0 and not foundIt_1 and guessLocation==lowerBound:
        lowerBound=guessLocation_0
        if lowerBound==lowerBound_old:
            lowerBound+=1
            guessLocation_0=lowerBound
        lowerBound_old=lowerBound
        locationRange=[lowerBound,currentLowestLocation]
        guessLocation=sum(locationRange)//2
        # if len(locationRange)==len(locationRange_old):
        #     locationRange=locationRange[1:]
        # locationRange_old=locationRange
        # guessLocation=locationRange[len(locationRange)//2]
    else:
        guessLocation-=1

# print(seedNumber,guessLocation)
print('2nd',locationRange[0])