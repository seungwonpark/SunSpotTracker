import math
import os
import scipy.ndimage
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
filelist_str = str(filelist)
filelist_str = filelist_str.replace('[','')
filelist_str = filelist_str.replace(']','')
filelist_str = filelist_str.replace("'",'')
filelist_str = filelist_str.replace(' ','')
filelist_str = filelist_str.replace('.jpg','')
filelist_dir = filelist_str.split(',')

# Initialize an animation
fig = plt.figure()
num = 0

# Initialize data saving
results = []

def updatefig(*args):
    global num
    f = scipy.ndimage.imread( 'images/' + filelist_dir[num] + '.jpg' )
    num += 1
    if(num >= len(filelist)): # Repeat the animation
        num = 0
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
                results.append([i, j, num])
    
    #im = plt.imshow(f, animated = True)
    im = plt.figure()
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit = True, save_count = 0)
plt.show()
a = np.asarray(results)
np.savetxt('results.csv', a, delimiter=',')
