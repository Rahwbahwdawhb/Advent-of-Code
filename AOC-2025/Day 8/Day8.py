import os
import bisect
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    junction_list_1=f.read().strip().split('\n')

junction_list=[]
for junction in junction_list_1:
    junction_list.append(tuple(int(pos) for pos in junction.split(',')))

def distance(j1,j2):
    d=0
    for j1_,j2_ in zip(j1,j2):
        d+=(j1_-j2_)**2
    return d

junction_pairs=[]
prior_pairs=set()
enough=False
for j1 in junction_list:
    for j2 in junction_list:
        if j1!=j2 and (j2,j1) not in prior_pairs:
            prior_pairs.add((j1,j2))
            d=distance(j1,j2)
            bisect.insort(junction_pairs,(d,j1,j2))
limit=1000 #change to 10 for the example
count=0
circuits=[]
N_junctions=len(junction_list)
#a bit slow but works
while True:
    d,j1,j2=junction_pairs.pop(0)
    j1_in=-1
    j2_in=-1
    for i,c in enumerate(circuits):
        if j1 in c:
            j1_in=i
        if j2 in c:
            j2_in=i
    if j1_in==-1 and j2_in==-1:
        circuits.append({j1,j2})
    elif j1_in!=-1 and j2_in==-1:
        circuits[j1_in].add(j2)
    elif j1_in==-1 and j2_in!=-1:
        circuits[j2_in].add(j1)
    elif j1_in!=-1 and j2_in!=-1:
        if j1_in!=j2_in:
            new_circuit=circuits[j1_in].union(circuits[j2_in])
            del circuits[max(j1_in,j2_in)]
            del circuits[min(j1_in,j2_in)]
            circuits.append(new_circuit)
    count+=1
    if count==limit:
        circuits_1=circuits+[]
    if count>limit and len(circuits)==1 and len(circuits[0])==N_junctions:
        x_product=j1[0]*j2[0]
        break
circuit_sizes_1=[]
for c in circuits_1:
    bisect.insort(circuit_sizes_1,len(c))
print("1st:",circuit_sizes_1[-1]*circuit_sizes_1[-2]*circuit_sizes_1[-3])
print("2nd:",x_product)