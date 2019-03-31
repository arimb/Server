from flask import Flask, jsonify, render_template
from district_points.district_points import recalc
import csv

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/getDistrictPoints/<year>')
def district_points(year):
    try:
        data = {}
        with open("district_points/" + str(year) + ".csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                team = row.pop("Team")
                data[team] = dict(row)
        print("hit")
        return jsonify(data)
    except FileNotFoundError:
        return jsonify(recalc(year))

#@app.route('/district_points')
#def render_district_points():
#    return render_template('district_points.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
