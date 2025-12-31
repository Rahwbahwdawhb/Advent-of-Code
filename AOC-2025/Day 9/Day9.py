import os
import bisect
os.chdir(os.path.dirname(__file__))
file='input.txt'
with open(file) as f:
    red_corner_strs=f.read().strip().split('\n')
red_corners=[]
x_border_dict={} #y-keys
y_border_dict={} #x-keys
border=[] #used in 1st slow solution
for red_corner_str in red_corner_strs:
    x_,y_=red_corner_str.split(',')
    x,y=int(x_),int(y_)
    red_corners.append((x,y))
    try:
        if x==last_x:
            if x not in y_border_dict:
                y_border_dict[x]=[]
            y_=min(y,last_y)
            y_stop=max(y,last_y)
            while y_<=y_stop:
                bisect.insort(y_border_dict[x],y_)
                border.append((x,y_))
                if y_ not in x_border_dict:
                    x_border_dict[y_]=[x]
                else:
                    bisect.insort(x_border_dict[y_],x)
                y_+=1
        else:
            if y not in x_border_dict:
                x_border_dict[y]=[]
            x_=min(x,last_x)
            x_stop=max(x,last_x)
            while x_<=x_stop:
                bisect.insort(x_border_dict[y],x_)
                border.append((x_,y))
                if x_ not in y_border_dict:
                    y_border_dict[x_]=[y]
                else:
                    bisect.insort(y_border_dict[x_],y)
                x_+=1
    except:
        pass
    last_x,last_y=x,y

last_x,last_y=border[0][0],border[0][1]
if x==last_x:
    if x not in y_border_dict:
        y_border_dict[x]=[]
    y_=min(y,last_y)
    y_stop=max(y,last_y)
    while y_<=y_stop:
        bisect.insort(y_border_dict[x],y_)
        border.append((x,y_))
        if y_ not in x_border_dict:
            x_border_dict[y_]=[x]
        else:
            bisect.insort(x_border_dict[y_],x)
        y_+=1
else:
    if y not in x_border_dict:
        x_border_dict[y]=[]
    x_=min(x,last_x)
    x_stop=max(x,last_x)
    while x_<=x_stop:
        bisect.insort(x_border_dict[y],x_)
        border.append((x_,y))
        if x_ not in y_border_dict:
            y_border_dict[x_]=[y]
        else:
            bisect.insort(y_border_dict[x_],y)
        x_+=1
border=set(border)

area_max=0
area_max_2=0
checked_corners=set()
inside_points=set()
areas=[]
for red_corner in red_corners:
    for red_corner_ in red_corners:
        if red_corner==red_corner_:
            continue
        if (red_corner,red_corner_) in checked_corners or (red_corner_,red_corner) in checked_corners:
            continue
        checked_corners.add((red_corner,red_corner_))
        x_start,x_stop=min(red_corner[0],red_corner_[0]),max(red_corner[0],red_corner_[0])
        y_start,y_stop=min(red_corner[1],red_corner_[1]),max(red_corner[1],red_corner_[1])
        area=(abs(x_start-x_stop)+1)*(abs(y_start-y_stop)+1)
        area_max=max(area_max,area)
        bisect.insort(areas,(area,red_corner,red_corner_))

