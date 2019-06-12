## Map-Clustering

## Usage

### Dependencies
	- Run `pip3 install -r requirements.txt` to install required modules
	- Copy the gdaltools folder to `/usr/local/bin/python3.6/dist-pacakages`

#### `python3 main.py -h`
```console
usage: main.py [-h] [-k KML] [-x XLSX] [-c CLUSTERS]

Map-Clustering: Clustering customers onto a map given a geo-location.

optional arguments:
  -h, --help            show this help message and exit
  -k KML, --kml KML     Geolocation map in kml format
  -x XLSX, --xlsx XLSX  Data of customers in excel format
  -c CLUSTERS, --clusters CLUSTERS
                        Number of clusters

```

*Example usage:* `python3 main.py --kml 3G_mumbai_grid_WK18.kml  --xlsx Book8.xlsx -c 5`


### Files

#### `script.py`

```python
class ReadData:
	"""To read data from an xlsx file
		And return one possible mapping params
		X-shift:
		Y-Mapping:
	"""
	pass

class ReferenceFrame:
	"""Take params of ReadData as input:
	And functions for refrenece data
	"""
	pass

```

#### `cluster.py`

Use `get_dict(no_of_clusters)` public function in `cluster.py` to use as an API and get clusters returned in dictionary.

#### `parser.py`

```python

def convert_KML_2_GeoJSON(filename):
	"""This will convert the KML file to GeoJSON"""

def update_Geo_JSON(filename):
	"""Changing the opacity and restructring the whole JSON tree"""

def convert_KML_2_GeoJSON(filename):
	"""This will convert the GeoJSON file to KML. Clusters are colored"""

def modify_kml_according_to_clusters(filename):
	"""It take clusters and points from KML as input and colors the grid accordingly """
```
