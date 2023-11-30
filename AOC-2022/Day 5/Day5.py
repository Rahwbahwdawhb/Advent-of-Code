from preload import input
import copy
# print(input)

#1st problem
inpList=input.split('\n')
crateConfig0=[]
for iter in range(9):
    crateConfig0.append([])
iter=0
for inp in inpList:
    if len(inp)==0:
        break
    crateLayer=[inp[i:i+4] for i in range(0,len(inp),4)]
    for ind,crate in enumerate(crateLayer):
        if '[' in crate:
            crateConfig0[ind].append(crate[1])
    iter+=1
for stack in crateConfig0:
    print(stack)
# movementList=[]

crateConfig=copy.deepcopy(crateConfig0)
for movement in inpList[iter+1:-1]:
    # movementList.append(movement)
    in1=movement.find('from')
    nCratesToMove=int(movement[5:in1-1])
    in2=movement.find('to')
    fromCrate=int(movement[in1+5:in2-1])-1
    toCrate=int(movement[in2+3:])-1
    # print(nCratesToMove,fromCrate,toCrate)
    movingCrates=[]
    for n in range(nCratesToMove):
        # movingCrates.append(crateConfig[fromCrate].pop(0))
        crateConfig[toCrate]=[crateConfig[fromCrate].pop(0)]+crateConfig[toCrate]

print('')
topCrates=''
for stack in crateConfig:
    # print(stack)
    topCrates+=stack[0]
print('1st: ',topCrates)

#2nd problem
crateConfig=copy.deepcopy(crateConfig0)
for movement in inpList[iter+1:-1]:
    # movementList.append(movement)
    in1=movement.find('from')
    nCratesToMove=int(movement[5:in1-1])
    in2=movement.find('to')
    fromCrate=int(movement[in1+5:in2-1])-1
    toCrate=int(movement[in2+3:])-1
    # print(nCratesToMove,fromCrate,toCrate)
    movingCrates=[]
    for n in range(nCratesToMove):
        movingCrates.append(crateConfig[fromCrate].pop(0))
    # movingCrates.reverse()
    crateConfig[toCrate]=movingCrates+crateConfig[toCrate]

topCrates=''
for stack in crateConfig:
    # print(stack)
    topCrates+=stack[0]
print('2nd: ',topCrates)


