import os
import numpy as np
os.chdir(os.path.dirname(__file__))
# fileName='input.txt'
fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
# print(inputStrList[0])
# print(inputStrList[-1])

def sequenceLooper(sequence):
    emptyInSequenceIndices=set([seqIn for seqIn,ch in enumerate(sequence) if ch=='.'])
    springInSequenceIndices=set([seqIn for seqIn,ch in enumerate(sequence) if ch=='#'])
    relativeSpringIndices=[]
    tempIndex=0
    for count in counts.split(','):
        relativeSpringIndices.append(np.array([i+tempIndex for i in range(int(count))]).astype(int))
        tempIndex=relativeSpringIndices[-1][-1]+2
    maxIndex=len(sequence)-1
    Nchunks=len(relativeSpringIndices)
    maxSteps=maxIndex-relativeSpringIndices[-1][-1]
    possibleSteps=np.array([maxSteps+0 for _ in range(Nchunks)]).astype(int)
    indexInSequences=np.zeros((len(sequence))).astype(int)
    indexShift=np.zeros((len(relativeSpringIndices))).astype(int)    
    validSequences=0
    # print('')
    # print(sequence)
    minIndexToModify=Nchunks-2
    approvedSequences=[]
    firstLastChars=[]
    while True:
        for iter,_ in enumerate(range(possibleSteps[-1]+1)):
            allAddIndices=np.array([])
            for iter2,(inSh,relInds) in enumerate(zip(indexShift,relativeSpringIndices)):
                addIndices=relInds+inSh+iter*(iter2==Nchunks-1)
                allAddIndices=np.concatenate((allAddIndices,addIndices))
            newSequence=''
            for i in range(maxIndex+1):
                if i in allAddIndices:
                    newSequence+='#'
                else:
                    newSequence+='.'
            # print(newSequence,'X',sequence)
            # if newSequence=='#.##.##...#.#...####' or newSequence=='#.##.##..#..#...####':
            #     1
            if allAddIndices[-1]<=maxIndex and len(emptyInSequenceIndices.intersection(allAddIndices))==0 and springInSequenceIndices.issubset(allAddIndices):
                np.add.at(indexInSequences,addIndices,1)
                validSequences+=1
                approvedSequences.append(newSequence)
                firstLastChars.append(newSequence[0]+newSequence[-1])
        1
        if sum(possibleSteps)==0:
            break
        indexToModify=Nchunks-2
        while True:            
            if possibleSteps[indexToModify]>0:
                possibleSteps[indexToModify]-=1
                possibleSteps[indexToModify+1:]=possibleSteps[indexToModify]+0
                indexShift[indexToModify:]=indexShift[indexToModify:]+1
                if indexShift[-1]+relativeSpringIndices[-1][-1]>maxIndex:
                    indexShift[indexToModify:]=indexShift[indexToModify]
                break
            else:
                if indexToModify==0:
                    break
                else:
                    indexToModify-=1
        # if indexToModify==0:
        #     minIndexToModify=indexToModify+0
        if indexToModify<minIndexToModify or indexToModify==0:
            minIndexToModify=indexToModify+0
            indexShift[indexToModify:]=indexShift[indexToModify]
    return firstLastChars,approvedSequences,validSequences
def firstLastCharsToGeneratorDict(firstLastChars):    
    for firstLastChars in allfirstLastChars:
        hh_sum=0
        pp_sum=0
        hp_sum=0
        ph_sum=0
        for charPair in firstLastChars:
            if charPair=='##':
                hh_sum+=1
            elif charPair=='..':
                pp_sum+=1
            elif charPair=='#.':
                hp_sum+=1
            elif charPair=='.#':
                ph_sum+=1
        generationDict=dict()
        generationDict['##']=[['x',hh_sum]]
        generationDict['#.']=[['..',pp_sum],['.#',ph_sum]]
        generationDict['..']=[['..',pp_sum],['.#',ph_sum]]
        generationDict['.#']=[['x',ph_sum]]
    return generationDict

def firstLastCharsToCountDict(firstLastChars):    
    for firstLastChars in allfirstLastChars:
        hh_sum=0
        pp_sum=0
        hp_sum=0
        ph_sum=0
        for charPair in firstLastChars:
            if charPair=='##':
                hh_sum+=1
            elif charPair=='..':
                pp_sum+=1
            elif charPair=='#.':
                hp_sum+=1
            elif charPair=='.#':
                ph_sum+=1
        countDict=dict()
        countDict['##']=hh_sum
        countDict['#.']=hp_sum
        countDict['..']=pp_sum
        countDict['.#']=ph_sum
    return countDict

