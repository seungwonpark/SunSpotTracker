# Select sunspot coordinates from results-raw file
# csv format : image_num, image_time, x, y, intensity
import os
import csv
import math

rawdata_dir = 'rawdata_to_select/'
selected_dir = 'selected/'
filelist = os.listdir(rawdata_dir)
write_recurerror = open('ErrorList/RecursionErrorList.txt', 'a')
write_unexperror = open('ErrorList/UnexpectedErrorList.txt', 'a')

# 2D array declaration
rawdata = []
zerorow = []
image = []

size = 1024
height = 1024
width = 1024
# radius_cut is used for removing dark background - so as to classify sunspots.
radius_cut = 440 # cutting radius
# real radius of sun - used for calculation.
radius_real = 460
halfheight = int(height/2)
halfwidth = int(width/2)

# Calculation of latitude and longitude of sunspot on sun
def latitude(x):
    return math.asin( (halfheight - x) / radius_real )
def longitude(x,y):
    return math.asin( (y - halfwidth) / (radius_real * math.cos(latitude(x))) )

#######################################################
#### DFS range. Need to determine this taxi radius.####
dx = [0,1,1,1,0,-1,-1,-1]
dy = [1,1,0,-1,-1,-1,0,1]
#######################################################

# temporary variables
x_pixel_sum = 0
y_pixel_sum = 0
num_pixel = 0
total_num_of_row = 0

def dfs(x,y): # DFS(Depth First Search)
    global x_pixel_sum
    global y_pixel_sum
    global num_pixel
    image[x][y] = -1 # mark as already visited.
    x_pixel_sum += x
    y_pixel_sum += y
    
    num_pixel += 1
    for i in range(0,len(dx)):
        if(image[x+dx[i]][y+dy[i]] == 1):
            dfs(x+dx[i],y+dy[i])
    
    
for num in range(0,len(filelist)): # process all files in rawdata_dir
    print ('Processing ' + filelist[num] + '...')
    f = open(rawdata_dir + filelist[num], 'r')
    result_raw = open(selected_dir + 'selected-raw_' + filelist[0], 'w')
    result = open(selected_dir + 'selected_' + filelist[0], 'w')
    csvReader = csv.reader(f)
    for row in csvReader:
        rawdata.append(row)
        total_num_of_row += 1
    f.close()
    total_num_of_image = int(rawdata[len(rawdata)-1][0]) + 1
    print('Total ' + str(total_num_of_image) + ' images detected.')
    
    num_row = 0
    for image_num in range(0,total_num_of_image):
        try:
            print('Image ' + str(image_num) + '...')
            
            image = [[0 for a in range(size)] for b in range(size)]
            
            # Make image array to perform DFS
            while(int(rawdata[num_row][0]) == image_num):
                current_time = float(rawdata[num_row][1])
                x = int(rawdata[num_row][2])
                y = int(rawdata[num_row][3])
                image[x][y] = 1
                num_row += 1
                if(num_row == total_num_of_row):
                    break
            
            print('DFS...')
            for a in range(0,size):
                for b in range(0,size):
                    if(image[a][b] == 1):
                        x_pixel_sum = 0
                        y_pixel_sum = 0
                        num_pixel = 0
                        dfs(a,b)
                        x_average = x_pixel_sum / num_pixel
                        y_average = y_pixel_sum / num_pixel
                        latit = latitude(x_average)
                        longi = longitude(x_average, y_average)
                        
                        result_raw.write(str(image_num) + ',' + str(current_time) + ',' + str(format(x_average, '.1f')) + ',' + str(format(y_average, '.1f')) + '\n')
                        result.write(str(image_num) + ',' + str(current_time) + ',' + str(format(latit, '.1f')) + ',' + str(format(longi, '.1f')) + '\n')
        except RecursionError:
            print('RecursionError had occured. This image number is saved to ErrorList/RecursionError.txt.')
            write_recurerror.write('Image No.' + str(image_num) + ' of file ' + filelist[num] + '\n')
        except:
            print('Unexpected error had occured. This image name is saved to ErrorList/UnexpectedErrorList.txt.')
            print('Skipping Image No.' + str(image_num) + ' of file ' + filelist[num] + '...')
            write_unexperror.write('Image No.' + str(image_num) + ' of file ' + filelist[num] + '\n')
