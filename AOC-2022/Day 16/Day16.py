from preload import input
# print(input)

# input=open('ex.txt').read()

inpList=input.strip().split('\n')

#1st problem, took quite some time and effort to figure out how to solve the first one..I was thinking about memoization quite early but wasn't sure how to implement it first, and it wasn't until I realized that I should populate the dictionaries from the "bottom and then up", i.e. starting giving values from 0 to all valves and then up to the final time that things really came together for the first part
class valve():
    def __init__(self,label,neighborNames,rate,valveList):
        self.label=label
        self.neighborNames=neighborNames
        self.valveList=valveList
        self.neighbors=[]
        self.endRelease=0
        self.rate=rate
        self.memoDict=dict()
        self.endOpenValves=''
        self.visited=False
        self.distList=[]
    def findNeighbors(self):
        for valve in self.valveList:
            if valve.label in self.neighborNames:
                self.neighbors.append(valve)
    def distToValves(self):
        for v in self.valveList:
            if v in self.neighbors:
                self.distList.append(1)
            elif v==self:
                self.distList.append(0)
            else:
                goal=v
                current=self
                visitQueue=[]
                currentDist=0
                while current!=goal:
                    for n in current.neighbors:
                        visitQueue.append((n,currentDist+1))
                    next=visitQueue.pop(0)
                    current=next[0]
                    currentDist=next[1]
                self.distList.append(currentDist)
        1
    def newEndRelease(self,accumRelease,minutesLeft,openValves):
        if minutesLeft>=0 and self.label not in openValves:
            newEndRelease=self.rate*(minutesLeft-1)+accumRelease
            if newEndRelease>self.endRelease:
                self.endRelease=newEndRelease
                self.endOpenValves=openValves
                
    # def memoSearch2(self,minutesLeft,openValves,path):
    #     k=self.memoDict.keys()
    #     k2=[(ii,self.memoDict[ii]) for ii in k if ii[0]==minutesLeft]
    #     k2.sort(key=lambda x:x[1][0],reverse=True)
    #     noSuitable=True
    #     for k2i in k2:
    #         if not set(k2i[1][1]) & set(openValves):
    #             noSuitable=False
    #             break
    #     if not noSuitable:
    #         return (self.memoDict[k2i[0]][0],self.memoDict[k2i[0]][1],self.memoDict[k2i[0]][2])
    #     else:
    #         if minutesLeft>0:

    #             outputOpenSelf=[]
    #             outputNotOpenSelf=[]
    #             if self.label not in openValves:
    #                 for n in self.neighbors:
    #                     val_o,openValRec_o,recPath_o=n.memoSearch(minutesLeft-2,sorted(openValves+[self.label]),path+self.label)
    #                     val_no,openValRec_no,recPath_no=n.memoSearch(minutesLeft-1,sorted(openValves),path+self.label)
    #                     outputOpenSelf.append((val_o+self.rate*(minutesLeft-1),openValRec_o,recPath_o)) 
    #                     outputNotOpenSelf.append((val_no,openValRec_no,recPath_no)) 
    #                 outputOpenSelf.sort(key=lambda x:x[0],reverse=True)
    #                 outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
    #                 if outputOpenSelf[0][0]>outputNotOpenSelf[0][0]:
    #                     endContrib=outputOpenSelf[0][0]
    #                     self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
    #                     return (endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
    #                 else:
    #                     self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
    #                     return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
    #             else:
    #                 for n in self.neighbors:
    #                     val_no,openValRec_no,recPath_no=n.memoSearch(minutesLeft-1,sorted(openValves),path+self.label)
    #                     outputNotOpenSelf.append((val_no,openValRec_no,recPath_no)) 
    #                 outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
    #                 self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
    #                 return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
    #         else:
    #             return (0,[],self.label)

    def memoSearch_2(self,minutesLeft,openValves):
        k=self.memoDict.keys()
        if (minutesLeft,''.join(sorted(openValves))) in k:
            return (self.memoDict[(minutesLeft,''.join(openValves))][0],self.memoDict[(minutesLeft,''.join(openValves))][1],self.memoDict[(minutesLeft,''.join(openValves))][3])
        # k2=[(k_e_y,self.memoDict[k_e_y]) for k_e_y in k if k_e_y[0]==minutesLeft]
        # k2.sort(key=lambda x:x[1][0],reverse=True)
        # noSuitable=True
        # # for k2i in k2:
        #     # if len(openValves)!=0 and len(openValves)==len([oValve for oValve in openValves if oValve in k2i[1][1]]):
        #     #     # print(k2i[1][1],openValves)
        #     #     noSuitable=False
        #     #     break
        #     # if set(k2i[1][1]).issubset(openValves):
        #     #     noSuitable=False
        #     #     break
        # for k2i in k2:
        #     if openValves!='' and not set(k2i[1][1]) & set(openValves): #check that openValves does not contain any valve that is opened if following k2i
        #         # if len(k2i[1][1])!=0 and len(openValves)!=0:
        #         #     1
        #         noSuitable=False
        #         break
        # noSuitable=True
        # if not noSuitable:
        #     if (minutesLeft,''.join(sorted(openValves))) not in k:
        #         self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=self.memoDict[k2i[0]]
        #     return (self.memoDict[k2i[0]][0],self.memoDict[k2i[0]][1],self.memoDict[k2i[0]][3])
        else:
            if minutesLeft>1:

                outputOpenSelf=[]
                outputNotOpenSelf=[]
                if self.label not in openValves and self.rate>0:
                    for n in self.neighbors:
                        val_o,openValRec_o,oRef_o=n.memoSearch_2(minutesLeft-2,sorted(openValves+[self.label]))
                        val_no,openValRec_no,oRef_no=n.memoSearch_2(minutesLeft-1,sorted(openValves))
                        outputOpenSelf.append((val_o+self.rate*(minutesLeft-1),openValRec_o,n.label,oRef_o)) 
                        outputNotOpenSelf.append((val_no,openValRec_no,n.label,oRef_no)) 
                    outputOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    if outputOpenSelf[0][0]>outputNotOpenSelf[0][0]:
                        endContrib=outputOpenSelf[0][0]
                        # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
                        # return (endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
                        openRef=[(minutesLeft,self.label)]+outputOpenSelf[0][3]
                        self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1]+[self.label],'open_THEN_'+outputOpenSelf[0][2],openRef)
                        return (endContrib,outputOpenSelf[0][1]+[self.label],openRef)
                    else:
                        # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                        # return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                        openRef=outputNotOpenSelf[0][3]
                        self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],'notopen_THEN_'+outputNotOpenSelf[0][2],openRef)
                        return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],openRef)
                else:
                    for n in self.neighbors:
                        val_no,openValRec_no,oRef_no=n.memoSearch_2(minutesLeft-1,sorted(openValves))
                        outputNotOpenSelf.append((val_no,openValRec_no,n.label,oRef_no)) 
                    outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    openRef=outputNotOpenSelf[0][3]
                    # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                    # return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                    self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],'notopen_THEN_'+outputNotOpenSelf[0][2],openRef)
                    return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],openRef)
            else:
                self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(0,[],'notopen_THEN_stop',[])
                return (0,[],[])

    def memoSearch(self,minutesLeft,openValves):
        k=self.memoDict.keys()
        k2=[(k_e_y,self.memoDict[k_e_y]) for k_e_y in k if k_e_y[0]==minutesLeft]
        k2.sort(key=lambda x:x[1][0],reverse=True)
        noSuitable=True
        # for k2i in k2:
            # if len(openValves)!=0 and len(openValves)==len([oValve for oValve in openValves if oValve in k2i[1][1]]):
            #     # print(k2i[1][1],openValves)
            #     noSuitable=False
            #     break
            # if set(k2i[1][1]).issubset(openValves):
            #     noSuitable=False
            #     break
        for k2i in k2:
            if openValves!='' and not set(k2i[1][1]) & set(openValves): #check that openValves does not contain any valve that is opened if following k2i
                # if len(k2i[1][1])!=0 and len(openValves)!=0:
                #     1
                noSuitable=False
                break
        if not noSuitable:
            if (minutesLeft,''.join(sorted(openValves))) not in k:
                self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=self.memoDict[k2i[0]]
            return (self.memoDict[k2i[0]][0],self.memoDict[k2i[0]][1],self.memoDict[k2i[0]][3])
        else:
            if minutesLeft>1:

                outputOpenSelf=[]
                outputNotOpenSelf=[]
                if self.label not in openValves and self.rate>0:
                    for n in self.neighbors:
                        val_o,openValRec_o,oRef_o=n.memoSearch(minutesLeft-2,sorted(openValves+[self.label]))
                        val_no,openValRec_no,oRef_no=n.memoSearch(minutesLeft-1,sorted(openValves))
                        outputOpenSelf.append((val_o+self.rate*(minutesLeft-1),openValRec_o,n.label,oRef_o)) 
                        outputNotOpenSelf.append((val_no,openValRec_no,n.label,oRef_no)) 
                    outputOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    if outputOpenSelf[0][0]>outputNotOpenSelf[0][0]:
                        endContrib=outputOpenSelf[0][0]
                        # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
                        # return (endContrib,outputOpenSelf[0][1]+[self.label],self.label+outputOpenSelf[0][2])
                        openRef=[(minutesLeft,self.label)]+outputOpenSelf[0][3]
                        self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1]+[self.label],'open_THEN_'+outputOpenSelf[0][2],openRef)
                        return (endContrib,outputOpenSelf[0][1]+[self.label],openRef)
                    else:
                        # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                        # return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                        openRef=outputNotOpenSelf[0][3]
                        self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],'notopen_THEN_'+outputNotOpenSelf[0][2],openRef)
                        return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],openRef)
                else:
                    for n in self.neighbors:
                        val_no,openValRec_no,oRef_no=n.memoSearch(minutesLeft-1,sorted(openValves))
                        outputNotOpenSelf.append((val_no,openValRec_no,n.label,oRef_no)) 
                    outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
                    openRef=outputNotOpenSelf[0][3]
                    # self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                    # return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                    self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],'notopen_THEN_'+outputNotOpenSelf[0][2],openRef)
                    return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],openRef)
            else:
                self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(0,[],'notopen_THEN_stop',[])
                return (0,[],[])

        # if (minutesLeft,''.join(sorted(openValves))) in self.memoDict.keys():
        #     return (self.memoDict[(minutesLeft,''.join(sorted(openValves)))][0],self.memoDict[(minutesLeft,''.join(sorted(openValves)))][1],self.memoDict[(minutesLeft,''.join(sorted(openValves)))][2])
        # else:
        #     if minutesLeft>0:

        #         outputOpenSelf=[]
        #         outputNotOpenSelf=[]
        #         if self.label not in openValves:
        #             for n in self.neighbors:
        #                 val_o,openValRec_o,recPath_o=n.memoSearch(minutesLeft-2,sorted(openValves+[self.label]),path+self.label)
        #                 val_no,openValRec_no,recPath_no=n.memoSearch(minutesLeft-1,sorted(openValves),path+self.label)
        #                 outputOpenSelf.append((val_o+self.rate*(minutesLeft-1),openValRec_o,recPath_o)) 
        #                 outputNotOpenSelf.append((val_no,openValRec_no,recPath_no)) 
        #             outputOpenSelf.sort(key=lambda x:x[0],reverse=True)
        #             outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
        #             if outputOpenSelf[0][0]>outputNotOpenSelf[0][0]:
        #                 endContrib=outputOpenSelf[0][0]
        #                 self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(endContrib,outputOpenSelf[0][1],self.label+outputOpenSelf[0][2])
        #                 return (endContrib,outputOpenSelf[0][1],self.label+outputOpenSelf[0][2])
        #             else:
        #                 self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
        #                 return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
        #         else:
        #             for n in self.neighbors:
        #                 val_no,openValRec_no,recPath_no=n.memoSearch(minutesLeft-1,sorted(openValves),path+self.label)
        #                 outputNotOpenSelf.append((val_no,openValRec_no,recPath_no)) 
        #             outputNotOpenSelf.sort(key=lambda x:x[0],reverse=True)
        #             self.memoDict[(minutesLeft,''.join(sorted(openValves)))]=(outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
        #             return (outputNotOpenSelf[0][0],outputNotOpenSelf[0][1],self.label+outputNotOpenSelf[0][2])
                

        #         if self.label not in openValves and self.rate>0:
        #             openValvesContrib=[self.label]
        #             selfContrib=self.rate*(minutesLeft-1)
        #             minToGo=minutesLeft-2
        #             openedSelf=True
        #         else:
        #             selfContrib=0
        #             openValvesContrib=[]
        #             minToGo=minutesLeft-1
        #             openedSelf=False
        #         outputs=[]
        #         for n in self.neighbors:
        #             # if minToGo==2 and openValves=='BB' and n.label=='AA':
        #             #     1
        #             # val,openValRec,recPath=n.memoSearch(minToGo,sorted(openValves+openValvesContrib),path+self.label)
        #             val,openValRec,recPath=n.memoSearch(minToGo,openValves+openValvesContrib,path+self.label)
        #             # if openValvesContrib+openValves_=='DDDD':
        #             #     1
        #             outputs.append((val,openValRec,recPath)) 
        #         if openedSelf:
        #             for n in self.neighbors:
        #                 val,openValRec,recPath=n.memoSearch(minutesLeft-1,openValves,path+self.label)
        #                 outputs.append((val,openValRec,recPath)) 
        #         outputs.sort(key=lambda x:x[0],reverse=True)
        #         # endContrib=max(outputs)+selfContrib
        #         endContrib=outputs[0][0]+selfContrib
        #         self.memoDict[(minutesLeft,''.join(openValves))]=(endContrib,outputs[0][1],self.label+outputs[0][2])
                
        #         return (endContrib,outputs[0][1],self.label+outputs[0][2])
        #     else:
        #         return (0,openValves+[],self.label)
    def updateNeighbors(self,accumRelease,minutesLeft,openValves):
        timeLeftNextValve=minutesLeft-2
        openValves.append(self)
        for v in self.neighbors:
            v.newEndRelease(self.rate*minutesLeft+accumRelease,timeLeftNextValve,openValves)
        # if timeLeftNextValve>=0:
        #     for v in self.neighbors:
        #         if v!=valveIn:
        #             if v not in openValves:
        #                 openValves.append(v)
        #                 v.newEndRelease(self.rate*minutesLeft+accumRelease,timeLeftNextValve)

