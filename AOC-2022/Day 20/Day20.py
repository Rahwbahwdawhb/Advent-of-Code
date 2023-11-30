from preload import input
# input='1\n2\n-3\n3\n-2\n0\n4'
# print(input)
inpList=input.strip().split('\n')
# print(inpList[0:3],inpList[-3:])

#1st problem

# nDict=dict()
# for i,inp in enumerate(inpList):
#     nDict[inp]=[i,]




# encyprted=[int(inp) for inp in inpList]
# print(encyprted[0:3],encyprted[-3:])
# print(len(encyprted))

class number:
    def __init__(self,value,initialPosition):
        self.value=value
        self.initialPosition=initialPosition
        self.currentPosition=initialPosition
    def findNextToMove(self,numberList):
        if self.initialPosition<len(numberList)-1:
            self.nextToMove=numberList[self.initialPosition+1]
        else:
            self.nextToMove=None
    def updatePosition(self,moved):
        self.currentPosition+=moved
    def checkListLength(self,numberList):
        self.Nnumbs=len(numberList)
        self.maxInd=self.Nnumbs-1
    def move(self,numberList):
        # decrpytList=[]
        # for n in numberList:
        #     decrpytList.append(n.value)
        # print(decrpytList)
        if abs(self.value)>=self.Nnumbs:
            # print(self.value,self.Nnumbs)
            valueToMove=abs(self.value)%(self.Nnumbs-1)*int(self.value/abs(self.value)) #rly lost a long time on that one revolution does not take self.Nnumbs to complete but self.Nnumbs-1 -saw it when checking how many more steps it would take for the -2 in the first example to get back to its initial position
        else:
            valueToMove=self.value
        desiredInd=valueToMove+self.currentPosition  
        if desiredInd==0:
            movInd=self.maxInd
            for n in numberList[self.currentPosition+1:]:
                n.updatePosition(-1)
            numberList=numberList[0:self.currentPosition]+numberList[self.currentPosition+1:]+[self]
        elif desiredInd==self.maxInd:
            movInd=0
            for n in numberList[0:self.currentPosition]:
                n.updatePosition(1)
            numberList=[self]+numberList[0:self.currentPosition]+numberList[self.currentPosition+1:]
        elif 0<desiredInd<self.maxInd:
            movInd=desiredInd
            if self.currentPosition>movInd:
                for n in numberList[desiredInd:self.currentPosition]:
                    n.updatePosition(1)
                numberList=numberList[0:desiredInd]+[self]+numberList[desiredInd:self.currentPosition]+numberList[self.currentPosition+1:]
            else:
                for n in numberList[self.currentPosition+1:desiredInd+1]:
                    n.updatePosition(-1)
                numberList=numberList[0:self.currentPosition]+numberList[self.currentPosition+1:desiredInd+1]+[self]+numberList[desiredInd+1:]
        elif desiredInd>self.maxInd:
            valueToMove=valueToMove-(self.maxInd-self.currentPosition)
            movInd=valueToMove
            for n in numberList[movInd:self.currentPosition]:
                n.updatePosition(1)
            numberList=numberList[0:movInd]+[self]+numberList[movInd:self.currentPosition]+numberList[self.currentPosition+1:]
        elif desiredInd<0:
            valueToMove=valueToMove+self.currentPosition
            movInd=valueToMove+self.maxInd
            for n in numberList[self.currentPosition+1:movInd+1]:
                n.updatePosition(-1)
            numberList=numberList[0:self.currentPosition]+numberList[self.currentPosition+1:movInd+1]+[self]+numberList[movInd+1:]
        else:
            print(self.value,self.currentPosition,desiredInd)
            1
        self.currentPosition=movInd
        return numberList,self.nextToMove

nList=[]
for i,inp in enumerate(inpList):
    nList.append(number(int(inp),i))
for n in nList:
    n.checkListLength(nList)
    n.findNextToMove(nList)

nList,nextToMove=nList[0].move(nList)
moveCount=0
while moveCount<len(nList)-1:
    nList,nextToMove=nextToMove.move(nList)
    if len(nList)>5000:
        print(moveCount)
        1
    moveCount+=1

decrpytList=[]
for n in nList:
    decrpytList.append(n.value)
# print(decrpytList)

in0=decrpytList.index(0)
coordSum=0
for indToWrap in [1000,2000,3000]:
    if indToWrap>=len(nList):
        indWrap=indToWrap%len(nList)
    else:
        indWrap=indToWrap
    if in0+indWrap>len(nList)-1:
        indToCheck=indWrap-(len(nList)-in0)
    else:
        indToCheck=indWrap+in0
    # coordSum+=nList[indToCheck].value
    coordSum+=decrpytList[indToCheck]
    # print(in0,indToCheck,nList[indToCheck].value,decrpytList[indToCheck])
print('1st: ',coordSum)

#2nd problem
decryptionKey=811589153
nList2=[]
for i,inp in enumerate(inpList):
    nList2.append(number(int(inp)*decryptionKey,i))
for n in nList2:
    n.checkListLength(nList2)
    n.findNextToMove(nList2)

startNumber=nList2[0]
for _ in range(10):
    nList2,nextToMove=startNumber.move(nList2)
    moveCount=0
    # print('')
    while moveCount<len(nList2)-1:
        # print(nextToMove.value/decryptionKey,moveCount)
        nList2,nextToMove=nextToMove.move(nList2)
        moveCount+=1
        # print(moveCount)

for i,n in enumerate(nList2):
    if n.value==0:
        in0=i
        break
coordSum=0
for indToWrap in [1000,2000,3000]:
    if indToWrap>=len(nList2):
        indWrap=indToWrap%len(nList2)
    else:
        indWrap=indToWrap
    if in0+indWrap>len(nList2)-1:
        indToCheck=indWrap-(len(nList2)-in0)
    else:
        indToCheck=indWrap+in0
    coordSum+=nList2[indToCheck].value
    # print(in0,indToCheck,nList[indToCheck].value,decrpytList[indToCheck])
print('2nd: ',coordSum)