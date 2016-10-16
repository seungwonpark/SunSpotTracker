# Select sunspot coordinates from results-raw file

import os
import csv

rawdata_dir = 'rawdata_to_select/'

filelist = os.listdir(rawdata_dir)

rawdata = []
data = dict() # use dictionary

previous_row = 0

for num in range(0,len(filelist)): # process all files in rawdata_dir
    f = open(rawdata_dir + filelist[num], 'r')
    csvReader = csv.reader(f)
    for row in csvReader:
        rawdata.append(row)
    f.close()
    
    rawdata_index = 0
    for image_num in range(0,int(rawdata[len(rawdata)-1][0])):
        while(int(rawdata[rawdata_index][0]) == image_num):
            data[image_num].append( {rawdata[rawdata_index][3], rawdata[rawdata_index][2]} ) # add coordinates
            rawdata_index += 1
    print(data[1])
    