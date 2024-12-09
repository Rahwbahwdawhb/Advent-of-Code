# Go to any day in AOC and click the link that shows the input for that day
# Follow the instructions here https://github.com/wimglenn/advent-of-code-wim/issues/1
# and locate the cookie part of the header that start with "session=..."
# copy that into a .txt file called token.txt (don't include ; if the ... part ends with it)
# placed in the same folder as this file, then just run this file after setting the day_date below.
# This will create a subfolder called "Day day_date" and add a file called input.txt to this folder.
# NOTE: this assumes that the name of the folder containing this file ends with -YEAR, e.g. -2024

day_date=9

def fetch_function():
    year=os.getcwd().split('-')[-1]    
    day_folder_name=f"Day {day_date}"
    directory_items=os.listdir()
    if day_folder_name not in directory_items:
        os.mkdir(day_folder_name)
        shutil.copyfile('dayTemplate.py',os.path.join(day_folder_name,f'Day{day_date}.py'))
    try:
        with open(os.path.join(day_folder_name,'input.txt')) as f:
            if len(f.read())==0:
                fetch_input_bool=True
            else:
                fetch_input_bool=False
    except:
        fetch_input_bool=True
    if fetch_input_bool:
        url=f"https://adventofcode.com/{year}/day/{day_date}/input"
        req=requests.get(url=url,cookies={cookie_token_list[0]:cookie_token_list[1]})
        with open(os.path.join(day_folder_name,'input.txt'),'w') as f:
            f.write(req.text)
        print(f'Input fetched into file: Day {day_date}/input.txt')


if __name__=='__main__':
    import os
    import requests
    import sys
    import shutil
    if len(sys.argv)==2:
        try:
            day_date=int(sys.argv[1])
        except:
            print('Could not convert input to int!')
    os.chdir(os.path.dirname(__file__))    
    try:
        with open('token.txt') as f:
            cookie_token_list=f.read().split('=')
    except:
        print('Something went wrong when reading token.txt :(')        
    fetch_function()