valveList=[]
for inp in inpList:
    label=inp[6:8]
    rate=int(inp[inp.find('=')+1:inp.find(';')])
    if inp.find('valves')==-1:
        valves=inp[-2:]
    else:
        valves=inp[inp.find('valves')+7:]
    neighbors=[x[0:2] for x in valves.split(' ')]
    # print(label,rate,neighbors)
    valveList.append(valve(label,neighbors,rate,valveList))

for ii,v in enumerate(valveList):
    v.findNeighbors()
    if v.label=='AA':
        start=v

# for v in valveList:
#     v.distToValves()

# timeLeft=30
# opens=set()
# releaseSum=0
# while timeLeft>0 and len(opens)!=len(valveList):
#     print(current.label,timeLeft)
#     releases=[]
#     for ii,v in enumerate(valveList):
#         releases.append(v.rate*(timeLeft-current.distList[ii]-1))
#     indOpen=releases.index(max(releases))
#     if valveList[indOpen]==current:        
#         if current not in opens:
#             releaseSum+=releases[indOpen]
#         opens.add(current)
#         releases[indOpen]=-1
#         indOpen=releases.index(max(releases))
#         timeLeft-=1
#     timeLeft-=current.distList[indOpen]
#     current=valveList[indOpen]    
    
# print(releaseSum)
totalTime=31
for t in range(totalTime):
    # print(t)
    for v in valveList:
        # endMax,opens,openRefs=v.memoSearch(t,[])
        endMax,opens,openRefs=v.memoSearch_2(t,[])
