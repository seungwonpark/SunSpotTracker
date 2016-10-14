# SunSpotTracker

Sunspots tracking tool based on python.

## track.py

+ Based on Python 3.5.2.
+ Requires scipy, numpy, and matplotlib. I recommend to use [Anaconda](https://www.continuum.io/downloads).
+ Usage : `python track.py 1`
+ If you don't want to use plot utility, then `python track.py 0 0`.
+ If you want to parse data as raw coordinates, tehn `python track.py 0 1`.
+ Ignore the matplotlib DeprecationError.

Time, latitude, and longtitude will be written in `results.csv`.



## getdata.py

+ Based on Python 2.7.12.
+ Usage : `python track.py startdate enddate hourgap`
+ Example : `python track.py 20160129 20160203 4`

This will save images from [NASA Solar Dynamics Observatory](http://sdo.gsfc.nasa.gov) to `images/` directory. You can also select minimum time gap between images.

Please refer to [Data Rights and Rules for Data Use](http://sdo.gsfc.nasa.gov/data/rules.php) and attribute as :

> "Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams."

**Caution** : Time gap between downloaded images are **not identical** to the `hourgap` you typed. `hourgap` is just a minimum time gap between images.
