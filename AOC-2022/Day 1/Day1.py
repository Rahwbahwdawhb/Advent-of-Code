from preload import input
# print(type(input))

#1st problem
inputList=input.split('\n')
maxSum=0
calSum=0
for row in inputList:
    if len(row)==0:
        newElf=False
        maxSum=max([maxSum,calSum])
        calSum=0
    else:
        newElf=True
    if newElf:
        calSum+=int(row)
print('1st: ',maxSum)

#2nd problem
calories=[]
newElf=True
calSum=0
for row in inputList:
    if len(row)==0:
        newElf=False
        calories.append(calSum)
        calSum=0
    else:
        newElf=True
    if newElf:
        calSum+=int(row)
calories.sort(reverse=True)
print('2nd: ',sum(calories[0:3]))