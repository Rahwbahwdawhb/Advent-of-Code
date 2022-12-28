from preload import input
import numpy as np

input=open('ex.txt').read()
# print(input)
boardStr,pathStr=input.split('\n\n')
# print(boardStr,pathStr)
 

#1st problem
board=[]
walls=[]
colBoundaries=dict()
maxCol=0
for rowIn,row in enumerate(boardStr.split('\n')):
    temp=[]
    onMap=[]
    for colIn,tile in enumerate(row):
        if tile=='#':
            walls.append((rowIn+1,colIn+1))
            onMap.append(colIn)
        elif tile=='.':
            onMap.append(colIn)
        temp.append(tile)
    colBoundaries[rowIn+1]=[min(onMap)+1,max(onMap)+1]
    maxCol=max([maxCol,len(temp)])
    board.append(temp)
rowBoundaries=dict()
maxRow=len(board)
for colIn in range(maxCol):
    rowInsOnMap=[]
    for j in range(len(board)):
        if len(board[j])-1<colIn:
            pass
        else:
            if board[j][colIn]=='#' or board[j][colIn]=='.':
                rowInsOnMap.append(j)
    rowBoundaries[colIn+1]=[min(rowInsOnMap)+1,max(rowInsOnMap)+1]

# for row in board:
#     print(row)
# print(board[-1])
pathStr='R'+pathStr.strip()
pathInstr=[]
temp=[]
for ch in pathStr:
    if ch=='R' or ch=='L':
        pathInstr.append(''.join(temp))
        temp=[ch]
    else:
        temp.append(ch)
pathInstr.append(''.join(temp))
pathInstr=pathInstr[1:]
# print(pathInstr)
# print(path)
# print(walls)
pos=np.array([1,[i for i,t in enumerate(board[0]) if t=='.'][0]+1])
#Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
facings=[0,1,2,3] 
# moveDict={0:np.array([0,1]),1:np.array([1,0]),2:np.array([0,-1]),3:np.array([-1,0])}
moveDict={0:np.array([0,1]),1:np.array([1,0]),2:np.array([0,1]),3:np.array([1,0])}
facingIn=3

