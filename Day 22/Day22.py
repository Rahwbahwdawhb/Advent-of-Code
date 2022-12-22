from preload import input
import numpy as np

input=open('ex.txt').read()
# print(input)
boardStr,pathStr=input.split('\n\n')
# print(boardStr,pathStr)


#1st problem
board=[]
walls=[]
for rowIn,row in enumerate(boardStr.split('\n')):
    temp=[]
    for colIn,tile in enumerate(row):
        if tile=='#':
            walls.append((rowIn+1,colIn+1))
        temp.append(tile)
    board.append(temp)
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
print(pathInstr)
# print(path)
# print(walls)
maxCol=len(board[0])
maxRow=len(board)
pos=(1,[i for i,t in enumerate(board[0]) if t=='.'][0]+1)
#Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
facings=[0,1,2,3] 
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
    if moveDir==0 or moveDir==2:
        wallsOnCols=[x for y,x in walls if y==pos[0]]
        wallsOnCols=np.array(wallsOnCols) #wallsOnCols should be sorted when it's set up given order that walls is added to
        posTemp=pos[1]+moveIntent
        diffs=posTemp-wallsOnCols
        if moveDir==0:
            indPast=np.argmax(diffs>0)
            if indPast==0 and diffs[0]<=0: #no walls are hit
                if posTemp<=maxCol:
                    stopX=posTemp
                else:
                    if wallsOnCols[0]==1:
                        stopX=maxCol
                    else:
                        moveIntent-=maxCol-pos[1]+1
                        posTemp=1+moveIntent
                        if posTemp-wallsOnCols[0]>=0:
                            stopX=wallsOnCols[0]-1
                        else:
                            if posTemp>maxCol:
                                moveIntent=moveIntent%maxCol+1
                                stopX=1+moveIntent
                            else:
                                stopX=posTemp
            else: #some wall is hit
                stopX=wallsOnCols[indPast]-1
        else:
            indPast=np.argmin(diffs<0)
            if indPast==0 and diffs[0]<=0: #all walls are hit
                stopX=wallsOnCols[-1]+1
            else:
                if posTemp>=1:
                    stopX=wallsOnCols[indPast]+1
                else:
                    if wallsOnCols[-1]==maxCol:
                        stopX=1
                    else:
                        moveIntent-=pos[1]-1+1
                        posTemp=maxCol+moveIntent
                        if posTemp-wallsOnCols[-1]<=0:
                            stopX=wallsOnCols[-1]+1
                        else:
                            if posTemp<1:
                                moveIntent=moveIntent%maxCol+1
                                stopX=maxCol-moveIntent
                            else:
                                stopX=posTemp
        pos[1]=stopX
    # print(moveDir,moveIntent)
    1

#2nd problem

