import os
os.chdir(os.path.dirname(__file__))
fileName='input.txt'
with open(fileName) as f:
    inputStr=f.read() 