for move in pathInstr:
    if move[0]=='R':
        facingIn+=1
        if facingIn==4:
            facingIn=0
    else:
        facingIn-=1
        if facingIn==-1:
            facingIn=3
    moveDir=facings[facingIn]
    moveIntent=int(move[1:])
    if facingIn==0 or facingIn==2:
        wallsOfInterest=[x for y,x in walls if y==pos[0]]
        xyCheck=pos[1]
        hitWallCorrection=np.array([1,0])
        minBound=colBoundaries[pos[0]][0]
        maxBound=colBoundaries[pos[0]][1]
        xyMin=np.array([pos[0],minBound])
        xyMax=np.array([pos[0],maxBound])
    else:
        wallsOfInterest=[y for y,x in walls if x==pos[1]]
        xyCheck=pos[0]
        hitWallCorrection=np.array([0,1])
        minBound=rowBoundaries[pos[1]][0]
        maxBound=rowBoundaries[pos[1]][1]
        xyMin=np.array([minBound,pos[1]])
        xyMax=np.array([maxBound,pos[1]])
    if facingIn==2 or facingIn==3:
        moveIntent*=-1
        hitWallSign=-1
    else:
        hitWallSign=1
    maxMove=maxBound+1-minBound
    xyTemp=xyCheck+moveIntent
    # print(move,facingIn,moveDir,moveIntent)
    # print(pos)
    if len(wallsOfInterest)==0:
        if minBound<=xyTemp<=maxBound:
            pos=pos+moveIntent*moveDict[facingIn]
        elif xyTemp<minBound:
            moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(xyCheck-minBound))
            if moveIntent==maxMove:
                pos=xyMin
            elif moveIntent>maxMove:
                moveIntent%=maxMove
                pos=xyMax+(moveIntent-np.sign(moveIntent))*moveDict[facingIn]
            else:
                pos=xyMax+(moveIntent-np.sign(moveIntent))*moveDict[facingIn]
        else:
            moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(maxBound-xyCheck))
            if moveIntent==maxMove:
                pos=xyMax
            elif moveIntent>maxMove:
                moveIntent%=maxMove
                pos=xyMin+(moveIntent-np.sign(moveIntent))*moveDict[facingIn]
            else:
                pos=xyMin+(moveIntent-np.sign(moveIntent))*moveDict[facingIn] 
    else:
        posDiff=wallsOfInterest-xyCheck
        if facingIn==2 or facingIn==3:
            prior=[i for i,xyd in enumerate(posDiff) if xyd<0]
            if len(prior)==0:
                closest=wallsOfInterest[-1]
            else:
                closest=wallsOfInterest[prior[-1]]
        else:
            coming=[i for i,xyd in enumerate(posDiff) if xyd>0]
            if len(coming)==0:
                closest=wallsOfInterest[0]
            else:
                closest=wallsOfInterest[coming[0]]
        closeDiff=xyCheck-closest
        # if np.sign((xyCheck-closest)*(xyTemp-closest))==hitWallSign:
        if np.sign(xyCheck-closest)!=np.sign(xyTemp-closest):
            pos=hitWallCorrection*pos+moveDict[facingIn]*(closest-hitWallSign)
        else:
            if minBound<=xyTemp<=maxBound:
                pos=pos+moveIntent*moveDict[facingIn]
            elif xyTemp<minBound:
                if closest==maxBound:
                    pos=xyMin
                else:
                    moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(xyCheck-minBound))
                    xyTemp=maxBound+(moveIntent-np.sign(moveIntent))
                    # if np.sign(xyTemp-closest)==hitWallSign:
                    if np.sign(maxBound-closest)!=np.sign(xyTemp-closest):
                        pos=hitWallCorrection*pos+moveDict[facingIn]*(closest-hitWallSign)
                    else:
                        pos=xyMax+(moveIntent-np.sign(moveIntent))*moveDict[facingIn]
            else:
                if closest==minBound:
                    pos=xyMax
                else:
                    moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(maxBound-xyCheck))
                    xyTemp=minBound+(moveIntent-np.sign(moveIntent))
                    # if np.sign(xyTemp-closest)==hitWallSign:
                    if np.sign(minBound-closest)!=np.sign(xyTemp-closest):
                        pos=hitWallCorrection*pos+moveDict[facingIn]*(closest-hitWallSign)
                    else:
                        pos=xyMin+(moveIntent-np.sign(moveIntent))*moveDict[facingIn]
# print(pos)
print('1st: ',1000*pos[0]+4*pos[1]+moveDir)

#2nd problem

