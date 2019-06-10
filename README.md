## Map-Clustering

### Classes
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

### Usage

```console
gavy42@jarvis:~$ python3 -i script.py
>>> rf.get_coordinate('R24')
{'x': 5, 'y': 0}
>>> 
```

Use `get_dict(no_of_clusters)` public function in `cluster.py` to use as an API and get clusters returned in dictionary.