"""For Displaying KML script using Google Maps JS API"""

from _config import yml_data

from fact import app
from flask import render_template

@app.route('/')
def display():
	return render_template('display.html')

if __name__ == '__main__':
	app.run()