#Decently fast
outer_points=set()
while areas:
    area,red_corner,red_corner_=areas.pop()
    x_start,x_stop=min(red_corner[0],red_corner_[0]),max(red_corner[0],red_corner_[0])
    y_start,y_stop=min(red_corner[1],red_corner_[1]),max(red_corner[1],red_corner_[1])
    
    #check if corners of rectangle lie outside the points along the boarder
    if not(y_border_dict[x_start][0]<=y_start and y_stop<=y_border_dict[x_start][-1]):
        continue
    if not(y_border_dict[x_stop][0]<=y_start and y_stop<=y_border_dict[x_stop][-1]):
        continue
    if not(x_border_dict[y_start][0]<=x_start and x_stop<=x_border_dict[y_start][-1]):
        continue
    if not(x_border_dict[y_stop][0]<=x_start and x_stop<=x_border_dict[y_stop][-1]):
        continue

    starts=[y_start,y_start,x_start,x_start]
    stops=[y_stop,y_stop,x_stop,x_stop]
    border_dicts=[y_border_dict[x_start],y_border_dict[x_stop],x_border_dict[y_start],x_border_dict[y_stop]]
    perpendicular_border_dicts=[x_border_dict,x_border_dict,y_border_dict,y_border_dict]
    perpendicular_starts=[x_start,x_start,y_start,y_start]
    fine=True
    for border_dict,start,stop,perpendicular_border_dict,perpendicular_start in zip(border_dicts,starts,stops,perpendicular_border_dicts,perpendicular_starts):
        i_1=bisect.bisect_left(border_dict,start)
        i_2=bisect.bisect_right(border_dict,stop)
        ref=border_dict[i_1]
        #check if there are any index skips along borders (i.e. potential outside regions)
        for i in range(i_1+1,i_2):
            temp=border_dict[i]
            if temp-ref>1:
                check_low_i=bisect.bisect_left(perpendicular_border_dict[temp],start)-1
                check_high_i=bisect.bisect_right(perpendicular_border_dict[temp],stop)
                try:
                    check_low=perpendicular_border_dict[temp][check_low_i]
                    check_high=perpendicular_border_dict[temp][check_high_i]
                except:
                    fine=False
                    break
                #at index skips, check if there are perpendicular borders that surround the point corresponding to the index after the skip
                if not (check_low<=perpendicular_start<=check_high):
                    fine=False
                    break
            ref=temp
        if not fine:
            break
    if fine:
        #the areas are sorted in ascending order, so the last one that is fine will be the biggets one (no need to compare with prior area_max_2-value)
        area_max_2=area
        break

# #still slow, but a bit faster
# outer_points=set()
# while areas:
#     area,red_corner,red_corner_=areas.pop()
#     x_start,x_stop=min(red_corner[0],red_corner_[0]),max(red_corner[0],red_corner_[0])
#     y_start,y_stop=min(red_corner[1],red_corner_[1]),max(red_corner[1],red_corner_[1])
    
#     if not(y_border_dict[x_start][0]<=y_start and y_stop<=y_border_dict[x_start][-1]):
#         continue
#     if not(y_border_dict[x_stop][0]<=y_start and y_stop<=y_border_dict[x_stop][-1]):
#         continue
#     if not(x_border_dict[y_start][0]<=x_start and x_stop<=x_border_dict[y_start][-1]):
#         continue
#     if not(x_border_dict[y_stop][0]<=x_start and x_stop<=x_border_dict[y_stop][-1]):
#         continue
#     fine=True
#     for x in range(x_start,x_stop+1):
#         for y in [y_start,y_stop]:
#             if (x,y) in outer_points:
#                 fine=False
#                 break
#             if (x,y) not in border and (x,y) not in inside_points:
#                 yc_1i=bisect.bisect_left(y_border_dict[x],y)-1
#                 yc_2i=bisect.bisect_right(y_border_dict[x],y)
#                 try:
#                     yc_1=y_border_dict[x][yc_1i]
#                     yc_2=y_border_dict[x][yc_2i]
#                     if not (yc_1<=y<=yc_2):
#                         fine=False
#                         break
#                 except:
#                     fine=False
#                     break
#                 try:
#                     xc_1i=bisect.bisect_left(x_border_dict[y],x)-1
#                     xc_2i=bisect.bisect_right(x_border_dict[y],x)
#                     xc_1=x_border_dict[y][xc_1i]
#                     xc_2=x_border_dict[y][xc_2i]
#                     if not (xc_1<=x<=xc_2):
#                         fine=False
#                         break
#                 except:
#                     fine=False
#                     break
#             inside_points.add((x,y))
#         if not fine:
#             outer_points.add((x,y))
#             break
#     if fine:
#         for x in [x_start,x_stop]:
#             for y in range(y_start,y_stop+1):
#                 if (x,y) in outer_points:
#                     fine=False
#                     break
#                 if (x,y) not in border and (x,y) not in inside_points:
#                     yc_1i=bisect.bisect_left(y_border_dict[x],y)-1
#                     yc_2i=bisect.bisect_right(y_border_dict[x],y)
#                     try:
#                         yc_1=y_border_dict[x][yc_1i]
#                         yc_2=y_border_dict[x][yc_2i]
#                         if not (yc_1<=y<=yc_2):
#                             fine=False
#                             break
#                     except:
#                         fine=False
#                         break
#                     try:
#                         xc_1i=bisect.bisect_left(x_border_dict[y],x)-1
#                         xc_2i=bisect.bisect_right(x_border_dict[y],x)
#                         xc_1=x_border_dict[y][xc_1i]
#                         xc_2=x_border_dict[y][xc_2i]
#                         if not (xc_1<=x<=xc_2):
#                             fine=False
#                             break
#                     except:
#                         fine=False
#                         break
#                 inside_points.add((x,y))
#             if not fine:
#                 outer_points.add((x,y))
#                 break
#     if fine:
#         area_max_2=area
#         break

