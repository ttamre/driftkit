#!/usr/bin/env python3

"""
Driftkit - Edmonton intersection camera and speed zone tracker
Copyright (C) 2019 Tem Tamre

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


Filename: driftkit.py
Description: Main file for the driftkit program

Data from the City of Edmonton open data portal
https://data.edmonton.ca/Transportation/Intersection-Safety-Device-Locations-Map/fwx6-by2r

References:
https://docs.python.org/3.6/library/csv.html
https://stackoverflow.com/a/40283805
"""
__author__ = "Tem Tamre"
__email__ = "ttamre@ualberta.ca"

DEBUG = False
INTERSECTION_CAMERAS = "https://data.edmonton.ca/api/views/fwx6-by2r/rows.csv?accessType=DOWNLOAD"
SPEEDTRAP_ZONES = "https://data.edmonton.ca/api/views/akzz-54k3/rows.csv?accessType=DOWNLOAD"

import os
import sys
import csv
import time
import datetime
import requests
import socket
from haversine import haversine
from flask import Flask, render_template, abort

from camera import Camera
from trap import Trap


def menu():
    '''
    Display the menu that the user will see and interact with

    Parameter(s):   None
    Return:         None
    '''
    print("\nDriftkit Copyright (C) 2019 Tem Tamre")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; view LICENSE for details.\n")
    print("-" * 70)
    print("""\
  _____  _____  _____ ______ _______ _  _______ _______ 
 |  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
 | |  | | |__) | | | | |__     | |  | ' /  | |    | |   
 | |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
 | |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
 |_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 """)

    # Update all relevant .csv files
    update()

    # Load all cameras and traps
    cameras = load_cameras()
    traps = load_traps()

    ui = input("Would you like to use the terminal or the webserver interface?\n> ").lower()
    if ui.startswith("t"):
        position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
        refresh_all(cameras, position)

        limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
        print_cameras(cameras, limit=limit)

        while True:
            print("Options: refresh, lite, traps, quit")
            end_ui = input("> ")

            if end_ui.startswith("r"):
                position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
                refresh_all(cameras, position)

                limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
                print_cameras(cameras, limit=limit)

            elif end_ui.startswith("l"):
                position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
                refresh_all(cameras, position)

                limit = float(input("Enter max distance to display cameras from (0 for no limit) > "))
                print_cameras(cameras, lite=True, limit=limit)

            elif end_ui.startswith("t"):
                print_traps(traps)

            elif end_ui.startswith("q"):
                sys.exit()
    
    elif ui.startswith("w"):
        if sys.version_info[0] == 3:
            app.run(debug=DEBUG)
    else:
        print("Unrecognized input")
    

def load_cameras(filename="assets/intersections.csv"):
    '''
    Load a list of intersection cameras based on the file at the given filename

    Parameter(s):   filename<string>            Path of file to load and parse
    Return:         camera_list<list><Camera>   List of intersection cameras that were found in filename
    '''
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


def load_traps(filename="assets/traps.csv"):
    '''
    Load a list of speed trap zones based on the file at the given filename

    Parameter(s):   filename<string>        Path of file to load and parse
    Return:         trap_list<list><Trap>   List of speed trap zones that were found in filename
    '''
    trap_list = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader, None)  # Skip the header

        for row in csvreader:
            direction = row[0][0:2]
            location = row[0][2::]
            speed = row[1]
            trap = Trap(direction, location, speed)
            trap_list.append(trap)
    
    return trap_list


def print_cameras(cameras, lite=False, limit=0):
    '''
    Print a list of all the cameras, in order of closest to farthest from the user

    Parameter(s):   cameras<list><Camera>   The cameras that we're printing
                    lite (default=False)    True for condensed output
                    limit (default=0)       Number of cameras to print (0 means no limit)
    Return:         None
    '''
    cameras.sort()
    print("-" * 70)
    if lite:
        for i in range(len(cameras)):
            distance = cameras[i].get_distance()
            if limit == 0 or distance <= limit:
                print("Camera {}) {} kilometres ({}, {})".format("%02d" % (i+1), "%.3f" % cameras[i].get_distance(), cameras[i].get_speed(), cameras[i].get_direction()))
                time.sleep(0.01)
        print("-" * 70)
    else:
        for camera in cameras:
            if limit == 0 or camera.get_distance() <= limit:
                print(camera)
                time.sleep(0.01)
    print("-" * 70)


def print_traps(traps):
    '''
    Print a list of all the traps, in order of closest to farthest from the user

    Parameter(s):   traps<list><Trap>   The traps that we're printing
    Return:         None

    NOTE: Sorting needs to be tested, might be an issue with Trap.__lt__() and Trap.location
    '''
    traps.sort()
    print("-" * 70)
    for trap in traps:
        print(trap)
    print("-" * 70)


def refresh_all(cameras, position):
    '''
    Update all camera distances with our current position

    Parameter(s):   position<tuple><float>  Current position of the user
    Return:         None
    '''
    for camera in cameras:
        camera.refresh(position)

    print("-" * 70)
    print("Data refreshed")
    print("-" * 70)
    time.sleep(0.5)


def internet():
    '''
    Try to establish a connection to google.ca to ensure internet connectivity

    Parameter(s):   None
    Return:         True if a connection was established, false otherwise
    '''
    try:
        socket.create_connection(("www.google.ca", 80))
        return True
    except OSError:
        return False


def update():
    '''
    If an internet connection is able to be established, compare our data to the data in the data portal
    If there are any differences, take the version on the data portal and overwrite our data with it

    Parameter(s):   None
    Return:         None

    NOTE: The datasets used in this application are updated weekly. Just to be sure, this program will check every time it's run
    '''
    print("-" * 70)
    if internet():
        print("Checking for update...")
        intersection_request = requests.get(INTERSECTION_CAMERAS, timeout=3)
        intersection_current = open("assets/intersections.csv", "rb").read()

        trap_request = requests.get(SPEEDTRAP_ZONES, timeout=3)
        trap_current = open("assets/traps.csv", "rb").read()
        
        if intersection_request.content != intersection_current:
            open("assets/intersections.csv", "wb").write(intersection_request.content)
            now = datetime.datetime.now()
            print("Intersection data updated as of {}".format(now.strftime("%Y-%m-%d")))
        else:
            print("Intersection data already up to date")
        
        if trap_request.content != trap_current:
            open("assets/traps.csv", "wb").write(trap_request.content)
            now = datetime.datetime.now()
            print("Speed trap data updated as of {}".format(now.strftime("%Y-%m-%d")))
        else:
            print("Speed trap data already up to date")

    else:
        print("Internet connection required to update...")
        print("Data may be inaccurate - make sure to update weekly")
    print("-" * 63)


# ==================================================
# Flask Webserver (Incomplete - for version 2)
# ==================================================
app = Flask(__name__)

class building:
    def __init__(self, key, name, lat, lon):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lon  = lon

buildings = (
    building('csc',  "Computing Science Center", 53.526757,-113.529391),
    building('ccis', "Centennial Centre for Interdisciplinary Sciences", 53.5281605,-113.526836),
    building('etlc', "Engineering Teaching and Learing Complex", 53.5273485,-113.53189768),
    building('echa', "Edmonton Clinic Health Academy", 53.5223334,-113.5283363),
    building('tory', "Tory Lecture Hall", 53.5282782,-113.5235847),
    building('sub',  "Students' Union Building", 53.5252652,-113.5293874),
    building('bus',  "Alberta School of Business", 53.5273542,-113.5227988),
    building('foot', "Foote Field", 53.5023045,-113.5284634)
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