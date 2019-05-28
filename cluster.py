"""Clustering of weighted points"""
import random
import pprint
from script import (ReferenceFrame, ReadData)

class Cluster:
	def __init__(self, n):
		self.n = n

	def reveal_variables(self):
		print("[*] No of clusters (to be): ", n)

	def get_points_from_names(self, rd, rf):
		points = []
		weights = []
		
		for i in rd.grid_list:
			t = rf.get_coordinate(i)
		
			points.append((t['x'], t['y'], t['w']))

		return points

	def get_clusters(self, data):
		not_converged = True

		# Sample n points randomly | call them centroids
		tmp_idx = random.sample(range(len(data)), self.n)
		tmp_idx.sort()
		centroids = [data[i] for i in tmp_idx]


		# while not_converged:
			


if __name__ == '__main__':

	cl = Cluster(5)
	
	rd = ReadData("Book8.xlsx")
	rf = ReferenceFrame(rd)

	data = cl.get_points_from_names(rd, rf)

	cl.get_clusters(data)