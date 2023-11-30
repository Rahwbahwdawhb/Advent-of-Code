from preload import input
# print(input)

# input='mjqjpqmgbljsphdztnvjfqwrcgsmlb'
# input='bvwbjplbgvbhsrlpgdmjqwftvncz'
#1st problem
inpList=input.split('\n')
inpStr=inpList[0]
# print(len(inpList),inpList[0])
# print(len(inpStr))
n=4
subStrs=[inpStr[i:i+n] for i in range(0,len(inpStr))]
iter=0
for subStr in subStrs:
    # print(subStr)
    uChars=''.join(set(subStr))
    if len(uChars)==n:
        break
    iter+=1
print('1st: ',iter+n)

#2nd problem
n=14
subStrs=[inpStr[i:i+n] for i in range(0,len(inpStr))]
iter=0
for subStr in subStrs:
    # print(subStr)
    uChars=''.join(set(subStr))
    if len(uChars)==n:
        break
    iter+=1
print('2nd: ',iter+n)