# #slow but works
# outer_points=set()
# while areas:
#     area,red_corner,red_corner_=areas.pop()
#     x_start,x_stop=min(red_corner[0],red_corner_[0]),max(red_corner[0],red_corner_[0])
#     y_start,y_stop=min(red_corner[1],red_corner_[1]),max(red_corner[1],red_corner_[1])
#     fine=True
#     for x in range(x_start,x_stop+1):
#         for y in [y_start,y_stop]:
#             if (x,y) in outer_points:
#                 fine=False
#                 break
#             if (x,y) not in border and (x,y) not in inside_points:
#                 yc_1i=bisect.bisect_left(y_border_dict[x],y)-1
#                 yc_2i=bisect.bisect_right(y_border_dict[x],y)
#                 try:
#                     yc_1=y_border_dict[x][yc_1i]
#                     yc_2=y_border_dict[x][yc_2i]
#                     if not (yc_1<=y<=yc_2):
#                         fine=False
#                         break
#                 except:
#                     fine=False
#                     break
#                 try:
#                     xc_1i=bisect.bisect_left(x_border_dict[y],x)-1
#                     xc_2i=bisect.bisect_right(x_border_dict[y],x)
#                     xc_1=x_border_dict[y][xc_1i]
#                     xc_2=x_border_dict[y][xc_2i]
#                     if not (xc_1<=x<=xc_2):
#                         fine=False
#                         break
#                 except:
#                     fine=False
#                     break
#             inside_points.add((x,y))
#         if not fine:
#             outer_points.add((x,y))
#             break
#     if fine:
#         for x in [x_start,x_stop]:
#             for y in range(y_start,y_stop+1):
#                 if (x,y) in outer_points:
#                     fine=False
#                     break
#                 if (x,y) not in border and (x,y) not in inside_points:
#                     yc_1i=bisect.bisect_left(y_border_dict[x],y)-1
#                     yc_2i=bisect.bisect_right(y_border_dict[x],y)
#                     try:
#                         yc_1=y_border_dict[x][yc_1i]
#                         yc_2=y_border_dict[x][yc_2i]
#                         if not (yc_1<=y<=yc_2):
#                             fine=False
#                             break
#                     except:
#                         fine=False
#                         break
#                     try:
#                         xc_1i=bisect.bisect_left(x_border_dict[y],x)-1
#                         xc_2i=bisect.bisect_right(x_border_dict[y],x)
#                         xc_1=x_border_dict[y][xc_1i]
#                         xc_2=x_border_dict[y][xc_2i]
#                         if not (xc_1<=x<=xc_2):
#                             fine=False
#                             break
#                     except:
#                         fine=False
#                         break
#                 inside_points.add((x,y))
#             if not fine:
#                 outer_points.add((x,y))
#                 break
#     if fine:
#         area_max_2=area
#         break

print("1st:",area_max)
print("2nd:",area_max_2)