import os
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
# fileName='example.txt'
with open(fileName) as f:
    inputStr=f.read().strip()
#for part 1 each workflow was stored by its name (keys) in a dict, each having an associated function, a list of instructions to evaluate and a list of outcomes if true
#each part was also stored as a dict with categories as keys and their values as values
#in the workflow functions, the instructions were evaluated  with eval after having read the part values into variables with the names occurring in the instructions
#the workflow functions return the string for the next workflow to go to or to accept/reject
#an accept (adding the part rating to a total tally) and a reject function (not doing anything) were also introduced, both of these returned None
#the outcomes from the workflow functions were plugged back into the workflow dictionary (also contained accept/reject functions) in a loop, and was iterated until a None was returned

# For part 2, the idea was to work with ranges instead of individual combinations and to add workflows after accepting ranges. 
# These workflows would have conditions to check that value ranges that lie within already accepted value ranges were rejected. 
# It's quite fun and it work, but it's rather slow to solve the actual input ~15 minutes

workflowsStr,ratingsStr=inputStr.split('\n\n')
totalApprovedRating=[0] #total tally of rating, in a list to have access to it inside functions
def accepted(part,toEvaluate,resultIfTrue):
    for id in ['x','m','a','s']:
        totalApprovedRating[0]+=part[id]
    return None
def rejected(part,toEvaluate,resultIfTrue):
    return None
workflowDict=dict()
workflowDict['A']=[accepted,None,None]
workflowDict['R']=[rejected,None,None]
def applyWorkflow(part,toEvaluate,resultIfTrue):
    x=part['x']
    m=part['m']
    a=part['a']
    s=part['s']
    for evalStr,resStr in zip(toEvaluate,resultIfTrue):
        if eval(evalStr):
            return resStr
#populate workflow dict
workflowsList=workflowsStr.split('\n')
for workflow in workflowsList:
    name,rest=workflow.split('{')
    rest=rest[:-1]
    instructionList=rest.split(',')
    toEvaluate=[]
    resultIfTrue=[]
    for indstruction in instructionList:
        instructionParts=indstruction.split(':')
        if len(instructionParts)==1:
            toEvaluate.append("x!='hej'") #dummy instruction/condition (to comply with rest of code) to check for instructions that only had a result
            resultIfTrue.append(instructionParts[0])
        else:
            toEvaluate.append(instructionParts[0])
            resultIfTrue.append(instructionParts[1])
    workflowDict[name]=[applyWorkflow,toEvaluate,resultIfTrue]

for partStr in ratingsStr.split('\n'):
    partDict=dict()
    for rating in partStr.strip('{}').split(','):
        partDict[rating[0]]=int(rating[2:])
    workflowTag='in' #always starting at the workflow called in
    while True:
        workflowFunction,toEvaluate,resultIfTrue=workflowDict[workflowTag]
        workflowTag=workflowFunction(partDict,toEvaluate,resultIfTrue)
        if workflowTag==None:
            break
print('1st:',totalApprovedRating[0])


#part 2
def copyDict(dictIn): #instead of using deepcopy
    newDict=dict()
    for id in ['x','m','a','s']:
        newDict[id]=[value for value in dictIn[id]]
    return newDict

# def recursiveSelection(dictIn,workflowTagIn):
#     if workflowTagIn=='A':
#         combinations=[]
#         for id in ['x','m','a','s']:
#             combinations.append(dictIn[id])
#         return combinations
#     elif workflowTagIn=='R':
#         return []
#     else:
#         workflowFunction,toEvaluate,resultIfTrue=workflowDict[workflowTagIn]
#         # workflowTag=workflowFunction(partDict,toEvaluate,resultIfTrue)
#         rejectedDict=copyDict(dictIn)
#         combinations_approved=[]
#         for evalStr,resStr in zip(toEvaluate,resultIfTrue):
#             eval_category=evalStr[0]
#             approvedValues=[]
#             rejectedValues=[]
#             for value in dictIn[eval_category]:
#                 if eval(str(value)+evalStr[1:]):
#                     approvedValues.append(value)
#                 else:
#                     rejectedValues.append(value)
#             if len(approvedValues)!=0:
#                 approvedDict=copyDict(rejectedDict)
#                 approvedDict[eval_category]=approvedValues
#                 combinations_approved+=recursiveSelection(approvedDict,resStr)
#             if len(rejectedValues)!=0:
#                 rejectedDict[eval_category]=rejectedValues
#             if len(approvedValues)==0:
#                 1
#             if len(rejectedValues)==0:
#                 break
#         return combinations_approved

#creating new workflow dict without any functions, workflows will be added to it while running
workflowDict2=dict()
for workflow in workflowsList:
    name,rest=workflow.split('{')
    rest=rest[:-1]
    instructionList=rest.split(',')
    toEvaluate=[]
    resultIfTrue=[]
    for indstruction in instructionList:
        instructionParts=indstruction.split(':')
        if len(instructionParts)==1:
            toEvaluate.append("x!='hej'")
            resultIfTrue.append(instructionParts[0])
        else:
            toEvaluate.append(instructionParts[0])
            resultIfTrue.append(instructionParts[1])
    workflowDict2[name]=[toEvaluate,resultIfTrue]

