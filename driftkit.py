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
import platform
import datetime
import requests
import socket
from haversine import haversine
from flask import Flask, render_template, abort


def menu():
    print("-" * 70)
    print("""\
  _____  _____  _____ ______ _______ _  _______ _______ 
 |  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
 | |  | | |__) | | | | |__     | |  | ' /  | |    | |   
 | |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
 | |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
 |_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 """)

    update()

    cameras = load_data()

    ui = input("Would you like to use the terminal or the webserver interface?\n> ").lower()
    if ui.startswith("t"):
        position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
        refresh_all(cameras, position)

        limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
        print_all(cameras, limit=limit)

        while True:
            print("Options: refresh, lite, quit")
            end_ui = input("> ")

            if end_ui.startswith("r"):
                position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
                refresh_all(cameras, position)

                limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
                print_all(cameras, limit=limit)

            elif end_ui.startswith("l"):
                position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
                refresh_all(cameras, position)

                limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
                print_all(cameras, lite=True, limit=limit)

            elif end_ui.startswith("q"):
                sys.exit()
        
    
    elif ui.startswith("w"):
        if sys.version_info[0] == 3:
            app.run(debug=DEBUG)
    else:
        print("Unrecognized input")



# ==================================================
# Main functionality
# ==================================================
class Camera:
    def __init__(self, site_id, enforcement, location, direction, speed, coords, distance=None):
        self.site_id = site_id
        self.enforcement = enforcement
        self.location = location
        self.direction = direction
        self.speed = speed
        self.coords = coords
        self.distance = distance

    def refresh(self, position):
        self.distance = haversine(position, self.coords)

    def get_distance(self):
        return self.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        s = """Site {site}:\t{location} ({direction})
        \tPosted speed: {speed}
        \tGPS Coordinates: {coords}
        \tApproximate distance away: {distance} kilometres\n
        """.format(
            site = self.site_id,
            location = self.location,
            direction = self.direction,
            speed = self.speed,
            coords = self.coords,
            distance = "%.3f" % self.distance
        )

        return s


def load_data(filename="assets/data.csv"):
    camera_list = []
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
            camera = Camera(site_id, enforcement, location, direction, speed, coordinates, distance)
            camera_list.append(camera)
    
    return camera_list



# ==================================================
# Network functions
# ==================================================
def internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


def update():
    print("-" * 70)
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
    print("-" * 70)



# ==================================================
# Iterative functions
# ==================================================
def refresh_all(cameras, position):
    for camera in cameras:
        camera.refresh(position)

    print("-" * 70)
    print("Data refreshed")
    print("-" * 70)
    time.sleep(0.5)


def print_all(cameras, lite=False, limit=0):
    cameras.sort()
    print("-" * 70)
    if lite:
        for i in range(len(cameras)):
            if limit == 0 or cameras[i].distance <= limit:
                print("Camera {}) {} kilometres ({}, {})".format("%02d" % (i+1), "%.3f" % cameras[i].distance, cameras[i].speed, cameras[i].direction))
                time.sleep(0.01)
        print("-" * 70)
    else:
        for camera in cameras:
            if limit == 0 or camera.distance <= limit:
                print(camera)
                time.sleep(0.01)
    print("-" * 70)



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