class side:
    def __init__(self,label,up,down,left,right,rowRange,colRange,sideList,sideSize):
        self.label=label
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.neighbors=[up,down,left,right]
        self.rowRange=rowRange
        self.colRange=colRange
        self.upDict=dict()
        self.downDict=dict()
        self.leftDict=dict()
        self.rightDict=dict()
        self.sideList=sideList
        self.sideSize=sideSize
    def getMapping(self):
        for n in self.neighbors:
            nn=[nnn for nnn in self.sideList if nnn.label()==n[0]][0]
            #connected to: 
            # (1,0,1)=top row normal column order
            # (1,0,-1)=top row reversed column order
            # (-1,0,1)=bot row normal column order
            # (-1,0,-1)=bot row reversed column order
            # (0,1,1)=leftmost column normal row order
            # (0,1,-1)=leftmost column reversed column order
            # (0,-1,1)=rightmost column normal column order
            # (0,-1,-1)=rightmost column reversed column order
            if n[1]==(0,1,1):
                neighRange_row=[i in range(nn.rowRange[0],nn.rowRange[1]+1,1)]
                neighRange_col=[]
                for _ in range(self.sideSize):
                    neighRange_col.append(nn.colRange[0])
            elif n[1]==(0,1,-1):
                neighRange_row=[self.sideSize-i+1 in range(nn.rowRange[0],nn.rowRange[1]+1,1)]
                neighRange_col=[]
                for _ in range(self.sideSize):
                    neighRange_col.append(nn.colRange[0])
            elif n[1]==(0,-1,1):
                neighRange_row=[i in range(nn.rowRange[0],nn.rowRange[1]+1,1)]
                neighRange_col=[]
                for _ in range(self.sideSize):
                    neighRange_col.append(nn.colRange[1])
            elif n[1]==(0,-1,-1):
                neighRange_row=[self.sideSize-i+1 in range(nn.rowRange[0],nn.rowRange[1]+1,1)]
                neighRange_col=[]
                for _ in range(self.sideSize):
                    neighRange_col.append(nn.colRange[1])

            elif n[1]==(1,0,1):
                neighRange_col=[i in range(nn.colRange[0],nn.colRange[1]+1,1)]
                neighRange_row=[]
                for _ in range(self.sideSize):
                    neighRange_row.append(nn.rowRange[0])
            elif n[1]==(1,0,-1):
                neighRange_col=[self.sideSize-i+1 in range(nn.colRange[0],nn.colRange[1]+1,1)]
                neighRange_row=[]
                for _ in range(self.sideSize):
                    neighRange_row.append(nn.rowRange[0])
            elif n[1]==(-1,0,1):
                neighRange_col=[i in range(nn.colRange[0],nn.colRange[1]+1,1)]
                neighRange_row=[]
                for _ in range(self.sideSize):
                    neighRange_row.append(nn.rowRange[1])
            elif n[1]==(-1,0,-1):
                neighRange_col=[self.sideSize-i+1 in range(nn.colRange[0],nn.colRange[1]+1,1)]
                neighRange_row=[]
                for _ in range(self.sideSize):
                    neighRange_row.append(nn.rowRange[1])

            if n==self.up:
                for iter,i in enumerate(range(self.colRange[0],self.colRange[1]+1,1)):
                    self.upDict[self.rowRange[0],i]=[neighRange_row[iter],neighRange_col[iter]]
            if n==self.down:
                for iter,i in enumerate(range(self.colRange[0],self.colRange[1]+1,1)):
                    self.downDict[self.rowRange[0],i]=[neighRange_row[iter],neighRange_col[iter]]
            elif n==self.left:
                for iter,i in enumerate(range(self.rowRange[0],self.rowRange[1]+1,1)):
                    self.leftDict[self.rowRange[0],i]=[neighRange_row[iter],neighRange_col[iter]]
            elif n==self.right:
                for iter,i in enumerate(range(self.rowRange[0],self.rowRange[1]+1,1)):
                    self.rightDict[self.rowRange[0],i]=[neighRange_row[iter],neighRange_col[iter]]

            facings=[]
            dictList=[self.upDict,self.downDict,self.leftDict,self.rightDict]
            # ori=[self.up,self.down,self.left,self.right]
            for iter,d in enumerate(dictList):
                keys=d.keys()
                dr=[]
                dc=[]
                for r,c in keys:
                    dr.append(r-d[r,c][0])
                    dc.append(c-d[r,c][1])
                if all(dR==dr[0] for dR in dr):
                    if dr[0]>0:
                        facings.append(1)
                    else:
                        facings.append(3)
                elif all(dC==dc[0] for dC in dc):
                    if dc[0]>0:
                        facings.append(2)
                    else:
                        facings.append(0)
                else:
                    drc=[]
                    dcr=[]
                    for r,c in keys:
                        drc.append(r-d[r,c][1])
                        dcr.append(c-d[r,c][0])
                    if all(dRC==drc[0] for dRC in drc):
                        match iter:
                            case 0:
                                if d[keys[0]][0]<d[keys[-1]][0]:
                                    facings.append(0)
                                else:
                                    facings.append(2)
                            case 1:
                                if d[keys[0]][0]<d[keys[-1]][0]:
                                    facings.append(2)
                                else:
                                    facings.append(0)
                            case 2:
                                # facings.append(3)
                                print(iter,' does come here!')
                            case 3:
                                print(iter,' does come here!')
                                # facings.append(3)
                    if all(dCR==dcr[0] for dCR in dcr):
                        match iter:
                                case 0:
                                    # facings.append(3)
                                    print(iter,' does come here!')
                                case 1:
                                    print(iter,' does come here!')
                                case 2:
                                    if d[keys[0]][1]<d[keys[-1]][1]:
                                        facings.append(1)
                                    else:
                                        facings.append(3)
                                case 3:
                                    if d[keys[0]][1]<d[keys[-1]][1]:
                                        facings.append(3)
                                    else:
                                        facings.append(1)

#establish sides for example and input based on shapes
#incorporate side objects when going off current side