print('1st:')
print('Pressure release: ',start.memoDict[(totalTime-1,'')][0])
print('open valves: ',sorted(start.memoDict[(totalTime-1,'')][1]))

t=30
v=start
def getPath(v,t,valveList,openStr):
    # openStr=''
    releaseSum=0
    path=''
    while t>1:
        path+=v.label+'->'
        vKeys=v.memoDict.keys()
        openStrSearch=openStr.replace(',','')
        if not (t,openStrSearch) in vKeys:
            # v.memoSearch(t,openStr.split(','))
            v.memoSearch_2(t,openStr.split(','))
        _,_,checkStr,_=v.memoDict[t,openStrSearch]
        openOrNot,nextV=checkStr.split('_THEN_')
        if openOrNot=='open':
            releaseSum+=(t-1)*v.rate
            path+='!'+v.label+'!->'
            t-=2
            if len(openStr)==0:
                openStr=v.label
            else:
                openStr+=','+v.label
                openStr=','.join(sorted(openStr.split(',')))
        else:
            t-=1
        for V in valveList:
            if V.label==nextV:
                v=V
                break
    return path,releaseSum
t=30
path,releaseSum=getPath(start,t,valveList,'')
print('path:',path[0:-2])
print('release sum:',releaseSum)

#2nd part, this was such a rabbit hole with so many different attempts..Occam's razor finally came through :D
#1st realization, that one can search in the valveList with different initially set opened valves to guide the searches
#this lead down a rabbit hole to try out all different combinations...slow and did not manage to set up them all as I only used permutations and did therefore not account for all possible combinations -still that gave me an upper and lower bound to that I could compare my final solution with
#2nd realization, one would naturally go for the closest closed valves with the highest rate so, by checking which valve to go for when omitting the first one that would be opened gave the first valve to be put in a separate list
#with two "starting points" it was "just" a matter of checking the orders that the other valves would be visited after those (while accounting for all opened valves), some comparisons needed to be made in case both search orders would end up at the same valve at the same time -checked which search path that would get the lowest release without it and appended it to that one
#took quite some time and effort before realizing that the order in which one would go for different nodes was to maximize the 
toOpen=[]
for v in valveList:
    if v.rate>0:
        toOpen.append(v.label)

