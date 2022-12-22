from preload import input
# print(input)

# input=open('ex.txt').read()

#1st problem
inpList=input.strip().split('Monkey')

class monkey:
    def __init__(self,number,operation,testDIV,throwMonkeyTrue,throwMonkeyFalse,monkeyList):
        self.number=number
        self.items=[]
        self.operation=operation
        self.testDIV=testDIV
        self.throwMonkeyTrue=throwMonkeyTrue
        self.throwMonkeyFalse=throwMonkeyFalse
        self.monkeyList=monkeyList
        self.itemsChecked=0
    def getItem(self,item):
        self.items.append(item)
    def monkeyTurn(self):
        while len(self.items)!=0:
            old=self.items.pop(0)
            new=eval(self.operation)
            new=int(new/3)
            self.itemsChecked+=1
            if new%self.testDIV==0:
                self.monkeyList[self.throwMonkeyTrue].getItem(new)
            else:
                self.monkeyList[self.throwMonkeyFalse].getItem(new)
    
monkeyList=[]
iter=0
for inp in inpList[1:]:
    monkeyInfo=inp.strip().split('\n')
    monkeyNumber=int(monkeyInfo[0][0])
    items_str=monkeyInfo[1].split(':')[1].split(',')
    operation=monkeyInfo[2][monkeyInfo[2].find('= ')+2:]
    testDIV=int(monkeyInfo[3][monkeyInfo[3].find('by ')+3:])
    throwMonkeyTrue=int(monkeyInfo[4][monkeyInfo[4].find('key ')+4:])
    throwMonkeyFalse=int(monkeyInfo[5][monkeyInfo[5].find('key ')+4:])

    monkeyList.append(monkey(monkeyNumber,operation,testDIV,throwMonkeyTrue,throwMonkeyFalse,monkeyList))
    for item in items_str:
        monkeyList[iter].getItem(int(item.strip()))
    iter+=1
    # print(inp.strip())
    # print('*****')

Nrounds=20
for _ in range(Nrounds):
    for m in monkeyList:
        m.monkeyTurn()
inspectList=[]
for m in monkeyList:
    inspectList.append(m.itemsChecked)
inspectList.sort(reverse=True)
print('1st: ',inspectList[0]*inspectList[1])

#2nd problem

class monkey2:
    def __init__(self,number,operation,testDIV,throwMonkeyTrue,throwMonkeyFalse,monkeyList):
        self.number=number
        self.items=[]
        self.operation=operation
        self.testDIV=testDIV
        self.throwMonkeyTrue=throwMonkeyTrue
        self.throwMonkeyFalse=throwMonkeyFalse
        self.monkeyList=monkeyList
        self.itemsChecked=0
        self.totTestDiv=1
    def getItem(self,item):
        self.items.append(item)
    def getTotTestDiv(self):
        for m in self.monkeyList:
            self.totTestDiv*=m.testDIV
    def monkeyTurn(self):
        while len(self.items)!=0:
            old=self.items.pop(0)
            new=eval(self.operation)
            if new>self.totTestDiv:
                new%=self.totTestDiv
            self.itemsChecked+=1
            if new%self.testDIV==0:
                self.monkeyList[self.throwMonkeyTrue].getItem(new)
            else:
                self.monkeyList[self.throwMonkeyFalse].getItem(new)
    
monkeyList=[]
iter=0
for inp in inpList[1:]:
    monkeyInfo=inp.strip().split('\n')
    monkeyNumber=int(monkeyInfo[0][0])
    items_str=monkeyInfo[1].split(':')[1].split(',')
    operation=monkeyInfo[2][monkeyInfo[2].find('= ')+2:]
    testDIV=int(monkeyInfo[3][monkeyInfo[3].find('by ')+3:])
    throwMonkeyTrue=int(monkeyInfo[4][monkeyInfo[4].find('key ')+4:])
    throwMonkeyFalse=int(monkeyInfo[5][monkeyInfo[5].find('key ')+4:])

    monkeyList.append(monkey2(monkeyNumber,operation,testDIV,throwMonkeyTrue,throwMonkeyFalse,monkeyList))
    for item in items_str:
        monkeyList[iter].getItem(int(item.strip()))
    iter+=1
for m in monkeyList:
    m.getTotTestDiv()

Nrounds=10000
for _ in range(Nrounds):
    for m in monkeyList:
        m.monkeyTurn()
inspectList=[]
for m in monkeyList:
    inspectList.append(m.itemsChecked)
inspectList.sort(reverse=True)
print('2nd: ',inspectList[0]*inspectList[1])

# import numpy as np
# Nrounds=100
# ci2=[]
# for _ in range(Nrounds):
#     ci=[]
#     for m in monkeyList:
#         m.monkeyTurn()
#         ci.append(m.itemsChecked)
#     ci2.append(ci)
# ci2=np.array(ci2)
# print(ci)
# ci.sort(reverse=True)
# print(ci[0]*ci[1])
# print(np.diff(ci2,axis=0))
#     inQueue=[]
#     for m in monkeyList:
#         inQueue.append(len(m.items))
#     print(inQueue)

