#!/usr/bin/env python3

"""
Filename: driftkit.py

Description: Intersection camera detector for the city of Edmonton

References:
https://docs.python.org/3.6/library/csv.html
https://stackoverflow.com/a/40283805

TODO
- sort cameras by closest distance (Haversine?)
- give approx. distance to nearest camera (Haversine?)
"""
__author__ = "Tem Tamre"
__email__ = "ttamre@ualberta.ca"

DEBUG = True

import os
import sys
import csv
import time
import datetime
import requests
import socket
from haversine import haversine
from flask import Flask, render_template, abort


def menu():
    print("-" * 60)
    print("""\
  _____  _____  _____ ______ _______ _  _______ _______ 
 |  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
 | |  | | |__) | | | | |__     | |  | ' /  | |    | |   
 | |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
 | |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
 |_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 """)
    print("-" * 60)
    update()
    print("-" * 60)

    data = load_csv()

    ui = input("Would you like to use the terminal or the webserver interface?\n> ").lower()
    if ui.startswith("t"):
        refresh(data)
        print_data(data)
    elif ui.startswith("w"):
        if sys.version_info[0] == 3:
            app.run(debug=DEBUG)


def internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


def update():
    if internet():
        print("Checking for update...")
        url = "https://data.edmonton.ca/api/views/fwx6-by2r/rows.csv?accessType=DOWNLOAD"
        
        r = requests.get(url, timeout=3)
        current = open("assets/data.csv", "rb").read()
        
        if r.content != current:
            open("assets/data.csv", "wb").write(r.content)
            now = datetime.datetime.now()
            print("Data updated as of {}".format(now.strftime("%Y-%m-%d")))
        else:
            print("Data already up to date")
    else:
        print("Internet connection required to update...")
        print("Data may be inaccurate - make sure to update weekly")


def load_csv(filename="assets/data.csv"):
    datadict = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader, None)  # Skip the header
        for row in csvreader:
            site_id = row[0]
            enforcement = row[1]
            location = "{} {}".format(row[2], row[3])
            direction = row[4]
            speed = row[5]
            coordinates = (float(row[6]), float(row[7]))
            distance = None
            datadict[site_id] = [enforcement, location, direction, speed, coordinates, distance]
    
    return datadict

def refresh(datadict):
    # Add a distance value to each dictionary
    # position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
    position = (53.56979565, -113.4521125)

    for site in datadict:
        site_distance = datadict[site][4]
        datadict[site][5] = haversine(position, site_distance)

    print("-" * 60)
    print("Data refreshed")
    print("-" * 60)
    time.sleep(1)

def print_data(datadict):

    for site in datadict:
        print("Site {site}:\t{location} ({direction})".format(
            site=site, location=datadict[site][1], direction=datadict[site][2]))
        print("\t\tPosted speed: {speed}".format(speed=datadict[site][3]))
        print("\t\tGPS Coordinates: {coords}".format(coords=datadict[site][4]))
        print("\t\tApproximate distance away: {distance} kilometres\n".format(distance="%.2f" % datadict[site][5]))
        


# ==================================================
# Flask Webserver
# ==================================================
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

if __name__ == "__main__":
    menu()