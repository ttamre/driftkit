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
Server entrypoint
-------------------------------------------------------------------------------
"""

from flask import Flask, render_template, request
from api.server import *
from api.cli import address_to_coords, refresh_devices

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')


# Main webpage
@app.route('/', methods=['GET'])
def index(devices=[]):

    if request.args:
        
        default_radius = 10

        # Get coordinates from address and convert radius from kilometers to meters
        coords = address_to_coords(location=request.args.get('address', ''), logger=gunicorn_logger)
        radius = float(request.args.get('radius', default_radius) or default_radius) * 1000

        # If we have coordinates, load cameras and traps
        if coords:   
            cameras = load_cameras(coords=coords, radius=radius, logger=gunicorn_logger)
            traps   = load_traps(coords=coords, radius=radius, logger=gunicorn_logger)
            devices = cameras + traps

            # Refresh device distances and sort from closest to farthest
            refresh_devices(devices, coords)
            devices.sort()

            # Log number of devices on successful load
            gunicorn_logger.info(f"Got {len(devices)} devices")

    return render_template('index.html', data=devices)


if __name__ == '__main__':
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(debug=True)