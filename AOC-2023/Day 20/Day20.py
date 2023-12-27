import os
import numpy as np
import heapq
import networkx as nx
from pyvis.network import Network

os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
# fileName='example2.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
inputStrList=inputStr.split('\n')

#idea: use classes for each of the module types and provide each with a function to send pulses that return a low or a high pulse
#the send pulse functions return a tuple (timeReceived,destinationModuleName,self.name,pulseToSend) that is sent to a heap which sorts pulses according to timeReceived
#a loop is created that pops the first element from the heap and sends the pulseToSend to the destinationModuleName along with the timeReceived and self.name=name of module sending the pulse (needed for conjunctions)
#in part 1 this is repeated 1000 times and then the number of sent pulses are used to calculate the answer
#in part 2 this is iterated until finding some reference values to calculate the answer, see comments below

class broadcaster:
    def __init__(self,broadCastStr):
        self.pulseReceived=0
        self.name='broadcaster'
        self.destinationModuleNames=[]
        for destinationModuleStr in broadCastStr.split(','):            
            self.destinationModuleNames.append(destinationModuleStr.strip(' '))
    def reset(self):
        self.pulseReceived=0
    def sendFirstPulse(self,timeReceived):
        self.pulseReceived=-1
        return [(timeReceived+1,destinationModuleName,self.name,-1) for destinationModuleName in self.destinationModuleNames]
class flipflop:
    def __init__(self,name,destinationModulesStr):
        self.pulseReceived=0
        self.name=name
        self.on=False #start in off state
        self.destinationModuleNames=[]
        for destinationModuleStr in destinationModulesStr.split(','):   
            self.destinationModuleNames.append(destinationModuleStr.strip(' '))
        self.numberOfDestinationModules=len(self.destinationModuleNames)
    def reset(self):
        self.pulseReceived=0
        self.on=False
    def sendPulse(self,sender,pulseReceived,timeReceived):
        self.pulseReceived=pulseReceived
        if pulseReceived==-1:
            if self.on:
                self.on=False
                pulseToSend=-1
            else:
                self.on=True
                pulseToSend=1
            return [(timeReceived+1,destinationModuleName,self.name,pulseToSend) for destinationModuleName in self.destinationModuleNames]
        else:
            return []
class conjunction:
    def __init__(self,name,destinationModulesStr):
        self.name=name
        self.destinationModuleNames=[]
        self.pulseReceived=0
        for destinationModuleStr in destinationModulesStr.split(','):   
            self.destinationModuleNames.append(destinationModuleStr.strip(' '))
    def findInputModules(self,moduleDict):
        self.inputModuleDict=dict()
        i=0
        for item in moduleDict.items(): #go through all modules in dict and check if this one's name is in any of their destinations
            if self.name in item[1].destinationModuleNames:
                self.inputModuleDict[item[1].name]=i
                i+=1
        self.memoryLength=i
        self.memorySlots=np.zeros(self.memoryLength)-1 #memory holder for last received pulses from the input modules
    def reset(self):
        self.memorySlots=np.zeros(self.memoryLength)-1
        self.pulseReceived=0
    def sendPulse(self,sender,pulseReceived,timeReceived):
        self.pulseReceived=pulseReceived
        senderIndex=self.inputModuleDict[sender]
        self.memorySlots[senderIndex]=pulseReceived
        if np.sum(self.memorySlots)==self.memoryLength:
            pulseToSend=-1
        else:
            pulseToSend=1
        return [(timeReceived+1,destinationModuleName,self.name,pulseToSend) for destinationModuleName in self.destinationModuleNames]

allModuleList=[]
conjunctionList=[]
rx_connection='' #placeholder for reference node to part 2
moduleDict=dict() #stores the module objects, their names are the keys
adjacencyList=dict() #used to draw graph
for row in inputStrList:
    modulePart,destinationPart=row.split(' -> ')    
    if modulePart=='broadcaster':
        moduleName=modulePart
        moduleType=broadcaster(destinationPart)
    else:
        moduleName=modulePart[1:]
        if modulePart[0]=='%':
            moduleType=flipflop(moduleName,destinationPart)
        elif modulePart[0]=='&':
            moduleType=conjunction(moduleName,destinationPart)
            conjunctionList.append(moduleType)
    moduleDict[moduleName]=moduleType
    allModuleList.append(moduleType)
    adjacencyList[moduleName]=[d.strip(' ') for d in destinationPart.split(',')]
    if 'rx' in destinationPart:
        rx_connection=moduleName

