# from parser import Parser
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Map-Clustering: Clustering customers onto a map given a geo-location.')

	parser.add_argument("-k", "--kml", type=str, help="Geolocation map in kml format")
	parser.add_argument("-x", "--xlsx", type=str, help="Data of customers in excel format")
	parser.add_argument("-c", "--clusters", type=int, default=5, help="Number of clusters")
	args = parser.parse_args()

	# Function called to convert the file
	data = {
		"kml_filepath": args.kml,
		"xlsx_filepath": args.xlsx,
		"clusters": args.clusters
	}

	p = Parser(data)
