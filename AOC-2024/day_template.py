import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    data_list=f.read().strip().split('\n')