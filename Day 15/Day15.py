from preload import input
import numpy as np
# print(input)

# input=open('ex.txt').read()
inpList=input.strip().split('\n')

#1st problem
beacons=[]
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
    beacons.append((bx,by))

def rowChecker(yInterest):
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
                    noBeaconRow.append((uR[1]+1,pe))
                    ok=False
                    break
        if ok:
            uRange.append((ps,pe))
    return uRange

yInterest=2000000 #input data
uRange=rowChecker(yInterest)

pointSum=0
beaconsAtYinterest=set()
for uR in uRange:
    pointSum+=uR[1]-uR[0]+1
for beacon in beacons:
    if beacon[1]==yInterest:
        if beacon not in beaconsAtYinterest:
            beaconsAtYinterest.add(beacon)
            pointSum-=1
print('1st: ',pointSum)

#2nd problem, this solution works but it's slow :(
rangeMax=4000000 #input data
# rangeMax=20 #example
yIntRange=range(0,rangeMax+1,1) #example
y=0
while y < rangeMax:
    uRange=rowChecker(y)
    starts=[xs for (xs,_) in uRange if 0<=xs<=rangeMax]
    starts.remove(min(starts))
    ends=[xe for (_,xe) in uRange if 0<=xe<=rangeMax]

    for xs in starts:
        if xs-1 not in ends:
            yVal=y
            xVal=xs-1
            y=rangeMax
    y+=1
print('2nd: ',xVal*4000000+yVal)