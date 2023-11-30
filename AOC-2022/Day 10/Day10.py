from preload import input
# print(input)

#1st problem
# input='noop\naddx 3\naddx -5'
# input=open('ex2.txt').read().strip()
inpList=input.strip().split('\n')
cycle=1
X=1
cyclesToGo=len(inpList)
currentAdder=(0,0)
inpToRead=0
cycleToCheck=20
signalSum=0
noMoreInputs=False
xPos=[]
while cycle<=cyclesToGo:
    currentAdder=(max([0,currentAdder[0]-1]),currentAdder[1])
    if currentAdder[0]==0:
        X+=currentAdder[1]
        currentAdder=(0,0)
    if currentAdder[0]==0:
        # X+=currentAdder[1]
        # currentAdder=(0,0)
        if inpToRead<len(inpList):
            inp=inpList[inpToRead]
            if inp.find('addx')!=-1:
                _,val=inp.split(' ')
                currentAdder=(2,int(val))
                cyclesToGo+=2
            inpToRead+=1
        else:
            noMoreInputs=True
    # else:
    #     currentAdder=(currentAdder[0]-1,currentAdder[1])
    if cycle==cycleToCheck:
        signalSum+=cycle*X
        # print(cycle*X)
        cycleToCheck+=40
    # print(cycle,currentAdder,X)
    if noMoreInputs and currentAdder[0]==0:
        break
    xPos.append(X)
    cycle+=1
print('1st: ',signalSum)

#2nd problem
dispStr=''
row=0
col=0
count=0
while count<240:
    if col>=40: #this check needs to come first, need to initiate print on new row before comparison with x-position, took too long time to see this :D
        col=0
        dispStr+='\n'
    if abs(col-xPos[count])<2:
            dispStr+='#'
    else:
        dispStr+='.'
    
    # if col<40:
    #     if abs(col-xPos[count])<2:
    #         dispStr+='#'
    #     else:
    #         dispStr+='.'
    # else:
    #     col=0
    #     dispStr+='\n'
        # row+=1
    col+=1
    count+=1        
print('2nd:')
print(dispStr)


