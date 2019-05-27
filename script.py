import pandas as pd 
from collections import Counter
import re

	
class ReferenceFrame:
	"""
	Form a Reference frame:
	Usage:
	`get_coordinate(name)`: Get a dict of x and y coordinates
	"""

	def __init__(self, x_min, y_name_list):
		self.x_min = x_min

		self.y_name_list = {}
		for idx, l in enumerate(y_name_list):
			self.y_name_list[l] = idx

	def __str__(self):
		"""string representation of class"""

		ret = ""
		ret += "Origin Shift X: " + str(self.x_min) + "\n"
		ret += "Origin Map Y: " + str(self.y_name_list) + "\n"
		return ret

	def get_coordinate(self, name):
		"""get coordinate from the name of grid: G34 (e.g.)"""
		
		tmp = re.split('(\d.*)', name)
		
		x = int(tmp[1]) - self.x_min
		y = self.y_name_list[tmp[0]]

		return {'x': x, 'y': y}


class ReadData:
	"""read data from a xlsx file"""
	
	def __init__(self, file_name):
		dfe = pd.read_excel(file_name)
		val = list(dfe['Grid'])

		grids = []
		for l in val:
			if type(l) is not float:
				grids.append(l)

		c_grids = Counter(grids)
		grid_list = sorted(c_grids)

		len4 = []
		len3 = []

		for l in grid_list:
			if (len(l)) == 3:
				len3.append(l)
			else:
				len4.append(l)
		
		d3 = self.max_and_min(len3)
		d4 = self.max_and_min(len4)
		min_glob = min(d3['min'], d4['min'])

		self.min_glob = min_glob
		self.names_list = d3['names'] + d4['names']

	def max_and_min(self, _list):
		"""Find max and min from a give list"""

		len3_new = []
		lister = []
		for l in _list:
			tmp = re.split('(\d.*)', l)
			len3_new.append(int(tmp[1]))
			lister.append(tmp[0])

		return {'max': (max(len3_new)), 'min': (min(len3_new)), 'names': sorted(list(set(lister)))}


rd = ReadData("Book8.xlsx")
rf = ReferenceFrame(rd.min_glob, rd.names_list)
