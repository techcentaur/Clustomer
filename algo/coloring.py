"""
This file will color the clusters
"""

# from .cluster import *
import sys

class ColorKML:
	# def __init__(self, params):
	# 	"""
	# 	params:
	# 	"""

	# 	self.kml_file_path = params["kml_file_path"]
	# 	self.data_file_path = params["xlsx_file_path"]
	# 	self.number_of_clusters = params["number_of_clusters"]

	# def __repr__(self):
	# 	string = "\n"
	# 	string += "[*] KML-Layer file path: {}\n".format(str(self.kml_file_path))
	# 	string += "[*] Data file path: {}\n".format(str(self.data_file_path))

	def perform_coloring(self, file_name):
		with open(file_name, 'r') as f:
			content = f.readlines()

		content = ("".join(content)).split("\n")

		biglist = {}
		smollist = []

		temp_key = 'no_name'
		for i in content:
			if i.find('<description>') == -1:
				smollist.append(i)
			else:
				biglist[temp_key] = smollist
				temp_key = (i.split("<description>")[1]).split("</description>")[0]
				
				smollist = []
				smollist.append(i)

		self.biglist = biglist
		

	def fill_the_color(self, block, color):
		"""
		block: block number in grid e.g. A34, BF5
		color: color in 4-hex format: FF001122 (alpha-r-g-b)
		"""

		try:
			for idx, i in enumerate(self.biglist[block]):
				if i.find("</fill>") != -1:
					j = i.split("</fill>")
					j[0] = j[0][:-1] + "1"
					j[1] = "<color>{c}</color>".format(c=color) + j[1]
					j = "</fill>".join(j)

					self.biglist[block][idx] = j
					break

		except Exception as e:
			print("[!] Exception Occured: {}".format(e))
			return False

		return True





if __name__ == '__main__':
	c = ColorKML()
	c.perform_coloring(str(sys.argv[1]))