import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example_short.txt'
# file='example_long.txt'
# file='example_short_2.txt'
with open(file) as f:
    warehouse_map_str,move_sequence_str=dataList=f.read().strip().split('\n\n')
warehouse_map_list=warehouse_map_str.split('\n')
move_sequence_list=move_sequence_str.split('\n')
move_sequence=''.join(move_sequence_list)

grid=[] #part 1
grid_2=[] #part 2
for i,row in enumerate(warehouse_map_str.split('\n')):
    temp=[] #part 1
    temp_2=[] #part 2
    for ii,ch in enumerate(row):
        temp.append(ch) #part 1
        if ch=='@':
            #part 1
            robot_row=i
            robot_col=ii
            temp[-1]='.'
            #part 2
            robot_row_2=i
            robot_col_2=ii*2
            temp_2+=['.','.']
        elif ch=='#': #part 2
            temp_2+=['#','#']
        elif ch=='O': #part 2
            temp_2+=['[',']']
        elif ch=='.': #part 2
            temp_2+=['.','.']
    grid.append(temp) #part 1
    grid_2.append(temp_2) #part 2

move_dict={'>':[0,1],'<':[0,-1],'^':[-1,0],'v':[1,0]}
anti_move_dict={'>':move_dict['<'],'<':move_dict['>'],'^':move_dict['v'],'v':move_dict['^']}

def recursive_move(row,col,direction,anti_direction): #part 1
    if grid[row][col]=='#':
        move_bool=False
    elif grid[row][col]=='O':
        move_bool=recursive_move(row+direction[0],col+direction[1],direction,anti_direction)
    else:
        move_bool=True
    if move_bool:
        grid[row][col]=grid[row+anti_direction[0]][col+anti_direction[1]]
    return move_bool

def recursive_move_2(grid,row,col,direction,anti_direction,actively_pushed=True): #part 2 
    current_ch=grid[row][col]
    if current_ch=='#':
        move_bool=False
        grid_updates=[]
        
    elif current_ch=='[' or current_ch==']':
        if direction in [[0,-1],[0,1]]:
            move_bool,grid_updates_=recursive_move_2(grid,row+direction[0],col+direction[1],direction,anti_direction)
            grid_updates=[[row,col,grid[row+anti_direction[0]][col+anti_direction[1]],actively_pushed]]+grid_updates_
        else:
            prior_ch=grid[row+anti_direction[0]][col+anti_direction[1]]
            if current_ch==prior_ch:
                move_bool,grid_updates_=recursive_move_2(grid,row+direction[0],col+direction[1],direction,anti_direction)
                grid_updates=[[row,col,grid[row+anti_direction[0]][col+anti_direction[1]],actively_pushed]]+grid_updates_
            else:
                #this is where one ends up if boxes are stacked like:
                # []
                #[]
                #and one pushes up or down, this is handled by doing a recursion on the neighboring column i.e. the one containg the ] if one starts in a [
                #and that recursion is labelled by actively_pushed=False, since that recursion was not issued by something actually pushing on that box part
                #the character to replace the character at the current neigboring column is assumed to be ., meaning that no other box was pusing on it
                #this caused problems in the following situation:
                # [][]
                #[][]
                #since e.g. the leftmost [ on the top will be pushed by a ] issuing a neighboring recursion for its ] that will want to replace
                #the [ below it with a . (as if it was not being pushed by the rightmost bottom box).
                #to resolve this, all of the actively_pushed=True recursions are added first to a list of characters to update and actively_pushed=False recursions are only added if
                #no active recursion for the same grid position has already been added to this list
                move_bool_1,grid_updates_1=recursive_move_2(grid,row+direction[0],col+direction[1],direction,anti_direction)
                if grid[row][col]=='[':
                    extra_col=1
                else:
                    extra_col=-1
                move_bool_2,grid_updates_2=recursive_move_2(grid,row+direction[0],col+extra_col+direction[1],direction,anti_direction,actively_pushed=False)
                if sum([move_bool_1,move_bool_2])==2: #check that all subsequent recursions are valid, i.e. no box going into an obstacle
                    move_bool=True
                    grid_updates=[[row,col,grid[row+anti_direction[0]][col+anti_direction[1]],actively_pushed]]
                    grid_updates+=[[row,col+extra_col,'.',False]]
                    grid_updates+=grid_updates_1
                    grid_updates+=grid_updates_2
                else:
                    move_bool=False
                    grid_updates=[]
    else:
        move_bool=True
        grid_updates=[[row,col,grid[row+anti_direction[0]][col+anti_direction[1]],actively_pushed]]

    final_grid_updates=[]
    active_coordinates=set()
    passive=[]
    while grid_updates:
        temp=grid_updates.pop()
        if temp[-1]:
            final_grid_updates.append(temp)
            active_coordinates.add((temp[0],temp[1]))
        else:
            passive.append(temp)
    for temp in passive:
        if (temp[0],temp[1]) not in active_coordinates:
            final_grid_updates.append(temp)
    return move_bool,final_grid_updates

def get_GPS(grid,ch_count):
    GPS=0
    count=0 #had this as output to debug issue with over [ and ] risking getting replaced by . with boxes stacked with [ and ] meeting
    for i,row in enumerate(grid):
        for ii,ch in enumerate(row):
            if ch==ch_count:
                GPS+=100*i+ii
                count+=1
    return GPS,count

for move in move_sequence:
    direction=move_dict[move]
    #part 1
    new_robot_row=robot_row+direction[0]
    new_robot_col=robot_col+direction[1]
    if recursive_move(new_robot_row,new_robot_col,direction,anti_move_dict[move]):
        robot_row=new_robot_row
        robot_col=new_robot_col
    #part 2
    new_robot_row_2=robot_row_2+direction[0]
    new_robot_col_2=robot_col_2+direction[1]
    move_bool,grid_updates=recursive_move_2(grid_2,new_robot_row_2,new_robot_col_2,direction,anti_move_dict[move])
    if move_bool:
        robot_row_2=new_robot_row_2
        robot_col_2=new_robot_col_2
        for row,col,ch,_ in grid_updates:
            grid_2[row][col]=ch

GPS_1,_=get_GPS(grid,'O')
print('1st:',GPS_1)
GPS_2,_=get_GPS(grid_2,'[')
print('2nd:',GPS_2)

#debug tool
def print_grid(grid,robot_row,robot_col,index_ranges=None):
    if index_ranges:        
        ir0,ir1,ic0,ic1=index_ranges
        grid_t=grid[ir0:ir1+1]
        grid_t=[x[ic0:ic1+1] for x in grid_t]
        e_grid=enumerate(grid_t)
    else:
        e_grid=enumerate(grid)
        ir0=0
        ic0=0
    for ir,row in e_grid:
        temp=''
        for ic,col in enumerate(row):
            if ir+ir0==robot_row and ic+ic0==robot_col:
                temp+='@'
            else:
                temp+=col
        print(temp)
# print_grid(grid_2,robot_row_2,robot_col_2) #print full grid
# print_grid(grid_2,robot_row_2,robot_col_2,[robot_row_2-5,robot_row_2+5,robot_col_2-5,robot_col_2+5]) #print part of grid around robot