# sideSize=4
sideSize=50
mapSideOnRow=maxRow//sideSize
# mapSideOnCol=maxCol//sideSize
sideRangeDict=dict() 
sideRangeDict['top']=[(1,sideSize),(2*sideSize+1,3*sideSize)] #(rowmin,rowmax),(colmin,colmax)
sideRangeDict['front']=[(sideSize+1,2*sideSize),(2*sideSize+1,3*sideSize)]        
sideRangeDict['back']=[(sideSize+1,2*sideSize),(1,sideSize)]
sideRangeDict['bot']=[(2*sideSize+1,3*sideSize),(2*sideSize+1,3*sideSize)]
sideRangeDict['left']=[(sideSize+1,2*sideSize),(sideSize+1,2*sideSize)]
sideRangeDict['right']=[(2*sideSize+1,3*sideSize),(3*sideSize+1,4*sideSize)]
from copy import deepcopy
if mapSideOnRow==4:
    pos=[sideRangeDict['back'][0][1],sideRangeDict['back'][1][0]]
    walls=[[len(board)-p1+1,p0] for p0,p1 in walls] #exchange rows and columns to rotate and then invert the rows to get same orientation as the map in the example
    temp=deepcopy(colBoundaries)
    colBoundaries=deepcopy(rowBoundaries)
    rowBoundaries=temp
    facingIn=2
    currentSide='back'
    pos=np.array([sideRangeDict['back'][0][1],sideRangeDict['back'][1][0]])
else:
    facingIn=3
    currentSide='top'
    pos=np.array([1,[i for i,t in enumerate(board[0]) if t=='.'][0]+1])

#Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
rowOutside=dict()
colOutside=dict()
#((side at lower row values,new direction,(rowCorrection,colCorrection)), (side at higher row values,new direction,(rowCorrection,colCorrection)))
rowOutside['top']=(('back',1),('front',1)) 
rowOutside['front']=(('top',3),('bot',1))
rowOutside['bot']=(('front',3),('back',3))
rowOutside['back']=('top',1),('bot',3)
rowOutside['left']=(('top',0),('bot',0))
rowOutside['right']=(('front',2),('back',0))
#side at lower col values, side at higher col values
colOutside['front']=(('left',2),('right',1)) 
colOutside['left']=(('back',2),('front',0))
colOutside['right']=(('bot',2),('top',2))
colOutside['back']=(('right',3),('left',0))
colOutside['top']=(('left',1),('right',2))
colOutside['bot']=(('left',3),('right',0))

