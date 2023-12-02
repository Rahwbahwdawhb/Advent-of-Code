import os
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read()
inputList=inputStr.strip().split('\n')
redLimit=12
greenLimit=13
blueLimit=14
validGameIDsum=0
powerSum=0
for game in inputList:
    gameID_str,draw_str=game.split(':')
    gameID=int(gameID_str.split(' ')[-1])
    drawList=draw_str.strip().split(';')
    # print(gameID,drawList[0])
    countDict={'red':0,'green':0,'blue':0}
    for draw in drawList:
        outcomes=draw.split(',')
        for outcome in outcomes:
            number,color=outcome.strip().split(' ')
            countDict[color]=max([countDict[color],int(number)])
    # print(gameID_str,countDict)
    powerSum+=countDict['red']*countDict['green']*countDict['blue']
    if countDict['red']<=redLimit and countDict['green']<=greenLimit and countDict['blue']<=blueLimit:
        validGameIDsum+=gameID
print('1st:',validGameIDsum)
print('2nd:',powerSum)