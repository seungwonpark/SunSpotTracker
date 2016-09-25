# SunSpotTracker(WIP)

Sunspots tracking tool based on python.

## track.py

+ Based on Python 3.5.2.
+ Requires scipy, numpy, and matplotlib. I recommend to use [Anaconda](https://www.continuum.io/downloads)
+ Ignore the matplotlib DeprecationError.

Time, latitude, and longtitude will be written in `results.csv`.



## getdata.py

+ Based on Python 2.7.12.
+ Usage : `python track.py startdate enddate hourgap`
+ Example : `python track.py 20160129 20160203 4`

This will save images from [NASA Solar Dynamics Observatory](http://sdo.gsfc.nasa.gov) to `images/` directory. You can also select minimum time gap between images.
**Caution** : Time gap between downloaded images are not identical to the `hourgap` you typed. `hourgap` is just a minimum time gap between images.