def getNextOpenValve(startValve,T0,valveList,openValves):
    path,_=getPath(startValve,T0,valveList,openValves)    
    if path.find('!')!=-1:
        pathList=path.split('->')
        tOpen=T0
        for v in pathList:
            if v.find('!')!=-1:
                vLabel=v.replace('!','')
                vObjet=[vv for vv in valveList if vv.label==vLabel][0]
                break
            tOpen-=1
    else:
        vLabel=''
        tOpen=0
        vObjet=startValve
    return vLabel,tOpen,vObjet

T0=26
vO1,tO1,valveO1=getNextOpenValve(start,T0,valveList,'')
vO2,tO2,valveO2=getNextOpenValve(start,T0,valveList,vO1)

vL1=[vO1]
vL2=[vO2]
while tO1>0 and tO2>0:
    vOpens=vL1+vL2
    vOpens.sort()
    vO1_,tO1_,valveO1_=getNextOpenValve(valveO1,tO1-1,valveList,','.join(vOpens))
    vO2_,tO2_,valveO2_=getNextOpenValve(valveO2,tO2-1,valveList,','.join(vOpens))
    if vO1_==vO2_:
        if tO1_<tO2_: 
            vL1.append(vO1_)
            tO1=tO1_
            valveO1=valveO1_
            vO2,tO2,valveO2=getNextOpenValve(valveO2,tO2-1,valveList,','.join(vOpens))
            vL2.append(vO2)
        elif tO1_>tO2_:
            vL2.append(vO2_)
            tO2=tO2_
            valveO2=valveO2_
            vO1,tO1,valveO1=getNextOpenValve(valveO1,tO1-1,valveList,','.join(vOpens))
            vL1.append(vO1)
        else: #if tO1==tO2
            vOpens2=vOpens+[vO1_]
            vOpens2.sort()
            _,s1=getPath(valveO1,tO1-1,valveList,','.join(vOpens2))
            _,s2=getPath(valveO2,tO2-1,valveList,','.join(vOpens2))
            if s1>s2:
                vL2.append(vO1_)
                tO2=tO2_
                valveO2=valveO2_
                vO1,tO1,valveO1=getNextOpenValve(valveO1,tO1-1,valveList,','.join(vOpens2))
                vL1.append(vO1)
            else:
                vL1.append(vO2_)
                tO1=tO1_
                valveO1=valveO1_
                vO2,tO2,valveO2=getNextOpenValve(valveO2,tO2-1,valveList,','.join(vOpens2))
                vL2.append(vO2)
            1
    else:
        vL1.append(vO1_)
        vL2.append(vO2_)
        valveO1=valveO1_
        valveO2=valveO2_
        tO1=tO1_
        tO2=tO2_
    # print(vL1)
    # print(vL2)
    # 1

p1,s1=getPath(start,T0,valveList,','.join(sorted(vL2)))
p2,s2=getPath(start,T0,valveList,','.join(sorted(vL1)))
# print(p1)
# print(p2)
# print(s1,s2,s1+s2)
print('2nd: ',s1+s2)
1

# valveList2=[]
# for inp in inpList:
#     label=inp[6:8]
#     rate=int(inp[inp.find('=')+1:inp.find(';')])
#     if inp.find('valves')==-1:
#         valves=inp[-2:]
#     else:
#         valves=inp[inp.find('valves')+7:]
#     neighbors=[x[0:2] for x in valves.split(' ')]
#     # print(label,rate,neighbors)
#     valveList2.append(valve(label,neighbors,rate,valveList2))

# for ii,v in enumerate(valveList2):
#     v.findNeighbors()
#     if v.label=='AA':
#         start=v

# toOpen=[]
# for v in valveList:
#     if v.rate>0:
#         toOpen.append(v.label)
# openCombos=[]
# NtoO=len(toOpen)
# NsplitSizes=NtoO
# for i in range(NsplitSizes):
#     temp=[]
#     if i==0:
#         # for ii in range(NtoO):
#         #     temp.append([[toOpen[ii]],sorted([x for x in toOpen if x!=toOpen[ii]])])
#         for toOpen_ii in toOpen:
#             temp.append([[toOpen_ii],sorted([x for x in toOpen if x!=toOpen_ii])])
#     else:
#         # for ii in range(NtoO):        
#         #     vRef=toOpen[ii]
#         for vRef in toOpen:
#             perms=[x for x in toOpen if x!=vRef]
#             permsEnd0=perms[-1]
#             while True:
#                 toC1=perms[0:i]
#                 temp_=[sorted([vRef]+toC1),sorted(perms[i:])]
#                 perms=perms[1::]+[perms[0]]                
#                 if temp_ not in temp:
#                     temp.append(temp_)
#                 if perms[-1]==permsEnd0:
#                     break
#     openCombos.append(temp)

