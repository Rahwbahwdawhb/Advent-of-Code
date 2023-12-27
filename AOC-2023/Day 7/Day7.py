import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
strengthOrder=['A','K','Q','J','T','9','8','7','6','5','4','3','2']
strengthStrs=['a','b','c','d','e','f','g','h','i','j','k','l','m']
strengthOrder=strengthOrder[::-1]
handList=[]
for _ in range(7):
    handList.append([])
for row in inputStrList:
    hand,bid=row.split(' ')
    uniqueCards=list(set(hand))
    occurences=[]
    for i,card in enumerate(uniqueCards):
        occurences.append(hand.count(card))
    if len(occurences)==5:
        handList[0].append([hand,bid])
    elif len(occurences)==4:
        handList[1].append([hand,bid])
    elif len(occurences)==3:
        if max(occurences)==2:
            handList[2].append([hand,bid])
        else:
            handList[3].append([hand,bid])
    elif len(occurences)==2:
        if max(occurences)==3:
            handList[4].append([hand,bid])
        else:
            handList[5].append([hand,bid])
    else:
        handList[6].append([hand,bid])

def sorter(listIn,strengthOrder,strengthStrs):
    handNumbers=[]
    for hand,_ in listIn:
        handNumberStr=''
        for card in hand:
            # handNumberStr+=str(strengthOrder.index(card))
            handNumberStr+=strengthStrs[strengthOrder.index(card)]
        # handNumbers.append(int(handNumberStr))
        handNumbers.append(handNumberStr)
    listInSorted=[x for _, x in sorted(zip(handNumbers,listIn), key=lambda pair: pair[0])]
    return listInSorted
            
    # listIn.sort(key=lambda x:x[0])
    # return listIn
# twos=twos[::-1]
# print(twos)
# sorter(twos)
# print(twos)
counter=0
totalPoints=0
for hands in handList:
    if hands!=[]:
        handsSorted=sorter(hands,strengthOrder,strengthStrs)
        pointList=[int(bid)*(i+1+counter) for i,(_,bid) in enumerate(handsSorted)]
        counter+=len(pointList)
        totalPoints+=sum(pointList)
print(totalPoints)

#part 2
strengthOrder=['A','K','Q','T','9','8','7','6','5','4','3','2','J']
strengthStrs=['a','b','c','d','e','f','g','h','i','j','k','l','m']
strengthOrder=strengthOrder[::-1]
handList=[]
for _ in range(7):
    handList.append([])
for row in inputStrList:
    hand,bid=row.split(' ')
    if hand.find('J')==-1:
        uniqueCards=list(set(hand))
        occurences=[]
        for i,card in enumerate(uniqueCards):
            occurences.append(hand.count(card))
        if len(occurences)==5:
            handList[0].append([hand,bid])
        elif len(occurences)==4:
            handList[1].append([hand,bid])
        elif len(occurences)==3:
            if max(occurences)==2:
                handList[2].append([hand,bid])
            else:
                handList[3].append([hand,bid])
        elif len(occurences)==2:
            if max(occurences)==3:
                handList[4].append([hand,bid])
            else:
                handList[5].append([hand,bid])
        else:
            handList[6].append([hand,bid])
    else:
        jHands=[hand]
        jIndices=[i for i,card in enumerate(hand) if card=='J']
        for i in jIndices:
            jHandsNew=[]
            for jHand in jHands:
                for card in strengthOrder:
                    jHandsNew.append(jHand[:i]+card+jHand[i+1:])
            jHands=[]+jHandsNew
        # jHandsBids=[[jHand,None] for jHand in jHands]
        jHandList=[]
        for _ in range(7):
            jHandList.append([])
        for jHand in jHands:
            uniqueCards=list(set(jHand))
            occurences=[]
            for i,card in enumerate(uniqueCards):
                occurences.append(jHand.count(card))
            if len(occurences)==5:
                jHandList[0].append([jHand,bid])
            elif len(occurences)==4:
                jHandList[1].append([jHand,bid])
            elif len(occurences)==3:
                if max(occurences)==2:
                    jHandList[2].append([jHand,bid])
                else:
                    jHandList[3].append([jHand,bid])
            elif len(occurences)==2:
                if max(occurences)==3:
                    jHandList[4].append([jHand,bid])
                else:
                    jHandList[5].append([jHand,bid])
            else:
                jHandList[6].append([jHand,bid])
        counter=0
        jHandsBest=[]
        for jHands in jHandList:
            if jHands!=[]:
                jHandsSorted=sorter(jHands,strengthOrder,strengthStrs)
                jHandsBest.append(jHandsSorted[-1])
                # pointList=[int(bid)*(i+1+counter) for i,(_,bid) in enumerate(jHandsSorted)]
                # counter+=len(pointList)
                # totalPoints+=sum(pointList)
        jHandBest=jHandsBest[-1][0]
        uniqueCards=list(set(jHandBest))
        occurences=[]
        for i,card in enumerate(uniqueCards):
            occurences.append(jHandBest.count(card))
        if len(occurences)==5:
            handList[0].append([hand,bid])
        elif len(occurences)==4:
            handList[1].append([hand,bid])
        elif len(occurences)==3:
            if max(occurences)==2:
                handList[2].append([hand,bid])
            else:
                handList[3].append([hand,bid])
        elif len(occurences)==2:
            if max(occurences)==3:
                handList[4].append([hand,bid])
            else:
                handList[5].append([hand,bid])
        else:
            handList[6].append([hand,bid])

counter=0
totalPoints=0
for hands in handList:
    if hands!=[]:
        handsSorted=sorter(hands,strengthOrder,strengthStrs)
        pointList=[int(bid)*(i+1+counter) for i,(_,bid) in enumerate(handsSorted)]
        counter+=len(pointList)
        totalPoints+=sum(pointList)
print(totalPoints)