def removeNoncombinableSequences(firstLastChars,invalidFirstLasts):
    firstLastChars_=[]
    for flc in firstLastChars:
        if flc not in invalidFirstLasts:
            firstLastChars_.append(flc)
    return firstLastChars_

def validateCountDicts(countDict1,countDict2,validPairs):
    newCountDict=dict()
    charPairs=['##','.#','#.','..']
    for charPair in  charPairs:
        newCountDict[charPair]=0
    for flc1,flc2 in validPairs:
        newCountDict[flc2]=countDict1[flc1]*countDict2[flc2]        
    return newCountDict
def addCountDicts(countDict1,countDict2):
    newCountDict=dict()
    for charPair in ['##','.#','#.','..']:
        newCountDict[charPair]=countDict1[charPair]+countDict2[charPair]
    return newCountDict

sequenceConfigurationsList=[]
validSequencesList=[]
Ntot=len(inputStrList)
allfirstLastChars=[]
validPairs=[['..','..'],['..','#.'],['..','.#'],['..','##'],
                        ['#.','..'],['#.','#.'],['#.','.#'],['#.','##'],
                        ['.#','..'],['.#','.#'],['##','..'],['##','.#']]
for bigIter,row in enumerate(inputStrList):    
    sequence,counts=row.split(' ')
    # sequence+='?'
    firstLastChars_0,approvedSequences_0,validSequences=sequenceLooper(sequence)
    firstLastChars_1,approvedSequences_1,_=sequenceLooper(sequence+'?')    
    firstLastChars_2,approvedSequences_2,_=sequenceLooper('?'+sequence)
    firstLastChars_3,approvedSequences_3,_=sequenceLooper('?'+sequence+'?')

    reducedFirstLastChars_10=[]
    for flc1,aps in zip(firstLastChars_1,approvedSequences_1):
        if aps not in approvedSequences_0:
            reducedFirstLastChars_10.append(flc1)

    countDict_0=firstLastCharsToCountDict(firstLastChars_0)
    countDict_1=firstLastCharsToCountDict(firstLastChars_1)
    countDict_2=firstLastCharsToCountDict(firstLastChars_2)

    ### finns 16 kombinationer av (sequence+?)(sequence).../(sequence)(?+sequence)...
    ### hitta sätt att generera kombinationerna, då kan använda countDicts utan ambiguities
    #7593738901198871808, too high
    reducedCountDict_1=firstLastCharsToCountDict(reducedCountDict_1) #problem i loop

    nextCountDict_1=validateCountDicts(countDict_0,countDict_2,validPairs)
    nextCountDict_2=validateCountDicts(reducedCountDict_1,countDict_0,validPairs)
    nextCountDict=addCountDicts(nextCountDict_1,nextCountDict_2)
    for _ in range(2):
        nextCountDict=validateCountDicts(nextCountDict,countDict_2,validPairs)

    firstLastChars_p2b,_=sequenceLooper('?'+sequence+'?')
    firstLastChars_p2c,_=sequenceLooper('?'+sequence)
    firstLastChars_p2a=removeNoncombinableSequences(firstLastChars_p2a,['##','.#'])
    firstLastChars_p2b=removeNoncombinableSequences(firstLastChars_p2b,['##','#.','.#'])
    firstLastChars_p2c=removeNoncombinableSequences(firstLastChars_p2c,['##','#.'])
    concactedSequences=len(firstLastChars_p2a)*len(firstLastChars_p2b)*len(firstLastChars_p2b)*len(firstLastChars_p2b)*len(firstLastChars_p2c)
    1
    

    # emptyInSequenceIndices=set([seqIn for seqIn,ch in enumerate(sequence) if ch=='.'])
    # springInSequenceIndices=set([seqIn for seqIn,ch in enumerate(sequence) if ch=='#'])
    # relativeSpringIndices=[]
    # tempIndex=0
    # for count in counts.split(','):
    #     relativeSpringIndices.append(np.array([i+tempIndex for i in range(int(count))]).astype(int))
    #     tempIndex=relativeSpringIndices[-1][-1]+2
    # maxIndex=len(sequence)-1
    # Nchunks=len(relativeSpringIndices)
    # maxSteps=maxIndex-relativeSpringIndices[-1][-1]
    # possibleSteps=np.array([maxSteps+0 for _ in range(Nchunks)]).astype(int)
    # indexInSequences=np.zeros((len(sequence))).astype(int)
    # indexShift=np.zeros((len(relativeSpringIndices))).astype(int)    
    # validSequences=0
    # # print('')
    # # print(sequence)
    # minIndexToModify=Nchunks-2
    # approvedSequences=[]
    # firstLastChars=[]
    # while True:
    #     for iter,_ in enumerate(range(possibleSteps[-1]+1)):
    #         allAddIndices=np.array([])
    #         for iter2,(inSh,relInds) in enumerate(zip(indexShift,relativeSpringIndices)):
    #             addIndices=relInds+inSh+iter*(iter2==Nchunks-1)
    #             allAddIndices=np.concatenate((allAddIndices,addIndices))
    #         newSequence=''
    #         for i in range(maxIndex+1):
    #             if i in allAddIndices:
    #                 newSequence+='#'
    #             else:
    #                 newSequence+='.'
    #         # print(newSequence,'X',sequence)
    #         # if newSequence=='#.##.##...#.#...####' or newSequence=='#.##.##..#..#...####':
    #         #     1
    #         if allAddIndices[-1]<=maxIndex and len(emptyInSequenceIndices.intersection(allAddIndices))==0 and springInSequenceIndices.issubset(allAddIndices):
    #             np.add.at(indexInSequences,addIndices,1)
    #             validSequences+=1
    #             approvedSequences.append(newSequence)
    #             firstLastChars.append(newSequence[0]+newSequence[-1])
    #     1
    #     if sum(possibleSteps)==0:
    #         break
    #     indexToModify=Nchunks-2
    #     while True:            
    #         if possibleSteps[indexToModify]>0:
    #             possibleSteps[indexToModify]-=1
    #             possibleSteps[indexToModify+1:]=possibleSteps[indexToModify]+0
    #             indexShift[indexToModify:]=indexShift[indexToModify:]+1
    #             if indexShift[-1]+relativeSpringIndices[-1][-1]>maxIndex:
    #                 indexShift[indexToModify:]=indexShift[indexToModify]
    #             break
    #         else:
    #             if indexToModify==0:
    #                 break
    #             else:
    #                 indexToModify-=1
    #     # if indexToModify==0:
    #     #     minIndexToModify=indexToModify+0
    #     if indexToModify<minIndexToModify or indexToModify==0:
    #         minIndexToModify=indexToModify+0
    #         indexShift[indexToModify:]=indexShift[indexToModify]
    allfirstLastChars.append(firstLastChars)
    validSequencesList.append(validSequences)
    # print(bigIter,Ntot)
