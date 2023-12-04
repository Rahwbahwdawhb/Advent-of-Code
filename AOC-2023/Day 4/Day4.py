import os
import numpy as np
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')
#1st problem
totalPoints=0
cardDict={}
for i,row in enumerate(inputStrList):
    wNumbers,numbers=row.split(':')[1].split('|')
    wList=wNumbers.strip().split(' ')
    wList=[w for w in wList if w.isdigit()]
    nList=numbers.strip().split(' ')
    nList=[n for n in nList if n.isdigit()]
    points=0
    luckyNumbers=[]
    for w in wList:
        if w in nList:
            if points==0:
                points=1
            else:
                points*=2
            del nList[nList.index(w)]
            luckyNumbers.append(w)
    totalPoints+=points
    rowsToGet=[i+ii+1 for ii in range(len(luckyNumbers))]
    cardDict[i]=rowsToGet
print('1st:',totalPoints)
#2nd problem
def appendCard(cardIn,cardDict,cardCollection):
    cardList=cardDict[cardIn]
    cardCollection.append(cardIn)
    for card in cardList:
         appendCard(card,cardDict,cardCollection)
def appendCard_memo(cardIn,cardDict,cardReturnDict):
    if cardIn in cardReturnDict:
        return cardReturnDict[cardIn]
    else:
        cardList=cardDict[cardIn]
        cardCollection=[]+cardList
        for card in cardList:
            cardCollection+=appendCard_memo(card,cardDict,cardReturnDict)
        # cardCollection=cardCollection
        cardReturnDict[cardIn]=cardCollection
        return cardCollection
totalCards=0
cardReturnDict={}
for card in cardDict.keys():
    # loopCollection_0=[]
    # appendCard(card,cardDict,loopCollection_0)
    loopCollection=[card]+appendCard_memo(card,cardDict,cardReturnDict)
    totalCards+=len(loopCollection)
print('2nd:',totalCards)
