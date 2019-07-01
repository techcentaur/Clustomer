from algo import cluster
import pandas as pd

if __name__ == '__main__':
	q = {"LTR": [3, 5, 6]}
	l = cluster.Logic("./Book8.xlsx", q)
	df = l.get_data_frame()
	print(df.head())