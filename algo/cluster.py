"""Clustering Algorithm"""

import random
import pprint
from .script import (ReferenceFrame, ReadGridData)
from collections import OrderedDict
from pandas import read_excel

class Cluster:
	def __init__(self, n):
		self.n = n

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
		# print("[*] Clustering: ")
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
				# print("[#] Converged at ")
				# print("[.] Converged on", iteration, "iteration and", diff, "difference.")

			iteration += 1
			# break
		self.prev_clusters = prev_clusters

# Can be used as API function
def get_dict(data_frame, no_of_clusters=5):
	cl = Cluster(no_of_clusters)
	
	df = data_frame
	rd = ReadGridData(df)
	rf = ReferenceFrame(rd)

	data = cl.get_points_from_names(rd, rf)
	cl.get_clusters(data)

	dict_data = OrderedDict()
	weight_dict = OrderedDict()

	centroids = sorted(cl.centroids, key=lambda x:x[2], reverse=True)

	for i in range(len(centroids)):
		dict_data[i] = rf.get_names_from_points(cl.prev_clusters[i])
		weight_dict[i] = centroids[i][2]

	return dict_data, weight_dict


class Logic:
	def __init__(self, data_file_path, query, logger):
		self.logger = logger

		if (data_file_path.rsplit(".", 1)[1]).lower() == "xlsx":
			self.df = read_excel(data_file_path)
		else:
			pass

		self.query = query

	def get_query_string(self, query):
		string = ""
		for key in query:
			for jdx, val in enumerate(query[key]):
				string += "( " + str(key) + "==" + str(val) + " )"
				if len(query[key]) > 1:
					if jdx != (len(query[key])-1):
						string += " or "

		return string

	def get_data_frame(self, string=None):
		query = self.query

		if query['type'] == 'discrete':
			return self.df.query(string)
		elif query['type'] == 'date':
			print(":Date")
			return self.df[(self.df[query['col']] >= query['from']) & (self.df[query['col']] <= query['to'])]
		elif query['type'] == 'time':
			print(":Time")
			return self.df[(self.df[query['col']] >= query['from']) & (self.df[query['col']] <= query['to'])]		
		else:
			return self.df
			

