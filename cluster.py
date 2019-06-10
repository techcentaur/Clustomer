"""Clustering of weighted points"""
import random
import pprint
from script import (ReferenceFrame, ReadData)

class Cluster:
	def __init__(self, n):
		self.n = n

	def reveal_variables(self,n):
		print("[*] No of clusters (to be): ", n)

	def get_points_from_names(self, rd, rf):
		points = []
		
		for i in rd.grid_list:
			t = rf.get_coordinate(i)
		
			points.append((t['x'], t['y'], t['w']))
		return points

		

	def get_clusters(self, data):
		def weighted_distance(i, j):
			return (((j[0] - i[0])**2 + (j[1] - i[1])**2)/(j[2] + i[2]))**0.5

		not_converged = True

		# CENTROIDS: Sample n points randomly | call them centroids
		tmp_idx = random.sample(range(len(data)), self.n)
		tmp_idx.sort()

		self.centroids = [data[i] for i in tmp_idx]
		self.old_centroids = [0 for i in tmp_idx]
		prev_clusters = [[] for i in tmp_idx]
		next_clusters = [[] for i in tmp_idx]

		# form intitial clusters
		for i in data:
			dist = []
			for j in self.centroids:
				dist.append(weighted_distance(i, j))
			prev_clusters[dist.index(min(dist))].append(i)


		iteration = 0
		print("[*] Clustering: ")
		while not_converged:
			# calculate new centroids
			for i in range(len(self.centroids)):
				self.old_centroids[i] = self.centroids[i]
			# print(self.old_centroids)
			# print(self.centroids)

			for i in range(len(prev_clusters)):
				sumx, sumy, sumw = 0, 0, 0
				for j in range(len(prev_clusters[i])):
					sumx += prev_clusters[i][j][2] * prev_clusters[i][j][0]
					sumy += prev_clusters[i][j][2] * prev_clusters[i][j][1]
					sumw += prev_clusters[i][j][2]

				self.centroids[i] = ((sumx/sumw), sumy/sumw, sumw/len(prev_clusters[i]))
	
			# form new clusters
			for i in data:
				dist = []
				for j in self.centroids:
					dist.append(weighted_distance(i, j))
				next_clusters[dist.index(min(dist))].append(i)

			# check convergence condition
			diff = 0
			for i in range(len(self.centroids)):
				diff += ((self.centroids[i][0] - self.old_centroids[i][0])**2 + (self.centroids[i][1] - self.old_centroids[i][1])**2)**0.5

			for i in range(len(self.centroids)):
				prev_clusters[i] = next_clusters[i]
				next_clusters[i] = []
				# self.old_centroids[i] = self.centroids[i]


			# print(diff)
			if diff < 0.01:
				not_converged = False
				print("[#] Converged at ")
				print("[.] Iteration: ", iteration, " with difference ", diff)

			iteration += 1
			# break
		self.prev_clusters = prev_clusters

# Can be used as API function
def get_dict(no_of_clusters=5):
	cl = Cluster(no_of_clusters)
	
	rd = ReadData("Book8.xlsx")
	rf = ReferenceFrame(rd)

	data = cl.get_points_from_names(rd, rf)
	cl.get_clusters(data)

	dict_data = {}
	for i in range(len(cl.centroids)):
		dict_data[i] = rf.get_names_from_points(cl.prev_clusters[i])
	return dict_data

