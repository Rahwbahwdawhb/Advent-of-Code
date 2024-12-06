import os

os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'
# file='example2.txt'
# file='example3.txt'
# file='example4.txt'

with open(file) as f:
    dataList=f.read().strip().split('\n')

dims=(len(dataList),len(dataList[0]))

grid=[]
rows=[]
rows_i=[]
for ir,row in enumerate(dataList):
    rows.append(row)
    rows_i.append([(ir,ic) for ic in range(dims[1])])
    grid.append([ch for ch in row])
cols=[]
cols_i=[]
for i in range(dims[1]):
    cols.append(''.join([grid[j][i] for j in range(dims[0])]))
    cols_i.append([(ir,i) for ir in range(dims[0])])

bot_diags_1=[]
bot_diags_1_i=[]
ir_start=0
while ir_start<dims[0]:
    ir=ir_start
    ic=0
    tempList=[]
    tempList_i=[]
    while True:
        try:
            tempList.append(grid[ir][ic])
            tempList_i.append((ir,ic))
            ir+=1
            ic+=1
        except:
            break
    bot_diags_1.append(''.join(tempList))
    bot_diags_1_i.append(tempList_i)
    ir_start+=1

top_diags_1=[]
top_diags_1_i=[]
ic_start=0
while ic_start<dims[1]:
    ic=ic_start
    ir=0
    tempList=[]
    tempList_i=[]
    while True:
        try:
            tempList.append(grid[ir][ic])
            tempList_i.append((ir,ic))
            ir+=1
            ic+=1
        except:
            break
    top_diags_1.append(''.join(tempList))
    top_diags_1_i.append(tempList_i)
    ic_start+=1

bot_diags_2=[]
bot_diags_2_i=[]
ir_start=0
while ir_start<dims[0]:
    ir=ir_start
    ic=dims[0]-1
    tempList=[]
    tempList_i=[]
    while True:
        try:
            tempList.append(grid[ir][ic])
            tempList_i.append((ir,ic))
            ir+=1
            ic-=1
        except:
            break
    bot_diags_2.append(''.join(tempList))
    bot_diags_2_i.append(tempList_i)
    ir_start+=1

top_diags_2=[]
top_diags_2_i=[]
ic_start=dims[0]-1
while ic_start>=0:
    ic=ic_start
    ir=0
    tempList=[]
    tempList_i=[]
    while ic>=0:
        try:
            tempList.append(grid[ir][ic])
            tempList_i.append((ir,ic))
            ir+=1
            ic-=1
        except:
            break
    top_diags_2.append(''.join(tempList))
    top_diags_2_i.append(tempList_i)
    ic_start-=1

#removing duplicate main diagonals
all_diags=bot_diags_1+top_diags_1[1:]+bot_diags_2+top_diags_2[1:] 
all_diags_i=bot_diags_1_i+top_diags_1_i[1:]+bot_diags_2_i+top_diags_2_i[1:]

to_search=rows+cols+all_diags
to_search_i=rows_i+cols_i+all_diags_i
find_str='XMAS'
N=len(find_str)
find_count=0
for str_ in to_search:
    temp=str_
    while True:
        ind=temp.find(find_str)
        if ind!=-1:
            find_count+=1
            temp=temp[ind+N:]
        else:
            break
    temp=str_[::-1]
    while True:
        ind=temp.find(find_str)
        if ind!=-1:
            find_count+=1
            temp=temp[ind+N:]
        else:
            break
print('1st:',find_count)

#part 2, idea: appoint indices to all grid points and for each MAS along diagonals, save the A index and count common indices for diagonals in both directions
find_str='MAS'
N=len(find_str)
A_is=[]
for iter in range(2):
    if iter==1:
        to_search=bot_diags_1+top_diags_1[1:]
        to_search_i=bot_diags_1_i+top_diags_1_i[1:]
    else:
        to_search=bot_diags_2+top_diags_2[1:]
        to_search_i=bot_diags_2_i+top_diags_2_i[1:]
    find_count=0
    temp_is=[]
    for str_,ins in zip(to_search,to_search_i):
        temp=str_
        temp_i=ins+[]
        while True:
            ind=temp.find(find_str)
            if ind!=-1:
                find_count+=1                
                temp_is.append(temp_i[ind+1])
                # if grid[temp_is[-1][0]][temp_is[-1][1]]!='A':  #sanity check
                #     1
                temp=temp[ind+N:]
                temp_i=temp_i[ind+N:]
            else:
                break
        temp=str_[::-1]
        temp_i=ins[::-1]+[] #important to flip here since the arrays in the while loop are cropped!
        while True:
            ind=temp.find(find_str)
            if ind!=-1:
                find_count+=1                
                temp_is.append(temp_i[ind+1])
                # if grid[temp_is[-1][0]][temp_is[-1][1]]!='A': #sanity check
                #     1
                temp=temp[ind+N:]
                temp_i=temp_i[ind+N:]
            else:
                break
    A_is.append(temp_is)

if len(A_is[0])>len(A_is[1]):
    longer=set(A_is[0])
    shorter=set(A_is[1])
else:
    longer=set(A_is[1])
    shorter=set(A_is[0])
common_counter=0
for s in shorter:
    if s in longer:
        common_counter+=1
print('2nd:',common_counter)