import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    dataList=f.read().strip().split('\n')