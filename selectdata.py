# Select sunspot coordinates from results-raw file
# csv format : image_num, image_time, x, y, intensity
import os
import csv

rawdata_dir = 'rawdata_to_select/'
selected_dir = 'selected/'
filelist = os.listdir(rawdata_dir)

rawdata = []
zerorow = []
image = []
size = 1024

previous_row = 0

# DFS range. Need to determine this taxi radius.
dx = [0,1,1,1,0,-1,-1,-1]
dy = [1,1,0,-1,-1,-1,0,1]

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
    for i in range(0,8):
        if(image[x+dx[i]][y+dy[i]] == 1):
            dfs(x+dx[i],y+dy[i])
    
    
for num in range(0,len(filelist)): # process all files in rawdata_dir
    print ('Processing ' + filelist[num] + '...')
    f = open(rawdata_dir + filelist[num], 'r')
    result = open(selected_dir + 'selected_' + filelist[0], 'w')
    csvReader = csv.reader(f)
    for row in csvReader:
        rawdata.append(row)
        total_num_of_row += 1
    f.close()
    total_num_of_image = int(rawdata[len(rawdata)-1][0]) + 1
    print('Total ' + str(total_num_of_image) + ' images detected.')
    
    # to make zero array
    #for i in range(0,size):
    #    zerorow.append(0)
    
    num_row = 0
    for image_num in range(0,total_num_of_image):
        print('Image ' + str(image_num) + '...')
        
        # Make zero(blank) array
        #for i in range(0,size):
        #    image.append(zerorow)
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
                    result.write(str(image_num) + ',' + str(current_time) + ',' + str(x_pixel_sum / num_pixel) + ',' + str(y_pixel_sum / num_pixel) + '\n')
