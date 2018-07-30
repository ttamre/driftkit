from flask import Flask, render_template, abort
app = Flask(__name__)

class building:
    def __init__(self, key, name, lat, lon):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lon  = lon

buildings = (
    building('csc',  "Computing Science Center", 53.5267138, -113.5293044),
    building('ccis', "Centennial Centre for Interdisciplinary Sciences", 53.5281621, -113.5279304),
    building('etlc', "Engineering Teaching and Learing Complex", 53.5273883, -113.5316418)
)

buildings_by_key = {building.key: building for building in buildings}

@app.route('/')
def index():
    return render_template('index.html', buildings=buildings)

@app.route("/<building_code>")
def show_building(building_code):
    building = buildings_by_key.get(building_code)
    if building:
        return render_template('map.html', building=building)
    else:
        abort(404)

app.run(debug=True)