workflowDict2['uniquePartStart']=[] #placeholder for the "start point" for only counting uniquecombinations
newWorkFlowCounter=[0] #used to name the new workflows
uniqueCombos=[0] #result
def recursiveSelection(dictIn,workflowTagIn,formerWorkflowTagIn,ie):
    if workflowTagIn=='A!': #new designation for accept of unique combinations
        newWorkFlowTag='WF'+str(newWorkFlowCounter[0]) #naming new workflow
        newWorkFlowCounter[0]+=1
        workflowDict2[formerWorkflowTagIn][1][ie]=newWorkFlowTag #linking the name of the new workflow to the instruction in the previous workflow where it was accepted and came here
        newEvaluateStrs=[]
        newResultStrs=[]        
        for id in ['x','m','a','s']: #creating instructions approve ranges outside of the value ranges that was accepted here, if values are outside then they are accepted if not they are rejected and sent to next instruction
            lower=min(dictIn[id])
            upper=max(dictIn[id])
            evalStr_lower=id+'<'+str(lower)
            evalStr_upper=id+'>'+str(upper)
            newEvaluateStrs.append(evalStr_lower)
            newEvaluateStrs.append(evalStr_upper)
            newResultStrs.append('A!')
            newResultStrs.append('A!')            
        newEvaluateStrs.append("x!='hej'") #adding a dummy instruction that leads to a reject if all prior instructions were rejected =all parameter values were within the already accepted range
        newResultStrs.append('R')            
        workflowDict2[newWorkFlowTag]=[newEvaluateStrs,newResultStrs]
        combos=1
        for id in ['x','m','a','s']:
            combos*=len(dictIn[id])
        uniqueCombos[0]+=combos
        
    elif workflowTagIn=='A':
        if len(workflowDict2['uniquePartStart'])==0: #setting up first workflow to check for unique combinations and linking it to the placeholder
            evaluateStrs=[]
            resultStrs=[]            
            combos=1            
            for id in ['x','m','a','s']:                
                combos*=len(dictIn[id])
                lower=min(dictIn[id])
                upper=max(dictIn[id])
                evalStr_lower=id+'<'+str(lower)
                evalStr_upper=id+'>'+str(upper)
                evaluateStrs.append(evalStr_lower)
                evaluateStrs.append(evalStr_upper)
                resultStrs.append('A!')
                resultStrs.append('A!')
            uniqueCombos[0]+=combos
            evaluateStrs.append("x!='hej'")
            resultStrs.append('R')
            workflowDict2['WF'+str(newWorkFlowCounter[0])]=[evaluateStrs,resultStrs]
            workflowDict2['uniquePartStart']=[["x!='hej'"],['WF'+str(newWorkFlowCounter[0])]]
            newWorkFlowCounter[0]+=1            
            
        else:
            recursiveSelection(dictIn,'uniquePartStart',formerWorkflowTagIn,ie)
    elif workflowTagIn=='R': #rejection does nothing
        pass
        
    else:
        #same idea as in part 1, get instructions to evaluate and where to go if accepted but do evaluation for ranges instead of individual numbers
        toEvaluate,resultIfTrue=workflowDict2[workflowTagIn] 
        rejectedDict=copyDict(dictIn) #the rejected values will keep iterating over multiple instructions, so they are used as reference, accepted will be sent onwards
        
        for ie,(evalStr,resStr) in enumerate(zip(toEvaluate,resultIfTrue)):
            eval_category=evalStr[0]
            approvedValues=[] #storing values that are accepted and rejected in separate lists
            rejectedValues=[]
            for value in rejectedDict[eval_category]:
                if eval(str(value)+evalStr[1:]):
                    approvedValues.append(value)
                else:
                    rejectedValues.append(value)
            if len(approvedValues)!=0:
                approvedDict=copyDict(rejectedDict) #copying reference dict and updating the values to correspond to what was approved
                approvedDict[eval_category]=approvedValues
                recursiveSelection(approvedDict,resStr,workflowTagIn,ie) #sending the approved values to the next workflow in resStr
            if len(rejectedValues)!=0:
                rejectedDict[eval_category]=rejectedValues #updating values in reference dict for next iteration, to remove the values that were accepted above
            if len(rejectedValues)==0: #if there are no rejected values it means that they were all accepted and sent onwards, so stop
                break
    
startDict=dict()
for id in ['x','m','a','s']: #populating start dict with values spanning 1-4000 for all categories
    startDict[id]=[i for i in range(1,4001)]
combinations_approved=recursiveSelection(startDict,'in','',0)
print('2nd:',uniqueCombos[0])

