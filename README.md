## Clustomer
Raed time customer data analysis platform with results in geo-location clusters

## Installation and Setup

#### From Source
```
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

## How to Troubleshoot
1. **Look in the Logs**: Look in `/logs` folder for the most recent log. The log-files are in a format as `YYYY-MM-DD HH-MM-logfile.log`, i.e., as an example: `2019-07-10 11-46-logfile.log`.

2. If logic halts and application misbehaves, feel free to drop a mail [here](mailto: ankit03june@gmail.com), with a subject starting from `CLUSTOMER ISSUE: <>`. I would be glad to solve it.

## How to View KML Files 

1. KML files can be viewed in Google-Earth PRO
```console
Here is how to download google earth: 
	- Download GEP from [here](https://www.google.com/earth/download/gep/agree.html).
	- Double-click the file and follow the installation process.
	-  To open Google Earth Pro, click Start and then Programs and then Google Earth Pro. Then, click Google Earth Pro.
``` 
2. View it online. This [website](http://kmlviewer.nsspot.net/) would work.
Note: KML files can also be viewed in Google-maps
