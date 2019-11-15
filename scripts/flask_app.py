
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/district_points/<endpoint>')
def district_points(endpoint):
    return send_from_directory('/home/arimb/district_points', endpoint+'.json');

@app.route('/wlt/<endpoint>')
def wlt(endpoint):
    return send_from_directory('/home/arimb/wlt', endpoint+'.json');

@app.route('/hexafecta')
def hexafecta():
    return send_from_directory('/home/arimb/', 'hexafecta.json');

