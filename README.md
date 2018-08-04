# SunSpotTracker

# IMPORTANT : `getdata.py` Currently not working., Please use `getdata_bs.py`.


Sunspots tracking tool based on python. `track.py`, `getdata_bs.py`, and `selectdata.py`.

## track.py

+ Based on Python3
+ Requires scipy, numpy, and matplotlib. I recommend to use [Anaconda](https://www.continuum.io/downloads).
+ First, place the images that you want to track at `images/` directory.
+ Recommended default usage : `python track.py 1 0`
+ If you don't want to use plot utility, then `python track.py 0 0`.
+ If you want to parse data as raw coordinates, tehn `python track.py 0 1`. Rawdata files are needed for using `selectdata.py`.
+ Results are written to `results/` directory.
+ Ignore the matplotlib DeprecationError.

Time, latitude, and longitude will be written in `results.csv`.
In `track.py`, each pixels of sunspot aren't abstracted to one point. If you want to use such utility, make rawdata files and use `selectdata.py`.


## getdata_bs.py : New version of getdata.py

+ Based on Python3
+ Requires BeautifulSoup. I recommend to use [Anaconda](https://www.continuum.io/downloads).
+ Usage : `python getdata_bs.py startdate enddate hourgap`
+ Example : `python getdata.py 20160129 20160203 4`
+ This will save images from [NASA Solar Dynamics Observatory](http://sdo.gsfc.nasa.gov) to `images/` directory. You can also select minimum time gap between images.
+ Please refer to [Data Rights and Rules for Data Use](http://sdo.gsfc.nasa.gov/data/rules.php) and attribute as :

> "Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams."

**Caution** : Time gap between downloaded images are **not identical** to the `hourgap` you typed. `hourgap` is just a minimum time gap between images.

## selectdata.py

+ Based on Python3
+ First, place the rawdata `*.csv` files to `rawdata_to_select/` directory. (You can put multiple files!)
+ Then, dfs-processed data will be written to `selected/` directory.


