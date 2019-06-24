"""Application Factory"""

from flask import Flask

upload_folder = "/home/solanki/Code/NOKIA/Clustomer"

app = Flask(__name__)

app.secret_key="secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
