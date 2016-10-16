# Based on Python 3.5.2 | Anaconda 4.1.1

# Print software information
print('This is SunSpotTracker. (c) Seungwon Park under the terms of the MIT License')
print('Source : https://github.com/seungwonpark/SunSpotTracker')

from sys import argv
script, bool_plot, bool_raw = argv # Input : whether or not to plot(show) the images
bool_plot = int(bool_plot)
bool_raw = int(bool_raw)

# Print selected options
if(bool_plot == 1):
    print('Plotting : Enabled.')
else:
    print('Plotting : Disabled.')
if(bool_raw == 1):
    print('RAWdata : Enabled.')
else:
    print('RAWdata : Disabled.')

print('Loading Libraries...')

import math
import os
import scipy.ndimage
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import date


height = 1024
width = 1024
# radius_cut is used for removing dark background - so as to classify sunspots.
radius_cut = 440 # cutting radius
# real radius of sun - used for calculation.
radius_real = 460
halfheight = int(height/2)
halfwidth = int(width/2)
criterion = 40 # sunspot criterion

filelist = os.listdir('images/')

initial_date = date(1980,1,1) # Not related with any other julian day stuff!
def filename_to_hour(filename):
    # Only difference between two time will be collected with this function, so initial_date doesn't matter.
    fileinfo = filename.split('_')
    date_int = int(fileinfo[0]) # 20160901
    time_int = int(fileinfo[1]) # 131039
    
    year = int(date_int / 10000)
    month = int( (date_int % 10000) / 100)
    day = date_int % 100
    hour = int(time_int / 10000)
    minute = int ( (time_int % 10000) / 100)
    second = time_int % 100
    delta = date(year, month, day) - initial_date
    return delta.days * 24 + hour + (minute / 60) + (second / 3600)

# Initialize data saving
day = []
results = []
if(bool_raw == 0):
    savefile = open('results/results_' + filelist[0] + '_' + filelist[len(filelist)-1] + '.csv', 'a') # append
else:
    savefile = open('results/results-raw_' + filelist[0] + '_' + filelist[len(filelist)-1] + '.csv', 'a') # append

# Calculation of latitude and longitude of sunspot on sun
def latitude(x):
    return math.asin( (halfheight - x) / radius_real )
def longitude(x,y):
    return math.asin( (y - halfwidth) / (radius_real * math.cos(latitude(x))) )

# Initialize plotting
if(bool_plot == 1):
    plt.ion()

# Initialize dark background removal
X, Y = np.ogrid[0:height, 0:width]
boundary = (X - halfheight) ** 2 + (Y - halfwidth) ** 2 > radius_real ** 2

# Track
for num in range(0,len(filelist)):
    print ('Parsing ' + 'images/' + filelist[num] + '...')
    f = scipy.ndimage.imread( 'images/' + filelist[num] )
    day.append(filename_to_hour(filelist[num]))
    time = day[num] - day[0] # Elapsed time since first picture
    
    # Remove dark background
    f[boundary] = 255
    
    # Center line : vertical / horizontal
    for i in range(0, height):
        f[i, halfwidth] = 255
    for i in range(0, width):
        f[halfheight, i] = 255
    
    # Classify sunspot coordinates in image.
    for i in range(0, height):
        for j in range(0, width):
            if(f[i,j] < criterion):
                if(bool_raw == 0):
                    savefile.write(str(num) + ',' + str(time) + ',' + str(latitude(i)) + ',' + str(longitude(i,j)) + ',' + str(f[i,j]) + '\n')
                else:
                    savefile.write(str(num) + ',' + str(time) + ',' + str(i) + ',' + str(j) + ',' + str(f[i,j]) + '\n')
    if(bool_plot == 1):
        # Plot image
        plt.title(filelist[num])
        plt.xlabel('X coordinates')
        plt.ylabel('Y coordinates')
        plt.imshow(f)
        plt.show()
        plt.pause(0.0001)

if(bool_plot == 1):
    plt.close()

savefile.close()
