import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    device_list=f.read().strip().split('\n')

class Device:
    def __init__(self,label,outputs,device_objects_dict):
        self.label=label
        self.outputs=outputs
        self.inputs=[]
        self.device_objects_dict=device_objects_dict
        self.outputs_connected_to_out=set()
        self.output_path_sum=[0]
        self.connections_to_target_from_outputs_dict={o:0 for o in outputs}
        self.sum_connections=0
    def add_input(self,input):
        self.inputs.append(input)
    def assign_input_to_others(self):
        for output in self.outputs:
            self.device_objects_dict[output].add_input(self.label)

device_dict=dict()
device_dict_2=dict()
device_objects_dict={}
for device_row in device_list:
    device_label,device_outputs=device_row.split(':')
    device_outputs=device_outputs.strip().split()
    device_dict[device_label]=device_outputs
    device=Device(device_label,device_outputs,device_objects_dict)
    device_objects_dict[device_label]=device
device_label="out"
device=Device(device_label,[],device_objects_dict)
device_objects_dict[device_label]=device
for _,device in device_objects_dict.items():
    device.assign_input_to_others()

paths_to_out=[0]
def recursive_explore(device_label):
    if device_label=="out":
        paths_to_out[0]+=1
    else:
        for next_device_label in device_dict[device_label]:
            recursive_explore(next_device_label)
recursive_explore("you")
print("1st:",paths_to_out[0]) #must be commented out for 2nd example input to not crash (you does not exist in it)

#slow but simple and works:
#1. dac->out, track all visited devices
#2. remove all visited devices froom 1
#3. use remaining devices from 2, and do fft->dac (verified that dac->fft does not have any paths, with different input just swap fft and dac), track all visited devices
#4. remove all visited devices from 3
#5. use remaining devices from 4 and do svr->fft
#6. multiply all paths from 1,3 and 6
def recursive_explore_2(paths_to_target,device_dict,device_label,target,visited_set):
    visited_set.add(device_label)
    if device_label==target:
        paths_to_target[0]+=1
    else:
        for next_device_label in device_dict[device_label]:
            recursive_explore_2(paths_to_target,device_dict,next_device_label,target,visited_set)

start_last="out"
relevant_device_dict=device_dict
total_paths=1
for start in ["dac","fft","svr"]:
    paths=[0]
    visited_set=set()
    recursive_explore_2(paths,relevant_device_dict,start,start_last,visited_set)
    next_relevant_device_dict=dict()
    for label,outputs in relevant_device_dict.items():
        if label not in visited_set:
            next_relevant_device_dict[label]=[]
            for output in outputs:
                if output not in visited_set or output==start:
                    next_relevant_device_dict[label].append(output)
    total_paths*=paths[0]
    relevant_device_dict=next_relevant_device_dict
    start_last=start
print("2nd:",total_paths)