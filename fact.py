"""Application Factory"""

import os
import sqlite3
import logging
from datetime import datetime 

from flask import Flask
from _config import yml_data
from flask_cors import CORS

# setup logging handlers
if not os.path.exists("./logs"):
	os.makedirs("./logs")
logfile_name = (str(datetime.now())).rsplit(":", 1)[0].replace(":", "-")
logging.basicConfig(filename="./logs/" + "{}-logfile.log".format(logfile_name), level=logging.DEBUG)
logger = logging.getLogger('LOG')


# flask application initiation
upload_folder = yml_data["path"]["file_upload_folder"]
app = Flask(__name__)
app.secret_key="secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024


# cross-platform headers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# set database connection
if not os.path.exists("./db"):
	os.makedirs("./db")

conn = sqlite3.connect("./db/"+yml_data["database"]["name"])
## create the table if it does not exists
cur = conn.cursor()
cur.execute("select name from sqlite_master where type='table' and name='"+yml_data["database"]["table_name"]+"'")
result = cur.fetchall()

if len(result) == 0:
	cur.execute(''' create table filenames 
			(id INTEGER PRIMARY KEY,
			datafile TEXT NOT NULL,
			kmlfile TEXT NOT NULL,
			time DATETIME)''')
	conn.commit()
	# table created
conn.close()
logger.info("[*] Database connection setup successful!")

# for storing files in pickled form
if not os.path.exists("./datafiles"):
	os.makedirs("./datafiles")
