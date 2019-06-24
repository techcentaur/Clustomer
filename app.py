"""Application"""

import os

import urllib.request
from werkzeug.utils import secure_filename
from flask import flash, request, redirect, render_template, url_for

from fact import app

allowed_extension = set(['pdf'])

def allowed_file(filename):
	return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in allowed_extension)

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method=='POST':
		if 'file' not in request.files:
			flash('No File-part Submitted!')
			return redirect(request.url)

		file = request.files['file']
		if file.filename=="":
			flash('Null File Selected for Uploading!')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			flash('File successfully completed!')
			return redirect('/')
		else:
			flash("Allowed types are: {}".format(str(allowed_extension)))
			return redirect(request.url)

if __name__=="__main__":
	app.run(debug=True)