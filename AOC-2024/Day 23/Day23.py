import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    map_rows=f.read().strip().split('\n')

class computer: #node to keep track of computer connections
    def __init__(self,id,computer_id_dict):
        self.id=id
        self.connected_ids=set()
        self.computer_dict=computer_id_dict
    def add_connection(self,id):
        self.connected_ids.add(id)
        self.computer_dict[id].connected_ids.add(self.id)
    def get_connections(self):
        return self.connected_ids

computer_id_dict=dict() #populating with all computers and setting up their connections
for row in map_rows:
    computer_ids=row.split('-')
    for computer_id in computer_ids:
        if computer_id not in computer_id_dict:
            computer_id_dict[computer_id]=computer(computer_id,computer_id_dict)
    computer_id_dict[computer_ids[0]].add_connection(computer_ids[1])

def add_to_dict(_id,_dict):
    try:
        _dict[_id]+=1
    except:
        _dict[_id]=1

#part 1
#for each node (computer), check if its neighbors' connections share any common connection with the node (the node does not list itself as a connection), if so the node + its neighbor + the common connection form a 3-party connection
#if the node and its neighbor share more than one common connection, they are part of multiple 3-part connections
party_dict=dict() #could have used set, but dict was nice in part 2
for id,computer_ in computer_id_dict.items():
    connection_ids=computer_.get_connections()
    for connection_id in connection_ids: #loop through neighbors' neighbors
        connection_ids_=computer_id_dict[connection_id].get_connections()
        id_overlap=connection_ids.intersection(connection_ids_) #check common node (computer) ids
        if len(id_overlap)==1: #1 common connection
            party_str=str(sorted(list(id_overlap.union({id,connection_id})))).strip('[]').replace("'",'').replace(' ','') #sort ids in connections alphabetically to avoid duplicate dict-keys with different permutations
            add_to_dict(party_str,party_dict)
        elif len(id_overlap)>1: #multiple common connections
            for id_ in id_overlap:
                party_str=str(sorted([id,id_,connection_id])).strip('[]').replace("'",'').replace(' ','')
                add_to_dict(party_str,party_dict)
N_3parties_with_ts=0
for party,_ in party_dict.items():
    if party[0]=='t' or ',t' in party: #looking for computers BEGINNING (not just containing) a t
        N_3parties_with_ts+=1
print('1st:',N_3parties_with_ts)

#part 2
#the idea is to recursively iterate through all of the computer's neighbors down to a given depth and check if a reference id is a part of the neighbors for each node (computer) at the given depth
#each time the reference id is present in a node's list of neighbors, add 1 to its count in a dictionary
#after each iteration, remove the nodes with the fewest connections, for the next iteration when iterating through neighbors, only visit those that are still left after the first iteration
#if all nodes have the same counts, increment the depth by 1, reset the dictionary counts to 0 and start over
#if all nodes have the same counts and the nodes left have been the same for two iterations stop the iteration (this means that the nodes that remain are all part of the largest connection, since one only checks neighbors that survived prior removals)
def recursive_loop(id_ref,id,id_count_dict,depth,loop_ids):
    if depth==0:
        if id_ref in computer_id_dict[id].get_connections():
            add_to_dict(id_ref,id_count_dict) #count occurrences at the final depth
    else:
        for id_ in computer_id_dict[id].get_connections():
            if id_ in loop_ids:
                recursive_loop(id_ref,id_,id_count_dict,depth-1,loop_ids)

loop_ids=list(computer_id_dict.keys()) #start with all node (computer) ids
depth=1 #initial depth
depth_dict=dict()
last_loop_ids=None
identical_counter=0
while loop_ids:
    id_count_dict={}
    min_max_counts=[10**16,0]
    count_id_dict=dict()
    for id in loop_ids:
        recursive_loop(id,id,id_count_dict,depth,loop_ids)
        count=id_count_dict[id]
        min_max_counts=[min([min_max_counts[0],count]),max([min_max_counts[1],count])]
        try:
            count_id_dict[count].append(id)
        except:
            count_id_dict[count]=[id]
    if min_max_counts[0]==min_max_counts[1]: #if all counts are the same, increase depth and increment identical counter
        depth+=1
        if last_loop_ids==loop_ids:
            identical_counter+=1
    else:
        for id in count_id_dict[min_max_counts[0]]: #remove the ids corresponding to the lowest counts
            loop_ids.remove(id)
        depth=1 #reset depth
        identical_counter=0 #reset identical counter
    if identical_counter==2:
        break
    last_loop_ids=loop_ids
print('2nd:',','.join(sorted(loop_ids)))