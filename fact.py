"""Application Factory"""

import sqlite3
from flask import Flask
from _config import yml_data
from flask_cors import CORS

upload_folder = yml_data["path"]["upload_folder"]

# flask application initiation
app = Flask(__name__)
app.secret_key="secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

# cross-platform headers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# database connection
conn = sqlite3.connect(yml_data["database"]["name"])

## create the table if it does not exists
cur = conn.cursor()
cur.execute("select name from sqlite_master where type='table' and name='"+yml_data["database"]["table_name"]+"'")
result = cur.fetchall()

if len(result) == 0:
	cur.execute(''' create table filenames 
			(id INTEGER PRIMARY KEY,
			kmlfile TEXT NOT NULL,
			datafile TEXT NOT NULL,
			time DATETIME)''')
	conn.commit()
	# table created