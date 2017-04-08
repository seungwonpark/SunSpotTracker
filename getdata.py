# Based on python 2.7.12
target = '1024_HMII.jpg'

import httplib
import time
from datetime import date, timedelta
from sys import argv
script, starttime, endtime, hourgap = argv # Input : starttime, endtime in '20160901'-like format
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


headers = {'User-agent': 'Python'}
conn = httplib.HTTPConnection('sdo.gsfc.nasa.gov')
lastdownloaded = 0

k = 0
while(k <= duration):
    try: # This enables us to try downloading again if temporary network error occurs.
        newdate = start_date + timedelta(k)
        directory = '/assets/img/browse/' + newdate.strftime('%Y') + '/' + newdate.strftime('%m') + '/' + newdate.strftime('%d') + '/'
        print 'Parsing ' + directory + '...'
        conn.request('GET', directory, '', headers)
        resp = conn.getresponse()
        html = resp.read()
        print(html)
        html_split = html.split(target)
        for i in range(1, len(html_split), 2):
            filename = html_split[i].replace('">', '') + target
            if(filename_to_hour(filename) - lastdownloaded > int(hourgap) - 0.1): # hour gap between downloading images
                lastdownloaded = filename_to_hour(filename)
                print 'Downloading ' + filename
                conn.request('GET', directory + filename, '', headers)
                resp = conn.getresponse()
                image = resp.read()
                f = open('images/' + filename, 'wb')
                f.write(image)
            else:
                print 'Skipping ' + filename
        k += 1
    except: # TODO : I can't remember the error name... Can anyone tell me?
        print('Temporary downloading error.')
