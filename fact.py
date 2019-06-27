"""Application Factory"""

from flask import Flask
from _config import yml_data

from flask_cors import CORS

upload_folder = yml_data["path"]["upload_folder"]

app = Flask(__name__)

app.secret_key="secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

