import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    data=f.read().strip()
start_engravings=data.split()

engraving_dict=dict() #keys=unique stone engravings, items=dicts with keys=number of blinks_to_go (i.e. before 0 left) => memoization for encountered engravings and blinks left, otherwise just apply rules and keep blinking recursively
def apply_rules(engraving):
    if engraving=='0':
        return ['1']
    N=len(engraving)
    if N%2==0:
        return [engraving[:N//2],str(int(engraving[N//2:]))] #str(int(...)) to get rid of leading 0s
    return [str(int(engraving)*2024)]

def add_engraving(blinks_to_go,engraving,stone_spawns_at_0):
    try:
        entry_dict=engraving_dict[engraving]
    except:
        engraving_dict[engraving]=dict()
        entry_dict=engraving_dict[engraving]
    entry_dict[blinks_to_go]=stone_spawns_at_0

def recursive_blinking(blinks_to_go,engraving,number_of_spawned_stones=0):
    if blinks_to_go==0:
        add_engraving(blinks_to_go,engraving,number_of_spawned_stones)
        return number_of_spawned_stones
    if engraving in engraving_dict:
        if blinks_to_go in engraving_dict[engraving]:
            return engraving_dict[engraving][blinks_to_go]
        
    new_engravings=apply_rules(engraving)
    N_spawned_stones_at_0=len(new_engravings)-1
    for stone_engraving in new_engravings:
        N_spawned_stones_at_0+=recursive_blinking(blinks_to_go-1,stone_engraving)
    add_engraving(blinks_to_go,engraving,N_spawned_stones_at_0)
    return N_spawned_stones_at_0

def blink(blinks_to_do):
    number_of_stones_at_0=len(start_engravings)
    for engraving in start_engravings:
        number_of_stones_at_0+=recursive_blinking(blinks_to_do,engraving)
    return number_of_stones_at_0

print('1st:',blink(25))
print('2nd:',blink(75))