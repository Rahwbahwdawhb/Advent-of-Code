from preload import input
# print(input)

#1st problem
# input='A Y\nB X\nC Z'
inputList=input.split('\n')
a_dict={
    "A X":3+1,
    "A Y":6+2,
    "A Z":0+3,
    "B X":0+1,
    "B Y":3+2,
    "B Z":6+3,
    "C X":6+1,
    "C Y":0+2,
    "C Z":3+3,
    }

print(inputList[0])
print(inputList[-2])
# print(inputList[:-1])
score=0
# it=0
for row in inputList:
    # print(row)
#     # a,b=row.split(' ')
#     # print(a+'?'+b)
    # print(row,a_dict[row],it)
    # if it==2499:
    #     1
    # it+=1
    if len(row)!=0:
        score+=a_dict[row]
print(score)

#2nd problem
#x=lose, y=draw, z=win
b_dict={
    "A X":"A Z",
    "A Y":"A X",
    "A Z":"A Y",
    "B X":"B X",
    "B Y":"B Y",
    "B Z":"B Z",
    "C X":"C Y",
    "C Y":"C Z",
    "C Z":"C X",
    }

score=0
for row in inputList:
    if len(row)!=0:
        score+=a_dict[b_dict[row]]
print(score)
