import os
import numpy as np
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    input_list=f.read().strip().split('\n\n')

#stuff to get get all different present orientations, turned out to not be required
A=np.array([[1,2,3],[4,5,6],[7,8,9]])
_ccw90=lambda matrix:matrix.T[::-1,:]
_xflip=lambda matrix:matrix[:,::-1]
_yflip=lambda matrix:matrix[::-1,:]
operations_at_each_rotation=[[_xflip],[_yflip],[_xflip,_yflip]]

orientations_dict={(0,0):[(0,0)],(0,1):[(0,1)],(0,2):[(0,2)],
                   (1,0):[(1,0)],(1,1):[(1,1)],(1,2):[(1,2)],
                   (2,0):[(2,0)],(2,1):[(2,1)],(2,2):[(2,2)]}
value_index_dict={1:(0,0),2:(0,1),3:(0,2),
                  4:(1,0),5:(1,1),6:(1,2),
                  7:(2,0),8:(2,1),9:(2,2)}

flatten_set={tuple(A.flatten())}
for _ in range(3):
    A=_ccw90(A)
    for operations in operations_at_each_rotation:
        A_=A+0
        for operation in operations:
            A_=operation(A_)
        A_flatten=tuple(A_.flatten())
        if A_flatten not in flatten_set:
            flatten_set.add(A_flatten)
            for ir,row in enumerate(A_):
                for ic,col in enumerate(row):
                    orientations_dict[value_index_dict[col]].append((ir,ic))

present_dict=dict()
region_list=[]
can_fit_sum=0
for entry in input_list:
    entry_list=entry.split('\n')
    if entry_list[0][-1]==':':
        id=int(entry_list[0][0])
        _sum=0
        for row in entry_list[1:]:
            for ch in row:
                if ch=='#':
                    _sum+=1
        present_dict[id]=_sum
        #stuff to get get all different present orientations, turned out to not be required
        # present_shape=np.zeros((3,3))
        # for ir,row in enumerate(entry_list[1:]):
        #     for ic,col in enumerate(row):
        #         if col=='#':
        #             present_shape[ir,ic]=1
    else:
        for row in entry.split('\n'):
            dimension_str,present_str=row.split(':')
            row_area=1
            for dimension in dimension_str.split('x'):
                row_area*=int(dimension)
            minimally_required_area=0
            for id,qty in enumerate(present_str.split()):
                minimally_required_area+=present_dict[id]*int(qty)
            if row_area>=minimally_required_area:
                can_fit_sum+=1
print("1st:",can_fit_sum)

