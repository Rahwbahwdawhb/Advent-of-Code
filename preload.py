#this file can be imported from subdirectories and will read the .txt-files called input.txt in those folders
#by running from preload import input, the file contents can be accessed as a string
#in order for this to work, this script needs to be placed in a directory that's interpreted as a module
#and then installed to the virtual environment running the scripts, details:
#https://stackoverflow.com/questions/1054271/how-to-import-a-python-class-that-is-in-a-directory-above

from os import chdir
from os.path import dirname
import __main__

#change directory to that of file calling this script
chdir(dirname(__main__.__file__))

def readInput():
    fileStr=None
    with open('input.txt') as file:
        fileStr=file.read()
    return fileStr

#read the input.txt-file in the folder of the calling file
input=readInput() 

