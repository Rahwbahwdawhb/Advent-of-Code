import os

os.chdir(os.path.dirname(__file__))

file='input.txt'
# file='example.txt'

with open(file) as f:
    ruleStr,updateStr=f.read().strip().split('\n\n')
ruleList=ruleStr.split('\n')
updateList=updateStr.split('\n')

ruleDict={}
for rule in ruleList:
    a,b=rule.split('|')
    ruleDict[(a,b)]=''

midPageSum=0
midPageSum_corrected=0
t=[]
for update in updateList:
    correct=True
    pages=update.split(',')
    ok_pages=[]
    while pages:
        page=pages.pop(0)
        try:
            for page_ in pages:
                ruleDict[(page,page_)]
            ok_pages.append(page)
        except:
            correct=False
            break
    if correct:
        midPageSum+=int(ok_pages[len(ok_pages)//2])
    else:
        pages_0=update.split(',')
        #slow solution, about 100 s to finish overall
        #using topological sorting is much faster
        while True:
            try:
                for i,p in enumerate(pages_0[:-1]):
                    for ii,p_ in enumerate(pages_0[i+1:]):
                        ruleDict[(p,p_)]
                break
            except:
                pages_0=[pages_0[i+1+ii]]+pages_0[:i+1]+pages_0[i+1:i+1+ii]+pages_0[i+1+ii+1:]
        midPageSum_corrected+=int(pages_0[len(pages_0)//2])

print('1st:',midPageSum)
print('2nd:',midPageSum_corrected)