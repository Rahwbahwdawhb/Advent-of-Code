import os
os.chdir(os.path.dirname(__file__))
with open('input.txt') as f:
    data=f.read().strip().split('\n')
list_1=[]
list_2=[]
for row in data:
    rowList=row.split()
    list_1.append(int(rowList[0]))
    list_2.append(int(rowList[1]))
difference_sum=0 #answer for part 1
similarity_sum=0 #answer for part 2
for id1,id2 in zip(sorted(list_1),sorted(list_2)):
    difference_sum+=abs(id1-id2) #part 1
    similarity_sum+=id1*list_2.count(id1) #part 2
print('1st:',difference_sum)
print('2nd:',similarity_sum)