# totalTime=26
# maxSum=0
# for combos in openCombos:
#     for c1,c2 in combos:
#         endMax1,opens1,openRefs1=start.memoSearch_2(totalTime,c1)
#         endMax2,opens2,openRefs2=start.memoSearch_2(totalTime,c2)
#         tempSum=endMax2+endMax1
#         if tempSum>maxSum:
#             maxSum=tempSum
#             maxCombo=(','.join(c1),','.join(c2))
# print(maxSum)
# print(maxCombo)

# p1=getPath(start,totalTime-1,valveList,maxCombo[0])[0]
# p2=getPath(start,totalTime-1,valveList,maxCombo[1])[0]

# totalTime=26
# maxSum=0
# for combos in openCombos:
#     for c1,c2 in combos:
#         p1,e1=getPath(start,totalTime,valveList,','.join(c1))
#         p2,e2=getPath(start,totalTime,valveList,','.join(c2))
#         tempSum=e1+e2
#         if tempSum>maxSum:
#             maxSum=tempSum
#             maxCombo=(','.join(c1),','.join(c2))
# print(maxSum)
# print(maxCombo)
# p1,p2=maxCombo

# p12=[p1,p2]
# evols=[]
# for p in p12:
#     st=p.split('->')
#     t0=1
#     rS=0
#     rSL=[]
#     for s in st:
#         if s.find('!')!=-1:
#             ss=s[1:-1]
#             for v in valveList:
#                 if v.label==ss:
#                     ssr=v.rate
#                     break
#             rS+=ssr
#         rSL.append([rS,t0])
#         t0+=1
#     evols.append(rSL)
# SS=0
# for i,pa in enumerate(evols[0]):
#     print('t='+str(pa[1]),'r1='+str(pa[0]),'r2='+str(evols[1][i][0]),'r1+r2='+str(pa[0]+evols[1][i][0]))
#     SS+=pa[0]+evols[1][i][0]
# print(SS)

# totalTime=27
# endDict=dict()
# maxSum=0
# for t in range(totalTime):
#     for combos in openCombos:
#         for c1,c2 in combos:
#             for v in valveList2:
#                 endMax1,opens1,openRefs1=v.memoSearch_2(t,c1)
#                 endMax2,opens2,openRefs2=v.memoSearch_2(t,c2)
#                 if t==totalTime-1 and v==start:
#                     maxTemp=endMax1+endMax2
#                     endDict[(','.join(c1),','.join(c2))]=[maxTemp,endMax1,opens1,openRefs1,endMax2,opens2,openRefs2]
#                     if maxTemp>maxSum:
#                         maxSum=maxTemp
#                         maxCombo=(','.join(c1),','.join(c2))

# print(maxSum)
# print(maxCombo)


# from copy import deepcopy

# toOpen=[]
# for v in valveList:
#     if v.rate>0:
#         toOpen.append(v.label)
# # toOpen.sort()
# openCombos=[]
# NtoO=len(toOpen)
# NsplitSizes=NtoO//2
# for i in range(NsplitSizes):
#     temp=[]
#     if i==0:
#         for ii in range(NtoO):
#             temp.append([[toOpen[ii]],sorted([x for x in toOpen if x!=toOpen[ii]])])
#     else:
#         for ii in range(NtoO):
#             vRef=toOpen[ii]
#             perms=[x for x in toOpen if x!=vRef]
#             permsEnd0=perms[-1]
#             while True:
#                 toC1=perms[0:i]
#                 temp_=[sorted([vRef]+toC1),sorted(perms[i:])]
#                 perms=perms[1::]+[perms[0]]                
#                 if temp_ not in temp:
#                     temp.append(temp_)
#                 if perms[-1]==permsEnd0:
#                     break
#     openCombos.append(temp)
# # for combo in openCombos:
# #     print('')
# #     for ccombo in combo:
# #         print(ccombo)

# # totalTime=26
# # maxSum=0
# # for combos in openCombos:
# #     for c1,c2 in combos:
# #         tempList=[]
# #         for v in valveList:
# #             tempList.append(deepcopy(v))
# #             if v.label=='AA':
# #                 startV=v
# #         p1,rs1=getPath(startV,totalTime,tempList,','.join(c1))
# #         p2,rs2=getPath(startV,totalTime,tempList,','.join(c2))
# #         tSum=rs1+rs2
# #         if tSum>maxSum:
# #             maxSum=tSum
# #             maxCombo=(c1,c2)
# #             maxPaths=(p1,p2)
# # print(maxSum)
# # print(maxCombo)
# # print(maxPaths[0])
# # print(maxPaths[1])
# 1


