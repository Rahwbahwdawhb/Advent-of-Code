from preload import input
import numpy as np
# print(input)

# input='2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8'

#1st problem

inpList=input.split('\n')
containedSum=0
sectionsCovered=[]
for row in inpList:
    if len(row)>0:
        sec1,sec2=row.split(',')
        s1a,s1b=sec1.split('-')
        s2a,s2b=sec2.split('-')
        secs=list(range(int(s1a),int(s1b)+1))+list(range(int(s2a),int(s2b)+1))
        sectionsCovered.append(np.unique(secs))
        
        if int(s1a)>=int(s2a) and int(s1b)<=int(s2b):
            containedSum+=1
        elif int(s1a)<=int(s2a) and int(s1b)>=int(s2b):
            containedSum+=1
        # print(sec1,':',sec2)
print('1st: ',containedSum)

#2nd problem
overlapSum=0
for row in inpList:
    if len(row)>0:
        sec1,sec2=row.split(',')
        s1a,s1b=sec1.split('-')
        s2a,s2b=sec2.split('-')
        
        secs1=list(range(int(s1a),int(s1b)+1))
        secs2=list(range(int(s2a),int(s2b)+1))

        for sec in secs1:
            if sec in secs2:
                overlapSum+=1
                break
print('2nd: ',overlapSum)

#misread 2nd problem and wasted time on wild goose chase, thought one had to find how many elf-pairs that had some overlapping section with any other elf pair and add those together, those efforts are below:
# overlapPairs=set()
# iter1=0
# # sectionsCovered2=sectionsCovered.copy()
# for secs in sectionsCovered:
#     # sectionsCovered2=sectionsCovered.copy() #find all unique overlapping elf-pairs
#     for sec in secs:        
#         iter2=0
#         sectionsCovered2=sectionsCovered.copy()
#         delIns=[]
#         while len(sectionsCovered2)>0:
#             if sec in sectionsCovered2[0] and iter1!=iter2:
#                 overlapPairs.add((min([iter1,iter2]),max([iter1,iter2])))
#                 delIns.append(iter2)
#             del sectionsCovered2[0]            
#             iter2+=1
#         for ind in sorted(delIns,reverse=True):
#             del sectionsCovered[ind]
#     iter1+=1
# print(len(overlapPairs))
# # print(overlapPairs)

