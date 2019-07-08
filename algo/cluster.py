"""Weighted Clustering Algorithm and Support for Logical Queries from Dataframe"""


from random import sample
from pandas import read_excel
from collections import OrderedDict

from .script import (ReferenceFrame, ReadGridData)

class Cluster:
	"""
	@params: n(int): Number of clusters to be formed
	"""
	def __init__(self, n):
		self.n = n

	def get_points_from_names(self, rd, rf):
		"""Get a list of points as a tuple of (x-cord, y-cord, weight) where x-cord and y-cord are based on `rf` reference frame.
		With input as the grid_list public attribute from `rd` object.

		@params: rd (object): ReadGridData
				 rf (object): ReferenceFrame
		"""
		points = []
		
		for i in rd.grid_list:
			t = rf.get_coordinate(i)
		
			points.append((t['x'], t['y'], t['w']))
		return points

	def get_clusters(self, data):
		"""	Run clustering algorithm and save the result in self as below written attributes.
			self.centroids: The last calculated centroids
			self.prev_clusters: The last formed clusters

			@params: data: List of all points in a format (x-cord, y-cord, weight) or as an output of public method of this class: `get_points_from_names()`
		"""
		def weighted_distance(i, j):
			""" weighted distance: (((j[0] - i[0])**2 + (j[1] - i[1])**2)/(j[2] + i[2]))**0.5
				@params: i, j: tuples with (x-cord, y-cord, weight)
			"""
			return (((j[0] - i[0])**2 + (j[1] - i[1])**2)/(j[2] + i[2]))**0.5

		not_converged = True

		# CENTROIDS: Sample n points randomly | call them centroids
		tmp_idx = sample(range(len(data)), self.n)
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
		while not_converged:
			for i in range(len(self.centroids)):
				self.old_centroids[i] = self.centroids[i]

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

			if diff < 0.01:
				not_converged = False

			iteration += 1
		self.prev_clusters = prev_clusters

		return True

# Can be used as a direct API function in back-end logic
def get_dict(data_frame, no_of_clusters):
	"""	Run clustering algorithm and get data in the form of dicts:

		1. Create ReadGridData and ReferenceFrame object with give dataframe as data
		2. Run `get_clusters` function from Cluster with the data
		3. Form ordered dict information from the calculated clusters

		@params:
		`data_frame` (pandas dataframe): Data
		`no_of_clusters` (int): No of clusters to be formed

		@return: (Both dicts are `OrderedDict`)
		`weight_dict`: weights of the centroids in decreasing order
		`dict_data`: corresponding grid names of the x, y coordinates
	"""
	cl = Cluster(no_of_clusters)
	
	rd = ReadGridData(data_frame)
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
	"""Support wrapper for query logic from pandas dataframe"""
	def __init__(self, data_file_path, query, logger):
		""" Read excel data and set up self attributes

			@params: data_file_path: file path of the excel data file
					 query: query as a dict in particular format (look for app.py doc for more)
					 logger: logger object for logs
		"""
		self.logger = logger

		if (data_file_path.rsplit(".", 1)[1]).lower() == "xlsx":
			self.df = read_excel(data_file_path)
		else:
			pass

		self.query = query

	def get_query_string(self, query):
		""" If the query is of type discrete convert it to a dataframe support query
			for e.g. [4, 5, 6] -> (col==4 | col==5 | col==6) for a column col

			@params: query: dict with column as keys
		"""

		string = ""
		for key in query:
			for jdx, val in enumerate(query[key]):
				string += "( " + str(key) + "==" + str(val) + " )"
				
				if len(query[key]) > 1:
					if jdx != (len(query[key])-1):
						string += " or "

		return string

	def get_data_frame(self):
		"""

		"""

		query = self.query

		if query['type'] == 'discrete':
			query.pop("type", None)
			return self.df.query(self.get_query_string(query))
		elif query['type'] == 'date':
			return self.df[(self.df[query['col']] >= query['from']) & (self.df[query['col']] <= query['to'])]
		elif query['type'] == 'time':
			return self.df[(self.df[query['col']] >= query['from']) & (self.df[query['col']] <= query['to'])]		
		else:
			return self.df
			