# valveLists=[[],[]]
# for v in valveList:
#     valveLists[0].append(deepcopy(v))
#     valveLists[1].append(deepcopy(v))
# startList=[]
# for vL in valveLists:
#     for vvL in vL:
#         if vvL.label=='AA':
#             startList.append(vvL)
#             break
# totalTime=27
# releaseDict=dict()
# maxSum=0
# for combos in openCombos:
#     for c1,c2 in combos:
#         # for vv in valveLists[0]:
#         #     vv.memoDict.clear()
#         # for vv in valveLists[1]:
#         #     vv.memoDict.clear()
#         # for tInner in range(totalTime):
#         #     for vv in valveLists[0]:
#         #         _,_,_=vv.memoSearch(tInner,c1)
#         #     for vv in valveLists[1]:
#         #         _,_,_=vv.memoSearch(tInner,c2)
#         if c1==['DD', 'EE', 'HH']:
#             1
#         # endMax1,_,_=startList[0].memoSearch(totalTime,c1)
#         # endMax2,_,_=startList[1].memoSearch(totalTime,c2)
#         p1,endMax1=getPath(startList[0],totalTime-1,valveLists[0],','.join(c1))
#         p2,endMax2=getPath(startList[1],totalTime-1,valveLists[1],','.join(c2))
#         releaseDict[''.join(c1)+','+''.join(c2)]=endMax1+endMax2
#         if endMax1+endMax2>maxSum:
#             maxSum=endMax1+endMax2
#             maxCombo=(c1,c2)
# print(releaseDict['DDEEHH,BBCCJJ'])
# print(maxSum)
# print(maxCombo)
# totalTime=26
# print('')
# path,releaseSum=getPath(start,totalTime,valveLists[0],'DD,EE,HH')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# path,releaseSum=getPath(start,totalTime,valveLists[1],'DD,EE,HH')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# path,releaseSum=getPath(start,totalTime,valveLists[0],'BB,CC,JJ')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# path,releaseSum=getPath(start,totalTime,valveLists[1],'BB,CC,JJ')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# print('')
# path,releaseSum=getPath(start,totalTime,valveList,'BB,CC,JJ')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# path,releaseSum=getPath(start,totalTime,valveList,'DD,EE,HH')
# print('path:',path[0:-2])
# print('release sum:',releaseSum)
# 1

# #testa söka från andra håll i lista...problem kanske att får nya referensvärden i dict som använder då gör vissa sökningar, dock skumt att de ger sämre ...

# # for i in range(len(toOpen)-1):
# #     openCombos.append([toOpen[0:i+1],toOpen[i+1:]])
# # refCombos=deepcopy(openCombos)
# # for _ in range(len(toOpen)-1):
# #     for i,combo in enumerate(refCombos):
# #         c1=combo[0]
# #         c2=combo[1]
# #         if len(c1)==1:
# #             newCombo=[[c2[0]],c2[1:]+[c1[0]]]
# #         elif len(c2)==1:
# #             newCombo=[c1[1:]+[c2[0]],[c1[0]]]
# #         else:
# #             newCombo=[c1[1:]+[c2[0]],c2[1:]+[c1[0]]]        
# #         openCombos.append(newCombo)
# #         refCombos[i]=newCombo

# # # for combo in openCombos:
# # #     print(combo)

# # sortedUniqueCombos=[]
# # for c1,c2 in openCombos:
# #     temp=[sorted(c1),sorted(c2)]
# #     if temp[1][0]<temp[0][0]:
# #         temp=[temp[1],temp[0]]
# #     if temp not in sortedUniqueCombos:
# #         sortedUniqueCombos.append(temp)
# # # print('')
# # # for combo in sortedUniqueCombos:
# # #     print(combo)

# # totalTime=27
# # releaseDict=dict()
# # maxSum=0
# # for c1,c2 in sortedUniqueCombos:
# #     endMax1,_,_=start.memoSearch(totalTime,c1)
# #     endMax2,_,_=start.memoSearch(totalTime,c2)
# #     releaseDict[''.join(c1)+','+''.join(c2)]=endMax1+endMax2
# #     maxSum=max([maxSum,endMax1+endMax2])
# # # print(releaseDict)
# # print(maxSum)


# t=26
# tLeft=[t,t]
# openStrList=['','']
# valveLists=[[],[]]
# goingForList=['','']
# isOpening=[False,False]
# for v in valveList:
#     valveLists[0].append(deepcopy(v))
#     valveLists[1].append(deepcopy(v))
# vList=[]
# for vL in valveLists:
#     for vvL in vL:
#         if vvL.label=='AA':
#             vList.append(vvL)
#             break
# releaseSum=0
# pathList=['','']
# while t>0:
#     for it,v in enumerate(vList):
#         pathList[it]+=v.label+'->'
#         vKeys=[vK for vK in v.memoDict.keys() if vK[0]==tLeft[it]]
#         # vKeys=[(vK,v.memoDict[vK][0]) for vK in v.memoDict.keys() if vK[0]==tLeft[it]]
#         openStrSearch=openStrList[it].replace(',','')
#         if not (t,openStrSearch) in vKeys:
#             v.memoSearch(t,openStrList[it].split(','))
#         _,_,checkStr,openRefs=v.memoDict[t,openStrSearch]
#         openOrNot,nextV=checkStr.split('_THEN_')      
        
#         if openOrNot=='open':
#             if not isOpening[it]:
#                 nextV=v.label
#                 isOpening[it]=True
#             else:
#                 isOpening[it]=False
#                 releaseSum+=t*v.rate

#                 if len(openStrList[it])==0:
#                     openStrList[it]=v.label
#                 else:
#                     newOpenStr=openStrList[it]+','+v.label
#                     openStrList[it]=','.join(sorted(newOpenStr.split(',')))

#                 openStrSearch=openStrList[it].replace(',','')
#                 if not (t,openStrSearch) in vKeys:
#                     v.memoSearch(t,openStrList[it].split(','))
#                 _,_,checkStr,openRefs=v.memoDict[t,openStrSearch]
#                 openOrNot,nextV=checkStr.split('_THEN_')      

