from preload import input
import numpy as np
# print(input)

# input=open('ex.txt').read()
inpList=input.strip().split('\n')

#1st problem
# sensors=[]
# beacons=[]
# yInterest=10
noBeaconAt=set()
for inp in inpList:
    s,b=inp.split(':')
    sx,sy=s.split(',')
    bx,by=b.split(',')
    sx=int(sx[sx.find('=')+1:])
    sy=int(sy[sy.find('=')+1:])
    bx=int(bx[bx.find('=')+1:])
    by=int(by[by.find('=')+1:])
    dx=abs(bx-sx)
    dy=abs(by-sy)
    scanMaxRange=dx+dy

    noBeaconAt.add(((sx,sy+scanMaxRange),(sx-scanMaxRange,sy),(sx+scanMaxRange,sy),(sx,sy-scanMaxRange)))

    
    # noBeacons=[]
    # tempY=sy-scanMaxRange
    # xExt=0
    # while tempY!=sy+scanMaxRange+1:
    #     tempXrange=range(sx-xExt,sx+xExt+1,1)
    #     for xP in tempXrange:
    #         noBeacons.append((xP,tempY))
    #     tempY+=1
    #     if tempY<=sy:
    #         xExt+=1
    #     else:
    #         xExt-=1
    # # print(sx,sy)
    # noBeacons.remove((bx,by))
    # for point in noBeacons:
    #     if point[1]==yInterest:
    #         noBeaconAt.add(point)
    # sensors.append((sx,sy))
    # beacons.append((bx,by))
# for i,s in enumerate(sensors):
#     print(s,beacons[i])

# yInterest=10
# pointsYinterest=[]
# for point in noBeaconAt:
#     if point[1]==yInterest:
#         pointsYinterest.append(point)
# yInterest=10
yInterest=2000000
noBeaconRow=[]
for noBeaconRegion in noBeaconAt:
    if noBeaconRegion[3][1]<=yInterest<=noBeaconRegion[0][1]:        
        if yInterest==noBeaconRegion[1][1]:
            rowAdd=[noBeaconRegion[1][0],noBeaconRegion[2][0]]
        else:
            # yDiff=noBeaconRegion[0][1]-noBeaconRegion[1][1]-abs(yInterest-noBeaconRegion[1][1])
            yDiff=abs(yInterest-noBeaconRegion[1][1])
            maxR=noBeaconRegion[0][1]-noBeaconRegion[1][1]
            # rowAdd=[noBeaconRegion[1][0]-yDiff,noBeaconRegion[1][0]+yDiff]
            rowAdd=[noBeaconRegion[0][0]-(maxR-yDiff),noBeaconRegion[0][0]+(maxR-yDiff)]
        noBeaconRow.append(rowAdd)
# print(len(rowAdd))
# print(noBeaconRow)
uRange=[]
while len(noBeaconRow)!=0:
    r=noBeaconRow.pop(0)
    ps=r[0]
    pe=r[1]
    ok=True
    for uR in uRange:
        if ps>uR[1] or pe<uR[0]:
            pass
        else:
            if ps<uR[0] and pe<=uR[1]:
                pe=uR[0]-1
            elif ps>=uR[0] and pe>uR[1]:
                ps=uR[1]+1
            elif ps>=uR[0] and pe<=uR[1]:
                ok=False
                break
            else:
                noBeaconRow.append((ps,uR[0]-1))
                noBeaconRow.append((pe,uR[1]+1))
                ok=False
                break
    if ok:
        uRange.append((ps,pe))
# print(uRange)
pointSum=0
for uR in uRange:
    pointSum+=uR[1]-uR[0]+1

print('1st: ',pointSum)
#2nd problem

