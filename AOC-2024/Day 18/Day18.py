import os
from bisect import insort
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    falling_byte_coordinates=f.read().strip().split('\n')

if file=='example.txt':
    row_max=6
    col_max=6
    bytes_to_fall_0=12
else:
    row_max=70
    col_max=70
    bytes_to_fall_0=1024

directions=[(-1,0),(1,0),(0,-1),(0,1)]

def get_grid(bytes_to_fall):
    grid=[['.']*(col_max+1) for _ in range(row_max+1)]
    for falling_byte_coordinate in falling_byte_coordinates[:bytes_to_fall]:
        x,y=[int(c) for c in falling_byte_coordinate.split(',')]
        grid[y][x]='#'
    return grid
def check_grid(grid):
    position_queue=[(0,0,0)]
    visited_positions=set()
    # visited_positions={(0,0)} #with 1st Dijkstra version, it can be initiated like this to not risk visiting starting node again..but with 2nd it has to be initiated as above
    finished=False
    while position_queue:
        steps,y,x=position_queue.pop(0)        
        if (y,x)==(row_max,col_max):
            finished=True
            break
        #1st version of Dijkstra, add to visited when adding to the queue and let each popped position enter the loop
        for dy,dx in directions:
            y_new=y+dy
            x_new=x+dx
            if 0<=y_new<=row_max and 0<=x_new<=col_max and (y_new,x_new) not in visited_positions:
                if grid[y_new][x_new]!='#':
                    insort(position_queue,(steps+1,y_new,x_new))
                    #in Dijkstra used for day 16, the line below was not used (but it does solve correctly when adding it as well), visited_positions was instead added to when a new iteration of the while loop was started. In this problem, this does not work because one gets stuck in areas without any obstacles -probably because the same position is added multiple times since they go further down in the queue
                    #this does however prevent the same position from being added to the queue multiple times
                    #Day 16 was a mix of this and the one below, which does not work well for grids with lots of open grounds -better to stick with one of these!
                    visited_positions.add((y_new,x_new))
        #2nd version of Dijkstra, add to visited nodes after pop and don't let all popped values enter the loop
        #the importance seems to be to add to visited nodes just after the check to visited nodes has been made!
        #this avoids the issues of letting the same points add themselves to the queue over and over as mentioned above...
        # if (y,x) not in visited_positions:
        #     visited_positions.add((y,x))
        #     for dy,dx in directions:
        #         y_new=y+dy
        #         x_new=x+dx
        #         if 0<=y_new<=row_max and 0<=x_new<=col_max:
        #             if grid[y_new][x_new]!='#':
        #                 insort(position_queue,(steps+1,y_new,x_new))
    return steps,finished

#part 1
grid_1=get_grid(bytes_to_fall_0)
step_1,_=check_grid(grid_1)
print('1st:',step_1)

#part 2
bytes_to_fall=bytes_to_fall_0+1
while bytes_to_fall<len(falling_byte_coordinates):
    grid_2=get_grid(bytes_to_fall)
    step_2,finished_2=check_grid(grid_2)
    if not finished_2:
        break
    bytes_to_fall+=1
print('2nd:',falling_byte_coordinates[bytes_to_fall-1])