#                 openRefsSort=sorted(openRefs,key=lambda x:x[0],reverse=True)
#                 if len(openRefsSort)!=0:
#                     goingFor=openRefsSort[0][1]
#                     goingForList[it]=goingFor
#                     if it==0:
#                         if len(openStrList[1])==0:
#                             openStrList[1]=goingFor
#                         else:
#                             newOpenStr=openStrList[1]+','+goingFor
#                             openStrList[1]=','.join(sorted(newOpenStr.split(',')))
#                         # for vv in valveLists[1]:
#                         #     vv.memoDict.clear()
#                         # for tInner in range(t):
#                         #     for vv in valveLists[1]:
#                         #         _,_,_=vv.memoSearch(tInner,openStrList[1].split(','))
#                     else:
#                         if len(openStrList[0])==0:
#                             openStrList[0]=goingFor
#                         else:
#                             newOpenStr=openStrList[0]+','+goingFor
#                             openStrList[0]=','.join(sorted(newOpenStr.split(',')))
#                         # for vv in valveLists[0]:
#                         #     vv.memoDict.clear()
#                         # for tInner in range(t):
#                         #     for vv in valveLists[0]:
#                         #         _,_,_=vv.memoSearch(tInner,openStrList[0].split(','))
#         else:
#             if len(goingForList[it])==0:
#                 openRefsSort=sorted(openRefs,key=lambda x:x[0],reverse=True)
#                 goingFor=openRefsSort[0][1]
#                 goingForList[it]=goingFor
#                 if it==0:
#                     if len(openStrList[1])==0:
#                         openStrList[1]=goingFor
#                     else:
#                         newOpenStr=openStrList[1]+','+goingFor
#                         openStrList[1]=','.join(sorted(newOpenStr.split(',')))
#                     for vv in valveLists[1]:
#                         vv.memoDict.clear()
#                     for tInner in range(t):
#                         for vv in valveLists[1]:
#                             _,_,_=vv.memoSearch(tInner,openStrList[1].split(','))
#                 else:
#                     if len(openStrList[0])==0:
#                         openStrList[0]=goingFor
#                     else:
#                         newOpenStr=openStrList[0]+','+goingFor
#                         openStrList[0]=','.join(sorted(newOpenStr.split(',')))
#                     # for vv in valveLists[0]:
#                     #     vv.memoDict.clear()
#                     # for tInner in range(t):
#                     #     for vv in valveLists[0]:
#                     #         _,_,_=vv.memoSearch(tInner,openStrList[0].split(','))

#         for V in valveLists[it]:
#             if V.label==nextV:
#                 vList[it]=V
#                 break
#     t-=1


#     #     if tLeft[it]==t:
#     #         pathList[it]+=v.label+'->'
#     #         vKeys=[vK for vK in v.memoDict.keys() if vK[0]==tLeft[it]]
#     #         # vKeys=[(vK,v.memoDict[vK][0]) for vK in v.memoDict.keys() if vK[0]==tLeft[it]]
#     #         openStrSearch=openStrList[it].replace(',','')
#     #         if not (t,openStrSearch) in vKeys:
#     #             v.memoSearch(t,openStrList[it].split(','))
#     #         _,_,checkStr,openRefs=v.memoDict[t,openStrSearch]
#     #         openOrNot,nextV=checkStr.split('_THEN_')           
#     #         if goingForList[it]=='':
#     #             openRefsSort=sorted(openRefs,key=lambda x:x[0],reverse=True)
#     #             goingFor=openRefsSort[0][1]
#     #             goingForList[it]=goingFor
#     #             if it==0:
#     #                 if len(openStrList[1])==0:
#     #                     openStrList[1]=goingFor
#     #                 else:
#     #                     newOpenStr=openStrList[1]+','+goingFor
#     #                     openStrList[1]=','.join(sorted(newOpenStr.split(',')))
#     #             else:
#     #                 if len(openStrList[0])==0:
#     #                     openStrList[0]=goingFor
#     #                 else:
#     #                     newOpenStr=openStrList[0]+','+goingFor
#     #                     openStrList[0]=','.join(sorted(newOpenStr.split(',')))
#     #         #     1
#     #         # if len(openRefs)!=0:
#     #         #     openRefsSort=sorted(openRefs,key=lambda x:x[0])
#     #         #     goingFor=openRefsSort[0][1]
#     #         #     if it==0:
#     #         #         if len(openStrList[1])==0:
#     #         #             openStrList[1]=goingFor
#     #         #         else:
#     #         #             if goingFor not in openStrList[1]:
#     #         #                 newOpenStr=openStrList[1]+','+goingFor
#     #         #                 openStrList[1]=','.join(sorted(newOpenStr.split(',')))
#     #         #                 # for vv in valveLists[1]:
#     #         #                 #     vv.memoDict.clear()
#     #         #                 # for tInner in range(t):
#     #         #                 #     for vv in valveLists[1]:
#     #         #                 #         _,_,_=vv.memoSearch(tInner,openStrList[1].split(','))
#     #         #     else:
#     #         #         if len(openStrList[0])==0:
#     #         #             openStrList[0]=goingFor
#     #         #         else:
#     #         #             if goingFor not in openStrList[0]:
#     #         #                 newOpenStr=openStrList[0]+','+goingFor
#     #         #                 openStrList[0]=','.join(sorted(newOpenStr.split(',')))
#     #         #                 # for vv in valveLists[0]:
#     #         #                 #     vv.memoDict.clear()
#     #         #                 # for tInner in range(t):
#     #         #                 #     for vv in valveLists[0]:
#     #         #                 #         _,_,_=vv.memoSearch(tInner,openStrList[0].split(','))