def newOutsidePos(currentSide,underOver,colRow,edgePosition):
    if colRow=='col':
        match currentSide:
            case 'top':
                nextSide,nextFacing=[('left',1),('right',2)][underOver]                
                if nextSide=='left':
                    rowNext=sideRangeDict[nextSide][0][0]
                    colNext=(edgePosition[0]-sideRangeDict['top'][0][0]+1)
                else:
                    rowNext=sideSize-(edgePosition[0]-sideRangeDict['top'][0][0]+1)+sideRangeDict['left'][1][0]
                    colNext=sideRangeDict['right'][0][1]
            case 'front':
                nextSide,nextFacing=[('left',2),('right',1)][underOver]
                if nextSide=='left':
                    rowNext=edgePosition[0]
                    colNext=sideRangeDict['left'][1][1]
                else:
                    rowNext=sideRangeDict['right'][0][0]
                    colNext=sideSize-(edgePosition[0]-sideRangeDict['front'][0][0]+1)+sideRangeDict['right'][1][0]
            case 'bot':
                nextSide,nextFacing=[('left',3),('right',0)][underOver]                
                if nextSide=='left':
                    rowNext=sideRangeDict['left'][0][1]
                    colNext=sideSize-(edgePosition[0]-sideRangeDict['bot'][0][0]+1)+sideRangeDict['left'][1][0]
                else:
                    rowNext=edgePosition[0]
                    colNext=sideRangeDict['right'][1][0]
            case 'back':
                nextSide,nextFacing=[('right',3),('left',0)][underOver]                  
                if nextSide=='right':     
                    rowNext=sideRangeDict['right'][0][1]               
                    colNext=sideSize-(edgePosition[0]-sideRangeDict['back'][0][0]+1)+sideRangeDict['right'][0][0]
                else:
                    rowNext=edgePosition[0]
                    colNext=sideRangeDict['left'][1][0]
            case 'left':
                nextSide,nextFacing=[('back',2),('front',0)][underOver]    
                colNext=sideRangeDict[nextSide][1][0]     
                rowNext=edgePosition[0]         
                if nextSide=='back':     
                    colNext=sideRangeDict['back'][0][1]
                else:
                    colNext=sideRangeDict['front'][0][0]
            case 'right':
                nextSide,nextFacing=[('bot',2),('top',2)][underOver]
                if nextSide=='bot':     
                    rowNext=edgePosition[0]
                    colNext=sideRangeDict['bot'][1][1]
                else:
                    colNext=sideRangeDict['top'][1][1]
                    rowNext=sideSize-(edgePosition[0]-sideRangeDict['right'][0][0]+1)+sideRangeDict['top'][0][0]
    else:
        match currentSide:
            case 'top':
                nextSide,nextFacing=[('back',1),('front',1)][underOver]
                rowNext=sideRangeDict[nextSide][0][0]
                if nextSide=='back':
                    colNext=sideSize-(edgePosition[1]-sideRangeDict['top'][1][0]+1)+sideRangeDict['back'][1][0]
                else:
                    colNext=edgePosition[1]
            case 'front':
                nextSide,nextFacing=[('top',3),('bot',1)][underOver]
                rowNext=sideRangeDict[nextSide][0][0]
                colNext=edgePosition[1]
            case 'bot':
                nextSide,nextFacing=[('front',3),('back',3)][underOver]                
                if nextSide=='back':
                    rowNext=sideRangeDict['back'][0][1]
                    colNext=sideSize-(edgePosition[1]-sideRangeDict['bot'][1][0]+1)+sideRangeDict['back'][1][0]
                else:
                    rowNext=sideRangeDict[nextSide][0][1]
                    colNext=edgePosition[1]
            case 'back':
                nextSide,nextFacing=[('top',1),('bot',3)][underOver]                  
                if nextSide=='top':     
                    rowNext=sideRangeDict[nextSide][0][0]               
                    colNext=sideSize-(edgePosition[1]-sideRangeDict['back'][1][0]+1)+sideRangeDict['top'][1][0]
                else:
                    rowNext=sideRangeDict[nextSide][0][1]
                    colNext=sideSize-(edgePosition[1]-sideRangeDict['back'][1][0]+1)+sideRangeDict['bot'][1][0]
            case 'left':
                nextSide,nextFacing=[('top',0),('bot',0)][underOver]    
                colNext=sideRangeDict[nextSide][1][0]              
                if nextSide=='top':     
                    rowNext=(edgePosition[1]-sideRangeDict['left'][1][0]+1)
                else:
                    rowNext=sideSize-(edgePosition[1]-sideRangeDict['left'][1][0]+1)+sideRangeDict['top'][0][0]
            case 'right':
                nextSide,nextFacing=[('front',2),('back',0)][underOver]
                if nextSide=='back':     
                    rowNext=sideSize-(edgePosition[1]-sideRangeDict['right'][1][0]+1)+sideRangeDict['back'][0][0]
                    colNext=sideRangeDict[nextSide][1][0]
                else:
                    colNext=sideRangeDict[nextSide][1][1]
                    rowNext=sideSize-(edgePosition[1]-sideRangeDict['right'][1][0]+1)+sideRangeDict['front'][0][0]

    return nextSide,nextFacing,rowNext,colNext

# print(sideRangeDict)
# print(maxRow//sideSize,maxCol//sideSize)

