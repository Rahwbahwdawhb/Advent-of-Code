import os
import re
os.chdir(os.path.dirname(__file__))

file='input.txt'

with open(file) as f:
    pattern=f.read().strip()

def patternSum(pattern,productBool=False):
    patternList=pattern.split('mul(')
    del patternList[0]
    totalSum=0
    products=[]
    patterns=[]
    for fragment in patternList:
        close=fragment.find(')')
        numbers=fragment[:close].split(',')
        if close!=-1 and len(numbers)==2: #initially missed the close!=-1, which could result in values without a closing parenthesis getting added
            product=1
            bools=[]
            for x in numbers:
                if 1<=len(x)<=3 and x.isdigit():
                    product*=int(x)
                    bools.append(True)
                else:
                    bools.append(False)
            if bools[0] and bools[1]:
                totalSum+=product
                products.append(product)
                patterns.append('mul('+fragment)
    if productBool:
        return totalSum,products,patterns
    else:
        return totalSum
print('1st:',patternSum(pattern))

#2nd problem, first idea of solving it
alternatives=["don't()","do()"]
lastAlternative=''
currentAlternative=alternatives[0]
currentPattern=pattern
sumPatterns=[]
alts=[]
while currentPattern!='':
    ind=currentPattern.find(currentAlternative)
    if ind!=-1:
        if currentAlternative==alternatives[0] and (lastAlternative==alternatives[1] or lastAlternative==''):
            sumPatterns.append(currentPattern[:ind])
            lastAlternative=currentAlternative
            currentAlternative=alternatives[1]
            currentPattern=currentPattern[ind+len(lastAlternative):]
        elif currentAlternative==alternatives[1] and lastAlternative==alternatives[0]:
            lastAlternative=currentAlternative
            currentAlternative=alternatives[0]
            currentPattern=currentPattern[ind+len(lastAlternative):]
        alts.append(currentAlternative)
    else:
        if len(currentPattern)>0:
            sumPatterns.append(currentPattern)
        break
finalSum=0
for p in sumPatterns:
    finalSum+=patternSum(p)
print('2nd:',finalSum)


#2nd problem, simpler solution
pattern2="do()"+pattern
tSum=0
i0o=0
while True:
    i0=pattern2[i0o:].find("do()")
    if i0==-1:
        break
    i0+=i0o
    i1=pattern2[i0:].find("don't()")
    if i1!=-1:
        i1+=i0
        tSum+=patternSum(pattern2[i0+4:i1])
        i0o=i1+7
    else:
        tSum+=patternSum(pattern2[i0+4:])
        break
print('2nd:',tSum,'(simpler solution)')

# #sanity check that revealed the missed close!=-1 in patternSum
# doList=pattern.split("do()")
# sum3=0
# sum3_=0
# for d in doList:
#     in_=d.find("don't()")
#     if in_==-1:
#         sum3+=patternSum(d)
#     else:
#         sum3+=patternSum(d[:in_])
#         sum3_+=patternSum(d[in_:])


