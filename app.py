"""Application"""

import os
import sqlite3
import urllib.request

import requests
from copy import deepcopy
from pandas import read_excel
from datetime import datetime

from werkzeug.utils import secure_filename
from flask import (flash, request, redirect, render_template, url_for, Response)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from fact import (app, logger)
from algo import (coloring, cluster, github_wrapper)

from _config import yml_data

allowed_extension = set(yml_data["allowed_extension"])

# Global
kml_file_name = ""
data_file_name = ""
data_file_frame = None


def allowed_file(filename):
	return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in allowed_extension)


@app.route('/', methods=["POST", "GET"])
def upload_file():
	global kml_file_name, data_file_name
	if request.method=='POST':
		postdata = (request.form).to_dict(flat=False)
		if 'datafilename' in postdata:
			# Second form: Filenames were chosen
			kml_file_name = secure_filename(str(postdata['kmlfilename']))
			filename = secure_filename(str(postdata['datafilename']))
			data_file_name = filename

			return redirect(url_for('select_content', filename=filename))
		elif 'outfilefromdb' in postdata:
			ofname = secure_filename(str(postdata['outfilefromdb']))
			return redirect(url_for('result_page', out_file_name=ofname))

		else:
			# First form: New files were uploaded			
			if 'datafile' not in request.files or 'kmlfile' not in request.files:
				flash('Some file-part not submitted in form!')
				return redirect(request.url)

			file = request.files['datafile']
			file2 = request.files['kmlfile']

			if file.filename=="" or file2.filename=="":
				flash('Null file selected for uploading!')
				return redirect(request.url)

			if (file and allowed_file(file.filename)) and (file2 and allowed_file(file2.filename)):
				filename = secure_filename(file.filename)
				kml_file_name = secure_filename(file2.filename)
				data_file_name = filename

				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				file2.save(os.path.join(app.config['UPLOAD_FOLDER'], kml_file_name))
				logger.warn("[.] File names securely parsed, and files saved in configured directory")

				# registering in data base
				conn = sqlite3.connect("./db/" + yml_data["database"]["inputfilesDB"]["name"])
				cur = conn.cursor()
				cur.execute("insert into filenames values (null, ?, ?, ?)", (filename, kml_file_name, datetime.now(), ))
				conn.commit()
				conn.close()
				logger.info("[.] Entry registered in data-base!")
				
				flash('File(s) successfully uploaded!')
				return redirect(url_for('select_content', filename=filename))
			else:
				flash("Allowed extensions are: {}".format(str(allowed_extension)))
				return redirect(request.url)
	else:
		conn = sqlite3.connect("./db/" + yml_data["database"]["inputfilesDB"]["name"])
		cur = conn.cursor()
		cur.execute("select * from filenames")
		query_data = cur.fetchall()
		conn.close()
		
		conn = sqlite3.connect("./db/" + yml_data["database"]["outputfilesDB"]["name"])
		cur = conn.cursor()
		cur.execute("select * from filenames")
		query_data_2 = cur.fetchall()
		conn.close()
		
		data = {'datafilenames': [], 'kmlfilenames': [], 'time': [], 'ofnames': []}
		for r in query_data:
			data['datafilenames'].append(r[1])
			data['kmlfilenames'].append(r[2])
			data['time'].append(str(r[3]).rsplit(":", 1)[0])

		for r in query_data_2:
			data['ofnames'].append(r[3])

		data['length'] = len(data['datafilenames'])
		data['olength'] = len(data['ofnames'])

		return render_template('upload.html', data=data)

@app.route('/select/<filename>', methods=['GET', 'POST'])
def select_content(filename):
	if request.method=='POST':
		geogrid = request.form.get('geogrid')
		column = request.form.get('column')
		
		return redirect(url_for('select_values', filename=filename, grid=geogrid, col=column))
	else:
		global data_file_frame
		df = read_excel(app.config['UPLOAD_FOLDER'] + "/" + filename)
		
		columns = list(df.columns)
		data_file_frame = deepcopy(df)

		if len(columns) == 0:
			flash('File has not data! Please enter a file with data')
			return redirect('/')

		data = {
			'flag': 0,
			'columns': columns,
			'selected_column': columns[0]}

		try:
			idx = columns.index('Grid')
		except:
			idx = 0
		data['selected_column_grid'] = columns[idx]
		
		return render_template('selection.html', data=data)

