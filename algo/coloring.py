"""
This file will color the clusters
"""

import sys
import seaborn as sns

from .cluster import (get_dict, Logic)
from collections import OrderedDict

class ColorKML:
	def __init__(self, params, logic=None, process=False):
		"""
		params:
		"""

		self.kml_file_path = params["kml_file_path"]
		self.data_file_path = params["data_file_path"]
		self.number_of_clusters = params["number_of_clusters"]


		self.logic = logic 

		if process:
			self.perform_coloring(self.kml_file_path)
			self.color_the_clusters(self.data_file_path, self.number_of_clusters)
			string = ""
			for key in self.biglist:
				string += "\n".join(self.biglist[key])
				string += "\n"

			self.save_file(string, "./output_file.kml")

	def __repr__(self):
		string = "\n"
		string += "[*] KML-Layer file path: {}\n".format(str(self.kml_file_path))
		string += "[*] Data file path: {}\n".format(str(self.data_file_path))

	def perform_coloring(self, file_name):
		with open(file_name, 'r') as f:
			content = f.readlines()

		content = ("".join(content)).split("\n")

		biglist = OrderedDict()
		smollist = []

		temp_key = 'no_name'
		for i in content:
			if i.find('<description>') == -1:
				pass
			else:
				biglist[temp_key] = smollist
				temp_key = (i.split("<description>")[1]).split("</description>")[0]
				
				smollist = []
			smollist.append(i)
		biglist["last_name"] = smollist

		self.biglist = biglist

	def color_argb_list_to_hex(self, list_argb):
		hexcolor = ""
		for i in list_argb:
			j = int(round(i*255))

			hexcolor += (j).to_bytes(1, byteorder='big').hex().upper()
		return "FF"+hexcolor

	def color_the_clusters(self, data_file_path=None, number_of_clusters=None):
		if not data_file_path:
			data_file_path = self.data_file_path
		if not number_of_clusters:
			number_of_clusters = self.number_of_clusters

		data_frame = self.logic.get_data_frame()
		cluster_dict, weight_dict = get_dict(data_frame, number_of_clusters)
		
		# temp = sns.dark_palette("red", n_colors=number_of_clusters, reverse=True)
		temp = sns.cubehelix_palette(n_colors=number_of_clusters, reverse=True)
		color_palettes = [self.color_argb_list_to_hex(list(x)) for x in temp]

		for i, key in enumerate(cluster_dict):
			for block in cluster_dict[key]:
				self.color_the_block(block, color_palettes[i])

		return True


	def color_the_block(self, block, color):
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


	def save_file(self, kml_string, out_file_name):
		"""
		kml_string: kml data in string format
		out_file_name: output kml file name
		"""

		if (out_file_name.rsplit(".", 1)[1]).lower() !='kml':
			out_file_name += ".kml"

		try:
			with open(out_file_name, 'w') as f:
				f.write(kml_string)
		except Exception as e:
			print("[!] Exception Occured: {}".format(e))
			return False
		return True



if __name__ == '__main__':
	data={
	"kml_file_path": "./3G_mumbai_grid_WK18.kml",
	"data_file_path": "./Book8.xlsx",
	"number_of_clusters": 5
	}
	c = ColorKML(data, process=True)
