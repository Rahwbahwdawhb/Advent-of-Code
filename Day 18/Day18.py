from preload import input

input=open('ex.txt').read()
# print(input)
inpList=input.strip().split('\n')

#1st problem
cubesAt=[]
for inp in inpList:
    x,y,z=inp.split(',')
    cubesAt.append((int(x),int(y),int(z)))

freeSides=0
freeSidesSet=set()
for x,y,z in cubesAt:
    toCheck=[(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]
    for i,side in enumerate(toCheck):
        if side not in cubesAt:
            freeSides+=1
            freeSidesSet.add((x,y,z))
            # freeSidesList.append(side)
print('1st: ',freeSides)
    

#2nd problem
freeSidesList=list(freeSidesSet)
freeSidesList.sort(key=lambda x:x[2])
zLevels=[]
temp=[]
zLevels.append(temp)
zTemp=freeSidesList[0][2]
for side in freeSidesList:
    z=side[2]
    if z!=zTemp:
        zTemp=z
        zLevels.append(temp)
        temp=[]
    temp.append(side)
zLevels.append(temp)
for zL in zLevels:
    zT=sorted(zL,key=lambda x:x[0])
    xy=[(xt,yt) for xt,yt,_ in zT]    
    print(zL[0][2],xy)


# def getConnections(refIn):
#     x=refIn[0]
#     y=refIn[1]
#     z=refIn[2]
#     # XY_z0=[(x+1,y,z),(x-1,y,z),(x+1,y+1,z),(x+1,y-1,z),(x-1,y+1,z),(x-1,y-1,z),(x,y-1,z),(x,y+1,z)]
#     # XY_z1=[(x+1,y,z+1),(x-1,y,z+1),(x+1,y+1,z+1),(x+1,y-1,z+1),(x-1,y+1,z+1),(x-1,y-1,z+1),(x,y-1,z+1),(x,y+1,z+1),(x,y,z+1)]
#     # XY_z2=[(x+1,y,z-1),(x-1,y,z-1),(x+1,y+1,z-1),(x+1,y-1,z-1),(x-1,y+1,z-1),(x-1,y-1,z-1),(x,y-1,z-1),(x,y+1,z-1),(x,y,z-1)]
#     # XY_z0=[(x+1,y,z),(x-1,y,z),(x+1,y+1,z),(x+1,y-1,z),(x-1,y+1,z),(x-1,y-1,z),(x,y-1,z),(x,y+1,z)]
#     # XY_z1=[(x+1,y,z+1),(x-1,y,z+1),(x,y-1,z+1),(x,y+1,z+1),(x,y,z+1)]
#     # XY_z2=[(x+1,y,z-1),(x-1,y,z-1),(x,y-1,z-1),(x,y+1,z-1),(x,y,z-1)]
#     # XY_z0=[(x+1,y+1,z),(x+1,y-1,z),(x-1,y+1,z),(x-1,y-1,z)]
#     # XY_z1=[(x+1,y,z+1),(x-1,y,z+1),(x,y-1,z+1),(x,y+1,z+1)]
#     # XY_z2=[(x+1,y,z-1),(x-1,y,z-1),(x,y-1,z-1),(x,y+1,z-1)]
#     # XY_z0=[(x+1,y,z),(x-1,y,z),(x,y-1,z),(x,y+1,z)]
#     # XY_z1=[(x,y,z+1)]
#     # XY_z2=[(x,y,z-1)]

#     # XY_z0=[(x+1,y,z),(x-1,y,z),(x,y-1,z),(x,y+1,z)]
#     # XY_z1=[(x+1,y,z+1),(x-1,y,z+1),(x,y+1,z+1),(x,y-1,z+1)]
#     # XY_z2=[(x+1,y,z-1),(x-1,y,z-1),(x,y+1,z-1),(x,y-1,z-1)]
#     XY_z0=[(x+1,y,z),(x-1,y,z),(x,y-1,z),(x,y+1,z),(x+1,y+1,z),(x-1,y+1,z),(x,y+1,z),(x,y-1,z)]
#     XY_z1=[(x+1,y,z+1),(x-1,y,z+1),(x,y+1,z+1),(x,y-1,z+1),(x+1,y+1,z+1),(x-1,y+1,z+1),(x,y+1,z+1),(x,y-1,z+1)]
#     XY_z2=[(x+1,y,z-1),(x-1,y,z-1),(x,y+1,z-1),(x,y-1,z-1),(x+1,y+1,z-1),(x-1,y+1,z-1),(x,y+1,z-1),(x,y-1,z-1)]
#     return XY_z0+XY_z1+XY_z2

# from copy import deepcopy
# lookList=deepcopy(freeSidesList)
# oneSurface=[]
# ref=lookList.pop(0)
# oneSurface.append(ref)
# refIn=0
# while True:
#     refCheck=getConnections(ref)
#     for i in range(len(lookList)):
#         if lookList[i] in refCheck:
#             oneSurface.append(lookList.pop(i))
#             break
#     refIn+=1
#     if refIn>len(oneSurface)-1:
#         break
#     else:
#         ref=oneSurface[refIn]
# print(len(oneSurface))
# print(len(lookList))


# import numpy as np
# freeSidesList=np.array(freeSidesList)
# meanPos=[np.mean([x for x in freeSidesList[0]]),np.mean([y for y in freeSidesList[1]]),np.mean([z for z in freeSidesList[1]])]
# # exteriorSides=freeSides
# radDists=[]
# for x,y,z in freeSidesList:
#     radDists.append(abs(x-meanPos[0])+abs(y-meanPos[1])+abs(z-meanPos[2]))
# mRD=np.mean(radDists)
# print(len([rd for rd in radDists if rd<mRD]))

# exteriorSides=0
# for x,y,z in cubesAt:
#     toCheck=[(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]
#     for i,side in enumerate(toCheck):
#         if side not in cubesAt:
#             if i==0 and len([xt for xt,yt,zt in cubesAt if yt==y and zt==z and xt>x+1])==0:
#                 exteriorSides+=1
#             if i==1 and len([xt for xt,yt,zt in cubesAt if yt==y and zt==z and xt<x-1])==0:
#                 exteriorSides+=1
#             if i==2 and len([yt for xt,yt,zt in cubesAt if xt==x and zt==z and yt>y+1])==0:
#                 exteriorSides+=1
#             if i==3 and len([yt for xt,yt,zt in cubesAt if xt==x and zt==z and yt<y-1])==0:
#                 exteriorSides+=1
#             if i==4 and len([zt for xt,yt,zt in cubesAt if xt==x and yt==y and zt>z+1])==0:
#                 exteriorSides+=1
#             if i==5 and len([zt for xt,yt,zt in cubesAt if xt==x and yt==y and zt<z-1])==0:
#                 exteriorSides+=1
# print('2nd: ',exteriorSides)