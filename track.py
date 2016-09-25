import math
import os
import scipy.ndimage
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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

# Initialize data saving
results = []
def latitude(x):
    return math.asin( (halfheight - x) / radius_real )
def longtitude(x,y):
    return math.asin( (y - halfwidth) / (radius_real * math.cos(latitude(x))) )

# Initialize plotting
plt.ion()

for num in range(0,len(filelist)):
    print ('Parsing ' + 'images/' + filelist[num] + '...')
    f = scipy.ndimage.imread( 'images/' + filelist[num] )
    # Remove dark background
    X, Y = np.ogrid[0:height, 0:width]
    boundary = (X - halfheight) ** 2 + (Y - halfwidth) ** 2 > radius_real ** 2
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
                results.append([latitude(i), longtitude(i,j), num])
    
    # Plot image
    plt.imshow(f)
    plt.show()
    plt.pause(0.0001)

plt.close()
a = np.asarray(results)
np.savetxt('results.csv', a, delimiter=',')
