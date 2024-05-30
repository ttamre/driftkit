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
INTERSECTION_CAMERAS = "https://data.edmonton.ca/resource/7fnd-72gr.json"
SPEEDTRAP_ZONES = "https://data.edmonton.ca/resource/akzz-54k3.json"

import sys
import time
import requests

from camera import Camera
from trap import Trap


def menu():
    print("-" * 70)
    print("Driftkit Copyright (C) 2019 Tem Tamre")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; view LICENSE for details.")
    print("-" * 70, end="")
    print(r"""
 _____  _____  _____ ______ _______ _  _______ _______ 
|  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
| |  | | |__) | | | | |__     | |  | ' /  | |    | |   
| |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
| |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
|_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 """)
    print("-" * 70)

    # Load all cameras and traps
    cameras = load_cameras()
    traps = load_traps()

    # Get the user's current position and max distance
    position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
    refresh_all(cameras, position)

    limit = float(input("Max radius (0 for no limit) > "))
    print_cameras(cameras, limit=limit)

    while True:
        print("Options: refresh, lite, traps, quit")
        end_ui = input("> ")

        # Refresh user position and/or max distance
        if end_ui.startswith("r"):
            position = float(input("Current Latitude > ")), float(input("Current Longitude > "))
            refresh_all(cameras, position)

            limit = float(input("Max radius (0 for no limit) > "))
            print_cameras(cameras, limit=limit)

        # Lite mode
        elif end_ui.startswith("l"):
            refresh_all(cameras, position)
            print_cameras(cameras, lite=True, limit=limit)

        # Display speed traps
        elif end_ui.startswith("t"):
            refresh_all(traps, position)
            print_traps(traps)

        # Quit the program
        elif end_ui.startswith("q"):
            sys.exit()
    

def load_cameras():
    '''
    Fetch the intersection cameras from the City of Edmonton API and return a list of Camera() objects
    '''
    response = requests.get(INTERSECTION_CAMERAS)
    if response.status_code == 200:
        cameras = []
        for camera in response.json():
            cameras.append(
                Camera(
                    site_id   = camera['site_id'],
                    speed     = int(camera['posted_speed'].split(" ")[0]),
                    direction = camera['travel_direction'],
                    location  = "{} {}".format(camera['approach'], camera['cross_street']),
                    coords    = (float(camera['latitude']), float(camera['longitude']))
                ))
        return cameras


def load_traps():
    '''
    Fetch the speed trap zones from the City of Edmonton API and return a list of Trap() objects
    '''
    response = requests.get(SPEEDTRAP_ZONES)
    if response.status_code == 200:
        traps = []
        for trap in response.json():
            traps.append(
                Trap(
                    site_id   = trap['site_id'],
                    speed     = int(trap['speed_limit']),
                    direction = trap['location_description'][0:2],
                    location  = trap['location_description'][3:],
                    coords    = (float(trap['latitude']), float(trap['longitude']))
                ))
        return traps


def print_cameras(cameras:list, lite:bool=False, limit:int=0):
    '''
    Print a list of all the cameras, in order of closest to farthest from the user

    :param  cameras     list of Camera() objects
    :param  lite        true = condensed output, false = verbose output
    :param  limit       Max distance from the user to display cameras for
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


def print_traps(traps:list):
    '''
    Print a list of all the traps, in order of closest to farthest from the user

    :param  traps  list of Trap() objects
    '''
    traps.sort()
    print("-" * 70)
    for trap in traps:
        print(trap)
    print("-" * 70)


def refresh_all(items:list, position:tuple):
    '''
    Update all camera distances with our current position

    :param  items       list of Camera() or Trap() objects (NOTE: Must have a refresh() class method)
    :param  position    current position of the user
    '''
    for item in items:
        item.refresh(position)