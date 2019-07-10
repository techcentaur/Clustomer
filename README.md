# Clustomer
Real time customer data analysis platform with results in geo-location clusters mapped on KML file (can be viewed in Google Maps)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Installation and Setup

#### From Source
```
1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Application is ready to be used. See Usage section.
```

#### From Docker-image
```
```

## Usage

#### Using as a Web-App
```bash
solanki@bhavya:~/NOKIA/Clustomer$ python3 app.py --flask
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

#### Using CLU (Command Line Utility)
```bash
solanki@bhavya:~/NOKIA/Clustomer$ python3 app.py -h
usage: app.py [-h] (-flask | -clu) [-k KML] [-x XLSX] [-c CLUSTERS]

Clustomer: Clustering customers onto a map in KML given a geo-location in Excel data format

optional arguments:
  -h, --help            show this help message and exit
  -flask, --flask       Run flask app
  -clu, --clu           Use command line utility
  -k KML, --kml KML     Geolocation map in kml format
  -x XLSX, --xlsx XLSX  Data of customers in excel format
  -c CLUSTERS, --clusters CLUSTERS
                        Number of clusters

```

#### Using from Python
```python3
>>> import logging
>>> logging.basicConfig(filename="somefile.log", level=logging.DEBUG)
>>> logger = logging.getLogger('LOG')
>>>
>>> from algo import *
>>> data = {
...     "data_file_path": "f1.xlsx",
...     "kml_file_path": "f2.kml",
...     "number_of_clusters": 5
... }
>>> logic = cluster.Logic(args.xlsx, query={}, logger=logger)
>>> c = coloring.ColorKML(data, logger=logger, logic=logic, process=True)
[*] File saved as updated_f2.kml

```
_Note_: Look into documentation to know how to gain more manual control with `process=False`

## How to Troubleshoot
1. **Look in the Logs**: Look in `/logs` folder for the most recent log. The log-files are in a format as `YYYY-MM-DD HH-MM-logfile.log`, i.e., as an example: `2019-07-10 11-46-logfile.log`.

2. If logic halts and application misbehaves, feel free to drop a mail [here](mailto:ankit03june@gmail.com), with a subject starting from `CLUSTOMER ISSUE: <>`. I would be glad to solve it.

## How to View KML Files 

1. KML files can be viewed in Google-Earth PRO

	- Here is how to download google earth: 
		- Download GEP from [here](https://www.google.com/earth/download/gep/agree.html).
		- Double-click the file and follow the installation process.
		-  To open GEP, click _Start_ and then _Programs_ and then _Google Earth Pro_. Then, click Google Earth Pro.
 
2. View it online: This [website](http://kmlviewer.nsspot.net/) would work.

_Note_: KML files can also be viewed in Google-maps