#find modules that give the inputs to the conjunctions
for c in conjunctionList:
    c.findInputModules(moduleDict)

def drawGraph(valueDict): #function that draws the graph, very helpful to make sense of part 2
    G = nx.DiGraph()
    for key in adjacencyList.keys():
        G.add_node(key,label=valueDict[key])
    for key in adjacencyList.keys():
        for tag in adjacencyList[key]:
            G.add_edge(key,tag)
    # G = nx.DiGraph(adjacencyList)
    nt = Network('500px', '500px',directed=True)
    nt.from_nx(G)
    nt.show('nx.html',notebook=False)

def broadcastPulses():
    firstPulses=moduleDict['broadcaster'].sendFirstPulse(-1)
    pulseQueue=[]
    for pulse in firstPulses:
        pulseQueue.append(pulse)
    heapq.heapify(pulseQueue)
    lowPulses=1
    highPulses=0
    broadcastStr=''
    while len(pulseQueue)!=0:
        timeSent,receiver,sender,pulseToSend=pulseQueue.pop(0)
        if pulseToSend==-1:
            pulseStr='low'
            lowPulses+=1
        else:
            pulseStr='high'
            highPulses+=1
        # broadcastStr+=str(timeSent)+','+sender+' -'+pulseStr+'-> '+receiver+'\n'
        try:
            pulseList=moduleDict[receiver].sendPulse(sender,pulseToSend,timeSent)
        except:
            pulseList=[]        
        for pulse in pulseList:
            heapq.heappush(pulseQueue,pulse)
        if receiver in ['hh','fn','fh','lk']:
            broadcastStr+=receiver+':'+pulseStr+','
        # broadcastStr+='conjunctionMemories: '
        # for c in conjunctionList:
        #     broadcastStr+=str(c.memorySlots)
        # broadcastStr+='\nlowPules='+str(lowPulses)+',highPulses='+str(highPulses)
        # broadcastStr=str(moduleDict['nc'].memorySlots)

        valueDict=dict()
    for key in moduleDict.keys():
        valueDict[key]=str(moduleDict[key].pulseReceived)
    return broadcastStr,lowPulses,highPulses,valueDict

# part 1
lowPulsesList=[]
highPulsesList=[]
for _ in range(1000):
    _,lowPulses,highPulses,_=broadcastPulses()
    lowPulsesList.append(lowPulses)
    highPulsesList.append(highPulses)
print('1st:',sum(lowPulsesList)*sum(highPulsesList))


#from inspecting the input, by plotting its graph with the stuff below, it was seen that the node connected to the rx output was itself connected to four flipflops (making it a conjunction)
# G = nx.DiGraph(adjacencyList)
# nt = Network('500px', '500px',directed=True)
# nt.from_nx(G)
# nt.show('nx_ref.html',notebook=False)
#in order for the conjunction connected to the rx output to send a low pulse, it had to receive four high pulses simultaneously, the four ingoing flipflops had to be in sync and all send high pulses
#looking at the iterations when the four flipflops were sent low signals (causing them to flip), it was seen that this had a periodicity -multiples of the first iteration it happend
#as the periods were different, they need to be multiplied for them to give the number of iterations for them to occur at the same time
#also, since the flipflops need to switch from on to off to send high pulses, and since they start off it means that they need to have been flipped an odd number of times
#this turned out to be the case directly when multiplying the periods otherwise multipliers of the "overall period" would have to been checked

#part 2
for module in allModuleList:
    module.reset()
finalFlipflops=dict()
finalFlipflops_number=0
for key in moduleDict.keys():
    if rx_connection in moduleDict[key].destinationModuleNames:
        finalFlipflops[key]=0
        finalFlipflops_number+=1

identifiedFinalFlipFlops=set()
iter=0
while len(identifiedFinalFlipFlops)!=finalFlipflops_number:
    iter+=1
    # print(iter)
    broadcastStr,lowPulses,highPulses,valueDict=broadcastPulses()
    # drawGraph(valueDict)
    # print(iter,broadcastStr)
    if 'low' in broadcastStr:
        for flipflopPulse in broadcastStr.split(','):
            if 'low' in flipflopPulse:
                flipflopName=flipflopPulse.split(':')[0]
                identifiedFinalFlipFlops.add(flipflopName)
                if finalFlipflops[flipflopName]==0:
                    finalFlipflops[flipflopName]=iter
totalIterations=1
for key in finalFlipflops.keys():
    totalIterations*=finalFlipflops[key]
print('2nd:',totalIterations)

    

