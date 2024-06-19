#!/usr/bin/env python3

"""
-------------------------------------------------------------------------------
Driftkit - yeg speed camera and speed zone locator
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
-------------------------------------------------------------------------------
CLI interface
-------------------------------------------------------------------------------
"""
__author__ = "Tem Tamre"
__email__ = "temtamre@gmail.com"


import os
import sys
import time
import requests
import certifi
import ssl
import logging
import geopy.geocoders

from api.device import Camera, Trap


# Environment variables
APP_TOKEN = os.environ['DRIFTKIT_APP_TOKEN']
SECRET_TOKEN = os.environ['DRIFTKIT_SECRET_TOKEN']

# API endpoints
CAMERA_URL = f"https://data.edmonton.ca/resource/7fnd-72gr.json"
TRAP_URL = f"https://data.edmonton.ca/resource/akzz-54k3.json"

# Defining our logger here and initializing it later when file is ran
# to avoid wasting memory on imports
cli_logger = None
# Functions that require a logger can have one passed as an argument 


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
    cameras = load_all_cameras()
    traps = load_all_traps()


    # Get the user's address and max distance
    coords = None
    while not coords:
        coords = address_to_coords(location=input("Location > "))

    refresh_devices(cameras, coords)

    limit = float(input("Max radius (0 for no limit) > "))
    print_cameras(cameras, limit=limit)

    while True:
        print("Options: refresh, lite, traps, quit")
        end_ui = input("> ")

        # Refresh user location and max distance
        if end_ui.startswith("r"):
            coords = None
            while not coords:
                coords = address_to_coords(input("Location > "))

            refresh_devices(cameras, coords)

            limit = float(input("Max radius (0 for no limit) > "))
            print_cameras(cameras, limit=limit)

        # Lite mode (condensed output)
        elif end_ui.startswith("l"):
            print_cameras(cameras, lite=True, limit=limit)

        # Display speed traps
        elif end_ui.startswith("t"):
            refresh_devices(traps, coords)
            print_traps(traps)

        # Quit the program
        elif end_ui.startswith("q"):
            sys.exit()
    

def load_all_cameras(logger=cli_logger):
    '''
    Fetch the intersection cameras from the City of Edmonton API and return a list of Camera() objects
    '''

    cameras = []
    response = requests.get(CAMERA_URL)

    if response.status_code == 200:
        for camera in response.json():
            cameras.append(
                Camera(
                    site_id   = camera['site_id'],
                    speed     = int(camera['posted_speed'].split(" ")[0]),
                    direction = camera['travel_direction'],
                    location  = "{} {}".format(camera['approach'], camera['cross_street']),
                    coords    = (float(camera['latitude']), float(camera['longitude']))
                ))
    else:
        logger.error(f"cli.load_all_cameras(): got {response.status_code} from data.edmonton.ca")
        logger.error(response.text)

    return cameras


def load_all_traps(logger=cli_logger):
    '''
    Fetch the speed trap zones from the City of Edmonton API and return a list of Trap() objects
    '''
    traps = []
    response = requests.get(TRAP_URL)
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
    else:
        logger.error(f"cli.load_all_traps(): got {response.status_code} from data.edmonton.ca")
        logger.error(response.text)
    
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


def refresh_devices(devices, coords):
    '''
    Refresh the distance of all devices in the list
    :param devices  list    List of Device() objects
    :param coords   tuple   GPS coordinates of the user (latitude, longitude)
    '''
    list(map(lambda device: device.refresh(coords), devices))


def address_to_coords(location:str, logger=cli_logger):
    '''
    If given an address, converts it to GPS coordinates (floats)
    If given coordinates, returns them as floats

    NOTE: This only works for the city of Edmonton, Alberta, Canada
    since the only data source is the Edmonton Open Data Portal

    :param  location    str     Address or coordinates
    :return             tuple   GPS coordinates (latitude, longitude)
                                or None if address is invalid
    '''
    if not location:
        logger.error("cli.address_to_coords(): invalid input (no location provided)")
        return None

    # If address starts with a colon, it's a coordinate
    if location.startswith(":"):
        lat, lon = location[1:].split(" ")[0], location[1:].split(" ")[1]
        try:
            return float(lat), float(lon)
        except ValueError:
            logger.error(f"cli.address_to_coords(): invalid coordinates ({location})")
            return None

    context = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = context

    geolocator = geopy.geocoders.Nominatim(user_agent="driftkit")
    coords = geolocator.geocode(f"{location}, Edmonton, Alberta, Canada")

    if not coords:
        logger.error(f"cli.address_to_coords(): geopy couldn't find coordinates for {location}")
        return None

    return coords.latitude, coords.longitude

if __name__ == "__main__":
    cli_logger = logging.getLogger(__name__)
    menu()