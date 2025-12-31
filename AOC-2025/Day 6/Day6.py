import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    data_list=f.read().strip().split('\n')
N=len(data_list)
numbers_dict=dict()
for i,row in enumerate(data_list):
    parts=row.split()
    if i==0:
        for ii in range(len(parts)):
            numbers_dict[ii]=[]
            1
    if i!=N-1:
        for ii,part in enumerate(parts):
            numbers_dict[ii].append(int(part))
    else:
        operators=parts

sum_total=0
for operator,(_,numbers) in zip(operators,numbers_dict.items()):
    match operator:
        case '*':
            temp=1
            for number in numbers:
                temp*=number
        case '+':
            temp=0
            for number in numbers:
                temp+=number
    sum_total+=temp
print("1st:",sum_total)

M=len(data_list[0])
last=0
number_chunks=[]
for i in range(M):
    temp_sum=0
    for row in data_list[:-1]:
        if not row[i].isdigit():
            temp_sum+=1
    if temp_sum==N-1:
        temp=[]
        for row in data_list[:-1]:
            temp.append(row[last:i])
        number_chunks.append(temp)
        last=i+1

temp=[]
for row in data_list:
    temp.append(row[last:])
number_chunks.append(temp)
sum_total_2=0
for operator,number_chunk in zip(operators,number_chunks):
    match operator:
        case '*':
            temp=1
            for i in range(len(number_chunk[0])):
                temp2=""
                for ii in range(N-1):
                    temp2+=number_chunk[ii][i]
                temp*=int(temp2)
        case '+':
            temp=0
            for i in range(len(number_chunk[0])):
                temp2=""
                for ii in range(N-1):
                    temp2+=number_chunk[ii][i]
                temp+=int(temp2)
    sum_total_2+=temp
print("2nd:",sum_total_2)