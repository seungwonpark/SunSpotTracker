import math
import os
import scipy.ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

height = 1024
width = 1024
radius = 450 # cutting radius
halfheight = int(height/2)
halfwidth = int(width/2)
criterion = 40 # sunspot criterion

filelist = os.listdir('images/')
filelist_str = str(filelist)
filelist_str = filelist_str.replace('[','')
filelist_str = filelist_str.replace(']','')
filelist_str = filelist_str.replace("'",'')
filelist_str = filelist_str.replace(' ','')
filelist_str = filelist_str.replace('.png','')
filelist_dir = filelist_str.split(',')

# Initialize an animation
fig = plt.figure()
num = 0

def updatefig(*args):
    global num
    f = scipy.ndimage.imread( 'images/' + filelist_dir[num] )
    num += 1
    if(num >= len(filelist)):
        num = 0
    X, Y = np.ogrid[0:height, 0:width]
    boundary = (X - halfheight) ** 2 + (Y - halfwidth) ** 2 > radius ** 2
    f[boundary] = 255
    for i in range(0, height): # center line (vertical)
        f[i, halfwidth] = 255
    for i in range(0, width): # center line (horizontal)
        f[halfheight, i] = 255
    
    im = plt.imshow(f, animated = True)
    return im,
    
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit = True)
plt.show()