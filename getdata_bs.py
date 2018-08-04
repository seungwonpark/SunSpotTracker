# Based on python 2.7.12 by Seungwon Park
#
# change to python 3.6 by guitar79@gs.hs.kr
# 

target = '1024_HMII.jpg'

import time
from datetime import date, timedelta
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sys import argv
script, starttime, endtime, hourgap = argv # Input : starttime, endtime in '20160901'-like format

#starttime = '20170101'
#endtime = '20170228'
#hourgap = '6'

start_t = time.strptime(starttime, '%Y%m%d')
end_t = time.strptime(endtime, '%Y%m%d')
start_date = date(start_t.tm_year, start_t.tm_mon, start_t.tm_mday)
end_date = date(end_t.tm_year, end_t.tm_mon, end_t.tm_mday)
delta = end_date - start_date
duration = delta.days

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
    return delta.days * 24 + hour + (minute / 60) + (second / 3600) # Calculate days / hour,minute,second sepeartely

site = 'https://sdo.gsfc.nasa.gov'
lastdownloaded = 0

k = 0
while(k <= duration):
    try: # This enables us to try downloading again if temporary network error occurs.
        newdate = start_date + timedelta(k)
        directory = '/assets/img/browse/' + newdate.strftime('%Y') + '/' \
        + newdate.strftime('%m') + '/' + newdate.strftime('%d') + '/'
        url = site + directory
        print ('trying %s ' % url)
        soup = BeautifulSoup(urlopen(url), "html.parser")
        pre_list = soup.find_all('pre')
        file_list = pre_list[0].find_all('a')
        
        for i in range(5, len(file_list)):
            filename = file_list[i].text
            #print ('debug', filename)
            if(filename_to_hour(filename) - lastdownloaded > int(hourgap) - 0.1)\
            and (filename[(-len(target)):] == target): # hour gap between downloading images
                lastdownloaded = filename_to_hour(filename)
                print ('Trying %s' % filename)
                urllib.request.urlretrieve(url+filename, 'images/%s' % filename)
            else:
                print ('Skipping ' + filename)
        k += 1
    except: # TODO : I can't remember the error name... Can anyone tell me?
        print('Temporary downloading error.')
