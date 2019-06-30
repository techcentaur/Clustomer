"""Application"""

import os
import urllib.request

import requests
from copy import deepcopy
from pandas import read_excel
from werkzeug.utils import secure_filename
from flask import (flash, request, redirect,
                   render_template, url_for, Response)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from fact import app
from algo import (coloring, cluster, github_wrapper)

from _config import yml_data

allowed_extension = set(yml_data["allowed_extension"])

# Global
kml_file_name = ""
data_file_frame = None


def allowed_file(filename):
	return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in allowed_extension)


@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'datafile' not in request.files or 'kmlfile' not in request.files:
			flash('Some file-part not submitted in form!')
			return redirect(request.url)

		file = request.files['datafile']
		file2 = request.files['kmlfile']

		if file.filename == "" or file2.filename == "":
			flash('Null file selected for uploading!')
			return redirect(request.url)

		if (file and allowed_file(file.filename)) and (file2 and allowed_file(file2.filename)):
			filename = secure_filename(file.filename)
			global kml_file_name
			kml_file_name = secure_filename(file2.filename)

			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file2.save(os.path.join(app.config['UPLOAD_FOLDER'], kml_file_name))

			flash('File(s) successfully uploaded!')
			return redirect(url_for('select_content', filename=filename))
		else:
			flash("Allowed extensions are: {}".format(str(allowed_extension)))
			return redirect(request.url)


@app.route('/select/<filename>', methods=['GET', 'POST'])
def select_content(filename):
	if request.method == 'POST':
		geogrid = request.form.get('geogrid')
		column = request.form.get('column')

		return redirect(url_for('select_values', filename=filename, grid=geogrid, col=column))
	
	else:
		global data_file_frame
		
		df = read_excel(filename)
		
		columns = list(df.columns)
		data_file_frame = deepcopy(df)

		if len(columns) == 0:
			flash('File has not data! Please enter a file with data')
			return redirect('/')

		data = {
		'flag': 0,
		'selected_column': columns[0],
		'columns': columns,
		'selected_column_grid': columns[0]
		}
		return render_template('selection.html', data=data)

@app.route('/select/<filename>/<grid>/<col>/', methods=['POST', 'GET'])
def select_values(filename, grid, col):
	global data_file_frame
	if request.method=='POST':
		clusters = request.form.get('val')

		data={
		"kml_file_path": "./3G_mumbai_grid_WK18.kml",
		"data_file_path": "./Book8.xlsx",
		"number_of_clusters": 5
		}
		val = []
		for i in set(list(data_file_frame[col])):
			if request.form.get(str(i)):
				val.append(i)

		query = {col: val}

		logic = cluster.Logic(data["data_file_path"], query)
		c = coloring.ColorKML(data, logic=logic, process=True)

		return redirect(url_for('show_kml'))
	else:
		columns = list(data_file_frame.columns)

		if len(columns) == 0:
			flash('File has not data! Please enter a file with data')
			return redirect('/')

		data = {
		'flag': 1,
		'selected_column': col,
		'columns': columns,
		'selected_column_grid': grid,
		'col_values': set(list(data_file_frame[col]))
		}

		return render_template('selection.html', data=data)

@app.route('/kml_viewer', methods=["GET"])
def show_kml():
	data={
        "user": yml_data["github"]["handle"],
        "password": yml_data["github"]["password"],
        "repo": yml_data["github"]["repo"],
        "branch": yml_data["github"]["branch"],
        "to_be_uploaded_file_list": ["./output_file.kml"],
        "commit_message": None,
        "verbose": True,
	}
	print(data)

	github_wrapper.post_on_github(data)
	url = "https://raw.githubusercontent.com/"+data["user"]+"/"+data["repo"]+"/"+data["branch"]+"/"+"output_file.kml"

	return render_template('display.html', github_url=url, api=yml_data["api"]["google_maps_js"])

# api = Api(app)

# class APIs(Resource):
@app.route('/api/v1/out.kml', methods=["GET"])
def get():
	headers = {'Content-Type': 'text/xml'}
	with open("./output_file.kml") as kml:
		data = kml.read()

	resp = Response(response=data, status=200, mimetype="application/vnd.google-earth.kml+xml")
	return resp 

# api.add_resource(APIs, '/api/v1/out.kml')

if __name__=="__main__":
	app.run(host="0.0.0.0", port=5000)