print(validSequencesList)
print(sum(validSequencesList))

charPairs=['##','.#','#.','..']
generatorDictList=[]
for firstLastChars in allfirstLastChars:
    hh_sum=0
    pp_sum=0
    hp_sum=0
    ph_sum=0
    for charPair in firstLastChars:
        if charPair=='##':
            hh_sum+=1
        elif charPair=='..':
            pp_sum+=1
        elif charPair=='#.':
            hp_sum+=1
        elif charPair=='.#':
            ph_sum+=1
    generationDict=dict()
    generationDict['##']=[['..',pp_sum],['.#',ph_sum]]
    generationDict['#.']=[['..',pp_sum],['.#',ph_sum],['#.',hp_sum],['##',hh_sum]]
    generationDict['..']=[['..',pp_sum],['.#',ph_sum],['#.',hp_sum],['##',hh_sum]]
    generationDict['.#']=[['..',pp_sum],['.#',ph_sum]]
    generatorDictList.append(generationDict)

    sumDict=dict()
    sumDict['##']=0+hh_sum
    sumDict['#.']=0+hp_sum
    sumDict['.#']=0+ph_sum
    sumDict['..']=0+pp_sum
    for _ in range(4):
        currentCombos=[]
        for charPair in charPairs:
            currentCombos.append(sumDict[charPair]+0)
            sumDict[charPair]=0
        for charPair,currentCombo in zip(charPairs,currentCombos):
            for generated in generationDict[charPair]:
                charPair_generated=generated[0]
                amount_generated=generated[1]
                sumDict[charPair_generated]+=amount_generated*currentCombo
        totalSum=0
        for charPair in charPairs:
            totalSum+=sumDict[charPair]
        print(totalSum)
    1


hh_sum=0
pp_sum=0
hp_sum=0
ph_sum=0
for charPair in firstLastChars:
    if charPair=='##':
        hh_sum+=1
    elif charPair=='..':
        pp_sum+=1
    elif charPair=='#.':
        hp_sum+=1
    elif charPair=='.#':
        ph_sum+=1