def stepAlong(currentSide,facingIn,pos,moveIntent):
    if facingIn==0 or facingIn==2:        
        xyCheck=pos[1]
        hitWallCorrection=np.array([1,0])
        # minBound=colBoundaries[pos[0]][0]
        # maxBound=colBoundaries[pos[0]][1]
        minBound=sideRangeDict[currentSide][1][0]
        maxBound=sideRangeDict[currentSide][1][1]
        wallsOfInterest=np.array([x for y,x in walls if y==pos[0] and minBound<=x<=maxBound])
        xyMin=np.array([pos[0],minBound])
        xyMax=np.array([pos[0],maxBound])
        colRow='col'
    else:        
        xyCheck=pos[0]
        hitWallCorrection=np.array([0,1])
        # minBound=rowBoundaries[pos[1]][0]
        # maxBound=rowBoundaries[pos[1]][1]        
        minBound=sideRangeDict[currentSide][0][0]
        maxBound=sideRangeDict[currentSide][0][1]
        wallsOfInterest=np.array([y for y,x in walls if x==pos[1] and minBound<=y<=maxBound])
        xyMin=np.array([minBound,pos[1]])
        xyMax=np.array([maxBound,pos[1]])
        colRow='row'
    if facingIn==2 or facingIn==3:
        moveIntent*=-1
        hitWallSign=-1
    else:
        hitWallSign=1
    # print(type(wallsOfInterest))
    # maxMove=maxBound+1-minBound
    xyTemp=xyCheck+moveIntent
    # print(move,facingIn,moveDir,moveIntent)
    # print(pos)
    nextSide=currentSide
    nextFacing=facingIn
    if len(wallsOfInterest)==0:
        if minBound<=xyTemp<=maxBound:
            pos=pos+moveIntent*moveDict[facingIn]
        elif xyTemp<minBound:
            moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(xyCheck-minBound))
            if moveIntent==0:
                pos=xyMin
            else:
                nextSide,nextFacing,rowNext,colNext=newOutsidePos(currentSide,0,colRow,xyMin)
                if (rowNext,colNext) in walls:
                    pos=xyMin
                else:
                    pos,nextSide,nextFacing=stepAlong(nextSide,nextFacing,[rowNext,colNext],abs(moveIntent-np.sign(moveIntent)))
        else:
            moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(maxBound-xyCheck))
            if moveIntent==0:
                pos=xyMax
            else:
                nextSide,nextFacing,rowNext,colNext=newOutsidePos(currentSide,1,colRow,xyMax)
                if (rowNext,colNext) in walls:
                    pos=xyMax
                else:
                    pos,nextSide,nextFacing=stepAlong(nextSide,nextFacing,[rowNext,colNext],abs(moveIntent-np.sign(moveIntent)))
                    1
    else:
        posDiff=wallsOfInterest-xyCheck
        if facingIn==2 or facingIn==3:
            prior=[i for i,xyd in enumerate(posDiff) if xyd<0]
            if len(prior)==0:
                closest=wallsOfInterest[-1]
            else:
                closest=wallsOfInterest[prior[-1]]
        else:
            coming=[i for i,xyd in enumerate(posDiff) if xyd>0]
            if len(coming)==0:
                closest=wallsOfInterest[0]
            else:
                closest=wallsOfInterest[coming[0]]
        # closeDiff=xyCheck-closest
        # if np.sign((xyCheck-closest)*(xyTemp-closest))==hitWallSign:
        if np.sign(xyCheck-closest)!=np.sign(xyTemp-closest):
            pos=hitWallCorrection*pos+moveDict[facingIn]*(closest-hitWallSign)
        else:
            if minBound<=xyTemp<=maxBound:
                pos=pos+moveIntent*moveDict[facingIn]
            elif xyTemp<minBound:
                moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(xyCheck-minBound))
                if moveIntent==0:
                    pos=xyMin
                else:
                    nextSide,nextFacing,rowNext,colNext=newOutsidePos(currentSide,0,colRow,xyMin)
                    if (rowNext,colNext) in walls:
                        pos=xyMin
                    else:
                        pos,nextSide,nextFacing=stepAlong(nextSide,nextFacing,[rowNext,colNext],abs(moveIntent-np.sign(moveIntent)))
            else:
                moveIntent=np.sign(moveIntent)*(np.abs(moveIntent)-(maxBound-xyCheck))
                if moveIntent==0:
                    pos=xyMax
                else:
                    nextSide,nextFacing,rowNext,colNext=newOutsidePos(currentSide,1,colRow,xyMax)
                    if (rowNext,colNext) in walls:
                        pos=xyMax
                    else:
                        pos,nextSide,nextFacing=stepAlong(nextSide,nextFacing,[rowNext,colNext],abs(moveIntent-np.sign(moveIntent)))
        
    return pos,nextSide,nextFacing

for move in pathInstr:
    if move[0]=='R':
        facingIn+=1
        if facingIn==4:
            facingIn=0
    else:
        facingIn-=1
        if facingIn==-1:
            facingIn=3
    moveDir=facings[facingIn]
    moveIntent=int(move[1:])
    # print(pos)
    pos,currentSide,facingIn=stepAlong(currentSide,facingIn,pos,moveIntent)


    
print(pos)
facingIn+=1
if facingIn==4:
    facingIn=0
print('2nd: ',1000*pos[1]+4*(200-pos[0]+1)+facingIn) #inverting back rows and columnes to get them in the initial frame