@app.route('/select/<filename>/<grid>/<col>/', methods=['POST', 'GET'])
def select_values(filename, grid, col):
	global data_file_frame
	if request.method=='POST':
		clusters = request.form.get('num_clusters')
		logger.debug("[*] {c} column selected: With {i} number of clusters to form:".format(c=col, i=clusters))

		data={
			"data_file_path": app.config['UPLOAD_FOLDER'] + "/" + filename,
			"kml_file_path": app.config['UPLOAD_FOLDER'] + "/" + kml_file_name,
			"number_of_clusters": int(clusters)
		}

		val = []
		for i in set(list(data_file_frame[col])):
			if request.form.get(str(i)):
				val.append(i)
		query = {col: val}

		logic = cluster.Logic(data["data_file_path"], query, logger)
		c = coloring.ColorKML(data, logger=logger, logic=logic, process=True)

		return redirect(url_for('result_page', out_file_name=c.get_saved_outfile_name()))
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

@app.route('/result_page/<out_file_name>', methods=["GET"])
def result_page(out_file_name):
	global kml_file_name, data_file_name

	try:
		if request.args.get('to_save') == 'true':
			conn = sqlite3.connect("./db/" + yml_data["database"]["outputfilesDB"]["name"])
			cur = conn.cursor()
			cur.execute("insert into filenames values (null, ?, ?, ?, ?)", (data_file_name, kml_file_name, out_file_name, datetime.now()))
			conn.commit()
			conn.close()
	except:
		logger.critical("[!] Cannot save the outfile")

	download_url = yml_data["host"]["url"] + "/api/v1/" + out_file_name
	save_url = yml_data["host"]["url"] + "/result_page/" + out_file_name + "?to_save=true"
	
	data = {
		"download_url": download_url,
		"out_file_name": out_file_name,
		"save_url": save_url
	}

	return render_template('result.html', data=data)


@app.route('/kml_viewer/<out_file_name>', methods=["GET"])
def show_kml(out_file_name):
	data={
        "user": yml_data["github"]["handle"],
        "password": yml_data["github"]["password"],
        "repo": yml_data["github"]["repo"],
        "branch": yml_data["github"]["branch"],
        "to_be_uploaded_file_list": ["./outfiles/" + out_file_name],
        "commit_message": None,
	}

	github_url = "https://raw.githubusercontent.com/"+data["user"]+"/"+data["repo"]+"/"+data["branch"]+"/"+out_file_name
	api_url = "https://maps.googleapis.com/maps/api/js?key="+ yml_data["api"]["google_maps_js"] +"&callback=initMap"
	download_url = yml_data["host"]["url"] + "/api/v1/" + out_file_name
	save_url = yml_data["host"]["url"] + "/kml_viewer/" + out_file_name + "?to_save=true"
	
	payload = {
		"github_url": github_url,
		"api_url": api_url,
		"download_url": download_url,
		"save_url": save_url
	}
	
	try:
		if request.args.get('to_save') == 'true':
			conn = sqlite3.connect("./db/" + yml_data["database"]["outputfilesDB"]["name"])
			cur = conn.cursor()
			cur.execute("insert into filenames values (null, ?, ?, ?, ?)", (data_file_name, kml_file_name, out_file_name, datetime.now(),))
			conn.commit()
			conn.close()

			return render_template('display.html', data=payload)
	except:
		logger.critical("[!] Cannot save the outfile")

	logger.debug("""[#] Google Maps API use kml file on a public server:
	By-passing it through GitHub raw user content:""")

	logger.info("[*] Posting KML via GitHub api")
	logger.debug("[*] Data {}\n".format(str(data)))

	github_wrapper.post_on_github(data, logger)

	return render_template('display.html', data=payload)

# api = Api(app)

# class APIs(Resource):
@app.route('/api/v1/<filename>', methods=["GET"])
def get(filename):
	headers = {'Content-Type': 'text/xml'}
	with open("./outfiles/" + filename) as kml:
		data = kml.read()

	resp = Response(response=data, status=200, mimetype="application/vnd.google-earth.kml+xml")
	return resp 

# api.add_resource(APIs, '/api/v1/out.kml')

if __name__=="__main__":
	app.run(host="0.0.0.0")