endPtot=pp_sum+hp_sum
endHtot=hh_sum+ph_sum
print(hh_sum+ph_sum+hp_sum+pp_sum)

generationDict=dict()
generationDict['##']=[['..',pp_sum],['.#',ph_sum]]
generationDict['#.']=[['..',pp_sum],['.#',ph_sum],['#.',hp_sum],['##',hh_sum]]
generationDict['..']=[['..',pp_sum],['.#',ph_sum],['#.',hp_sum],['##',hh_sum]]
generationDict['.#']=[['..',pp_sum],['.#',ph_sum]]
sumDict=dict()
sumDict['##']=0+hh_sum
sumDict['#.']=0+hp_sum
sumDict['.#']=0+ph_sum
sumDict['..']=0+pp_sum
charPairs=['##','.#','#.','..']

for _ in range(4):
    currentCombos=[]
    for charPair in charPairs:
        currentCombos.append(sumDict[charPair]+0)
        sumDict[charPair]=0
    for charPair,currentCombo in zip(charPairs,currentCombos):
        for generated in generationDict[charPair]:
            charPair_generated=generated[0]
            amount_generated=generated[1]
            sumDict[charPair_generated]+=amount_generated*currentCombo
    totalSum=0
    for charPair in charPairs:
        totalSum+=sumDict[charPair]
    print(totalSum)

1

# #behöver fixa sista indexskiftningen
#     countList=[int(count) for count in counts.split(',')]
#     sequenceList=[sequencePart for sequencePart in sequence.split('.') if sequencePart!='']
#     if len(countList)==len(sequenceList):
#         configurationsList=[]
#         for c,s in zip(countList,sequenceList):
#             if len(s)==c:
#                 configurationsList.append(1)
#             else:
#                 c=7
#                 s='????##?##???'
#                 sStripped=s.strip('?')                
#                 if sStripped=='':
#                     configurationsList.append(len(s)-c+1)
#                 else:
#                     existingIndices=[is_ for is_,s_ in enumerate(s) if s_=='#']
#                     existingRange=[min(existingIndices),max(existingIndices)]
#                     subSequenceLength=existingRange[1]-existingRange[0]+1
#                     leftToFind=c-subSequenceLength
#                     if leftToFind==0:
#                         configurations_=1
#                     else:
#                         lowerIndex=max([existingRange[0]-leftToFind,0])
#                         upperIndex=min([existingRange[1]+leftToFind,len(s)-1])
#                         lowerIndices=[lowerIndex+ni for ni in range(existingRange[0]-lowerIndex)]
#                         upperIndices=[upperIndex+ni for ni in range(upperIndex-existingRange[1])]
#                         configurations_=0
#                         stepIntoLower=0
#                         while True:
#                             upperPart=subSequenceLength+len(upperIndices)
#                             if upperPart==c:
#                                 configurations_+=1
#                                 del upperIndices[-1]
#                             else:
#                                 stepIntoLower+=1
#                                 if len(lowerIndices)-stepIntoLower>=0:                    
#                                     if upperPart+stepIntoLower==c:
#                                         configurations_+=1
#                                     else:
#                                         break
#                                 else:
#                                     break
#                     configurationsList.append(configurations_)
#                     # print(configurations_)
#                     1
#     #         1
#     #     1
#     # configurations_=0
#     # if upperIndex-existingRange[1]==leftToFind:
#     #     configurations_+=1
#     # if existingRange[0]-lowerIndex==leftToFind:
#     #     configurations_+=1
#     # print([lowerIndex+ni for ni in range(existingRange[0]-lowerIndex)])
#     # print([upperIndex+ni for ni in range(upperIndex-existingRange[1])])
                    
#                     s_mod=''
#                     for is_,s_ in enumerate(s):
#                         if existingRange[0]<=is_<=existingRange[1]:
#                             s_mod+='#'
#                         else:
#                             s_mod+=s_

                    

#                     leftToFind=c-len(sStripped)
#                     existing=len([s_ for s_ in sStripped if s_=='#'])
                    
#                     leftToFind=c-existing
#                     1
#                 configurationsList.append(c-len([s_ for s_ in s if s_=='#']))
#         sequenceConfigurations=1
#         for configurations in configurationsList:
#             sequenceConfigurations*=configurations
#         sequenceConfigurationsList.append(sequenceConfigurations)
#         print(row,sequenceConfigurations)
#     else:
        
#         1
    # print(countList)
    # print(sequenceList)
    # print('')

# a='.###.##.#...'.split('.')
# b=[ap for ap in a if ap!='']
# print(b)
# print('?###????????'.split('.'))