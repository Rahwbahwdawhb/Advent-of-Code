from preload import input

# input=open('ex.txt').read()
inpList=input.strip().split('\n')
# print(input)
# print(len(inpList))

#1st problem
monkeyNumberDict=dict()
monkeyCalcList=[]
for inp in inpList:
    name,action=inp.split(': ')
    if action.find('+')==-1 and action.find('-')==-1 and action.find('*')==-1 and action.find('/')==-1:
        monkeyNumberDict[name]=action
    else:
        name1,calc,name2=action.split(' ')
        monkeyCalcList.append((name,name1,name2,calc))

# for m in monkeyNumberDict:
#     print(m,monkeyNumberDict[m])
# print('')
# for m in monkeyCalcList:
#     print(m)

while len(monkeyCalcList)!=0:
    finishedCalcs=[]
    for i,m in enumerate(monkeyCalcList):
        if m[1] in monkeyNumberDict.keys() and m[2] in monkeyNumberDict.keys():
            monkeyNumber=eval(monkeyNumberDict[m[1]]+m[3]+monkeyNumberDict[m[2]])
            monkeyNumberDict[m[0]]=str(int(monkeyNumber))
            finishedCalcs.append(i)
    for i in sorted(finishedCalcs,reverse=True):
        del monkeyCalcList[i]
print('1st: ',monkeyNumberDict['root'])

#2nd problem
monkeyDict=dict()
for inp in inpList:
    name,action=inp.split(': ')
    if name=='root':
        name1,_,name2=action.split(' ')
        monkeyDict['root']=name1+'=='+name2
        numsToBeCompared=[name1,name2]
    elif name=='humn':
        monkeyDict['humn']='x'
    else:
        monkeyDict[name]=action

mknNames=monkeyDict.keys()
expressions=[]
for name in numsToBeCompared:
    nameTemp=name
    namesFound=1
    while namesFound!=0:
        namesFound=0
        for mName in mknNames:
            if mName in nameTemp:
                namesFound+=1
                nameTemp=nameTemp.replace(mName,'('+monkeyDict[mName]+')')
    expressions.append(nameTemp)    
    # print(nameTemp)
for exp in expressions:
    if exp.find('x')==-1:
        # compValue=eval(exp)
        compStr=exp
    else:
        lhs=exp

import sympy
sympy_eq=sympy.sympify('Eq('+lhs+','+compStr+')')
toYell=sympy.solve(sympy_eq)[0]
print('2nd:',toYell)
1




