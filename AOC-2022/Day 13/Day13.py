from preload import input
# print(input)
# input=open('ex.txt').read()

inpList=input.strip().split('\n\n')
# for inp in inpList:
#     print(inp)

#1st problem
def comp(a,b):
    if isinstance(a,int) and isinstance(b,int):
        if a<b:
            return 1
        elif a==b:
            return 2
        else:
            return 3
    elif type(a) is list and type(b) is list:
        itMax=min([len(a),len(b)])-1
        it=0
        while True and it<=itMax:
            res=comp(a[it],b[it])
            if res==1 or res==3:
                break
            it+=1
        if itMax<0 or (it>itMax and res==2):
            if len(a)<len(b):
                return 1
            elif len(a)>len(b):
                return 3
            else:
                return 2
        else:
            return res
    elif type(a) is list and isinstance(b,int):
        res=comp(a,[b])
        return res
    elif isinstance(a,int) and type(b) is list:
        res=comp([a],b)
        return res

inRightOrder=[]
order=1
for inp in inpList:
    a,b=inp.split('\n')
    a_=eval(a)
    b_=eval(b)
    res=comp(a_,b_)
    # print(a)
    # print(b)
    # print(res)
    if res==1:
        inRightOrder.append(order)
    order+=1
    1
print('1st: ',sum(inRightOrder))


#2nd problem
inpList0=input.strip().split('\n')
inpList=[]
for inp in inpList0:
    if len(inp)!=0:
        inpList.append(inp)
        # print(inp)
inpList.append('[[2]]')
inpList.append('[[6]]')

wrongSum=1
while wrongSum!=0:
    wrongSum=0
    for i in range(0,len(inpList),2):
        a=inpList[i]
        b=inpList[i+1]
        res=comp(eval(a),eval(b))
        if res==3:
            inpList[i]=b
            inpList[i+1]=a
            wrongSum+=1
    for i in range(1,len(inpList)-1,2):
        a=inpList[i]
        b=inpList[i+1]
        res=comp(eval(a),eval(b))
        if res==3:
            inpList[i]=b
            inpList[i+1]=a
            wrongSum+=1
    # print(inpList[i])
decoderIndices=[]
for it,inp in enumerate(inpList):
    # print(inp)
    if inp=='[[2]]' or inp=='[[6]]':
        decoderIndices.append(it+1)
print('2nd: ',decoderIndices[0]*decoderIndices[1])
# for it,inp in enumerate(inpList):
#     a,b=inp.split('\n')
#     a_=eval(a)
#     b_=eval(b)
#     res=comp(a_,b_)
#     if res==3:
#         inpList[it]=b+'\n'+a