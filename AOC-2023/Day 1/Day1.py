import os
import numpy as np
os.chdir(os.path.dirname(__file__))
with open('input.txt') as f:
    inputStr=f.read()
inputList=inputStr.split('\n')
# inputList=['1abc2','pqr3stu8vwx','a1b2c3d4e5f','treb7uchet']
# inputList=['two1nine','eightwothree','abcone2threexyz','xtwone3four','4nineeightseven2','zoneight234','7pqrstsixteen']
numberStrs=[str(x) for x in range(10)]

#1st problem
digit_sum=0
for row in inputList:
    first_digit=''
    second_digit=''
    for ch in row:
        if ch in numberStrs:
            first_digit=ch
            break
    for ch in row[::-1]:
        if ch in numberStrs:
            second_digit=ch
            break
    if first_digit!='':
        digit_sum+=int(first_digit+second_digit)
print('1st:',digit_sum)

#2nd problem
numberStrs_full=['zero','one','two','three','four','five','six','seven','eight','nine','ten']
digit_sum=0
for row in inputList:
    ins1a_=[]
    ins1b_=[]
    ins2a_=[]
    ins2b_=[]
    if row!='':
        for ns1,ns2 in zip(numberStrs,numberStrs_full):
            try:
                ins1a=row.index(ns1)
                ins1b=row[::-1].index(ns1)
            except:
                ins1a=np.inf
                ins1b=np.inf
            try:
                ins2a=row.index(ns2)
                ins2b=row[::-1].index(ns2[::-1])
            except:
                ins2a=np.inf
                ins2b=np.inf
            ins1a_.append(ins1a)
            ins1b_.append(ins1b)
            ins2a_.append(ins2a)
            ins2b_.append(ins2b)
        if min(ins1a_)<min(ins2a_):
            in1=np.argmin(ins1a_)
        else:
            in1=np.argmin(ins2a_)
        if min(ins1b_)<min(ins2b_):
            in2=np.argmin(ins1b_)
        else:
            in2=np.argmin(ins2b_)
        # in1=min([np.argmin(ins1a_),np.argmin(ins2a_)])
        # in2=min([np.argmin(ins1b_),np.argmin(ins2b_)])
        digit_sum+=int(numberStrs[in1]+numberStrs[in2])
print('2nd :',digit_sum)