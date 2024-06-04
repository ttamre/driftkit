#!/usr/bin/env python3

"""
-------------------------------------------------------------------------------
Driftkit - yeg speed camera and speed zone locator
Copyright (C) 2024 Tem Tamre

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
API functionality
-------------------------------------------------------------------------------
"""

import requests
import logging
import time

from api.device import Camera, Trap
from api.cli import CAMERA_URL, TRAP_URL


def load_cameras(coords, radius, logger=logging.getLogger(__name__)):
    '''
    Fetch the intersection cameras from the City of Edmonton API and return a list of Camera() objects

    :param coords       tuple       GPS coordinates of the user (lat:float, lon:float)
    :param radius       str/int     Search radius (in metres)
    :param logger       logger      Logging object
    '''

    cameras = []

    url = f"{CAMERA_URL}?$where=within_circle(geo_location, {coords[0]}, {coords[1]}, {radius})"
    response = requests.get(url)

    if response.status_code == 200:        
        for camera in response.json():
            cameras.append(
                Camera(
                    site_id   = camera['site_id'],
                    speed     = int(camera['posted_speed'].split(" ")[0]),
                    direction = camera['travel_direction'],
                    location  = "{} {}".format(camera['approach'], camera['cross_street']),
                    coords    = (float(camera['latitude']), float(camera['longitude'])),
                ))
    else:
        logger.error(f"server.load_cameras(): got {response.status_code} from data.edmonton.ca")
        logger.error(response.text)

    return cameras


def load_traps(coords, radius, logger=logging.getLogger(__name__)):
    '''
    Fetch the speed trap zones from the City of Edmonton API and return a list of Trap() objects

    :param coords       tuple       GPS coordinates of the trap zone (lat:float, lon:float)
    :param radius       str/int     Search radius (in metres)
    :param logger       logger      Logging object
    '''

    traps = []

    url = f"{TRAP_URL}?$where=within_circle(geo_location, {coords[0]}, {coords[1]}, {radius})"
    response = requests.get(url)

    if response.status_code == 200:

        for trap in response.json():
            traps.append(
                Trap(
                    site_id   = trap['site_id'],
                    speed     = int(trap['speed_limit']),
                    direction = trap['location_description'][0:2],
                    location  = trap['location_description'][3:],
                    coords    = (float(trap['latitude']), float(trap['longitude'])),
                ))
    else:
        logger.error(f"server.load_traps(): got {response.status_code} from data.edmonton.ca")
        logger.error(response.text)

    return traps