#     #         if openOrNot=='open':
#     #             releaseSum+=(tLeft[it]-1)*v.rate
#     #             tLeft[it]-=2
#     #             goingForList[it]=''
#     #             # for iiii in range(2):
#     #             #     if len(openStrList[iiii])==0:
#     #             #         openStrList[iiii]=v.label
#     #             #     else:
#     #             #         newOpenStr=openStrList[iiii]+','+v.label
#     #             #         openStrList[iiii]=','.join(sorted(newOpenStr.split(',')))
#     #             # for iiii in range(2):
#     #             #     for vv in valveLists[iiii]:
#     #             #         vv.memoDict.clear()
#     #             # for iiii in range(2):
#     #             #     for tInner in range(t):
#     #             #         for vv in valveLists[iiii]:
#     #             #             _,_,_=vv.memoSearch(tInner,openStrList[iiii].split(','))
#     #             # if it==0:
#     #             #     1
#     #             # else:
#     #             #     1
#     #         else:
#     #             tLeft[it]-=1
            
#     #         for V in valveLists[it]:
#     #             if V.label==nextV:
#     #                 vList[it]=V
#     #                 break
#     # t-=1
# print(releaseSum)
# for pt in pathList:
#     print(pt)
# print(openStrList)
# # 2nd part
# class partyEffort:
#     def __init__(self,valveList):
#         self.valveList=valveList
#         self.posDict=dict()
#     def scatter(self,timeIn):
#         for t in range(timeIn):
#             for iter1,v1 in enumerate(self.valveList):
#                 for iter2,v2 in enumerate(self.valveList):
#                     if t==0:
#                         posDict[(t,iter1,iter2)]=0
#                         return 0
#                     if not (t,iter1,iter2) in self.posDict.keys():
#                         endMax1,opens1,path1=v1.memoSearch(t,[],'')
#                         endMax2,opens2,path2=v2.memoSearch(t,opens1,'')
#                         posDict[(t,iter1,iter2)]=endMax1+endMax2
#                         return endMax1+endMax2
#                     else:
#                         return self.posDict[(t,iter1,iter2)]


# totalTime=27
# posDict=dict()
# for t in range(totalTime):
#     for iter1,v1 in enumerate(valveList):
#         for iter2,v2 in enumerate(valveList):
#             if not (t,iter1,iter2) in posDict.keys():
#                 endMax1,opens1,path1=v1.memoSearch(t,[],'')
#                 endMax2,opens2,path2=v2.memoSearch(t,opens1,'')
#                 posDict[(t,iter1,iter2)]=endMax1+endMax2
# for iter,v in enumerate(valveList):
#     if v==start:
#         startPos=iter
# print(posDict[(totalTime-1,startPos,startPos)])

# valveList=[]
# for inp in inpList:
#     label=inp[6:8]
#     rate=int(inp[inp.find('=')+1:inp.find(';')])
#     if inp.find('valves')==-1:
#         valves=inp[-2:]
#     else:
#         valves=inp[inp.find('valves')+7:]
#     neighbors=[x[0:2] for x in valves.split(' ')]
#     # print(label,rate,neighbors)
#     valveList.append(valve(label,neighbors,rate,valveList))

# for ii,v in enumerate(valveList):
#     v.findNeighbors()
#     if v.label=='AA':
#         start=v
# totalTime=31
# for t in range(totalTime):
#     # print(t)
#     for v in valveList:
#         endMax,opens,path=v.memoSearch(t,[],'')
#         endMax,opens,path=v.memoSearch(t,opens,'')
# print('2nd:')
# print('Pressure release: ',start.memoDict[(totalTime-1,'')][0])


# Nvalves=len(valveList)
# Nupdated=1
# while Nupdated!=0:
#     Nupdated=0
#     vCurrent=valveList[0]
#     vCurrent.visited=True
#     Nvisited=1
#     timeLeft=30
#     openValves=''
#     toVisit=[]
#     toVisitSet=set()
#     while timeLeft>1:    
#         for n in vCurrent.neighbors:
#             if vCurrent.label not in n.endOpenValves and vCurrent.rate>0:
#                 timeToDeduct=2
#             else:
#                 timeToDeduct=1
#             nCer=n.endRelease
#             n.newEndRelease(vCurrent.endRelease,timeLeft-1,vCurrent.endOpenValves+vCurrent.label)
#             if n not in toVisitSet:
#                 toVisit.append([n,timeLeft-timeToDeduct])
#                 toVisitSet.add(n)
#             if nCer!=n.endRelease:
#                 Nupdated+=1
#         if len(toVisit)!=0:
#             popped=toVisit.pop(0)
#             vCurrent=popped[0]
#             toVisitSet.remove(vCurrent)
#             vCurrent.visited=True
#             Nvisited+=1
#             timeLeft=popped[1]
#     print(Nupdated)
# releases=[]
# for v in valveList:
#     releases.append(v.endRelease)
#     print('')
#     print(v.endRelease)
#     print(v.endOpenValves+v.label)
# print('1st: ',max(releases))
# val,opens=valveList[0].memoSearch(30,'')
# print(opens)
# print(val)
# for v in valveList:
#     print(v.endRelease)

# from copy import deepcopy
# timeLeft=30
# toCheck=[(valveList[0],[])]
# while timeLeft>=0 and len(toCheck)!=0:
#     toCheckNext=[]
#     while len(toCheck)!=0:
#         current=toCheck.pop(0)
#         openValves=current[1]
#         current[0].updateNeighbors(current[0].endRelease,timeLeft,openValves)
#         for v in current[0].neighbors:
#             toCheckNext.append((v,deepcopy(openValves)))
#     toCheck=deepcopy(toCheckNext)
#     timeLeft-=1

#2nd problem

