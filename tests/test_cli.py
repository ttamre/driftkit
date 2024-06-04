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
CLI unit tests
-------------------------------------------------------------------------------
"""

import sys
import logging
import unittest


from api import cli
from api.device import Camera, Trap


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logging.disable(logging.CRITICAL)  # Disable logging for tests


CAMERAS = [ # Only used for printing tests
        Camera(site_id="TEST_CAM_1", speed=0, direction="", location="", coords=(50.54646216, -113.5085364)),
        Camera(site_id="TEST_CAM_2", speed=0, direction="", location="", coords=(50.44646216, -113.7085364)),
        Camera(site_id="TEST_CAM_3", speed=0, direction="", location="", coords=(50.44646216, -113.7185364)),
        Camera(site_id="TEST_CAM_4", speed=0, direction="", location="", coords=(50.44646216, -114.0085364)),
        Camera(site_id="TEST_CAM_5", speed=0, direction="", location="", coords=(51.44646216, -114.2085364))
]

TRAPS = [   # Only used for printing tests
        Trap(site_id="TEST_TRAP_1", speed=0, direction="", location="", coords=(50.54646216, -113.5085364)),
        Trap(site_id="TEST_TRAP_2", speed=0, direction="", location="", coords=(50.44646216, -113.7085364)),
        Trap(site_id="TEST_TRAP_3", speed=0, direction="", location="", coords=(50.44646216, -113.7185364)),
        Trap(site_id="TEST_TRAP_4", speed=0, direction="", location="", coords=(50.44646216, -114.0085364)),
        Trap(site_id="TEST_TRAP_5", speed=0, direction="", location="", coords=(51.44646216, -114.2085364))
]

class TestDriftkit(unittest.TestCase):

    def test_load_cameras(self):
        # Returns a populated list on 200 response code, empty list otherwise
        cameras = cli.load_all_cameras(logger=logger)
        self.assertIsInstance(cameras, list)
        list(map(lambda camera: self.assertIsInstance(camera, Camera), cameras))

    def test_load_traps(self):
        # Returns a populated list on 200 response code, empty list otherwise
        traps = cli.load_all_traps(logger=logger)
        self.assertIsInstance(traps, list)
        list(map(lambda trap: self.assertIsInstance(trap, Trap), traps))

    # No return values to test, just checking for crashes or thrown errors
    def test_print_cameras(self):
        self.assertIsNone(cli.print_cameras(cameras=CAMERAS, lite=True))
        self.assertIsNone(cli.print_cameras(cameras=CAMERAS, lite=False))
        self.assertIsNone(cli.print_cameras(cameras=[], lite=True))
        self.assertIsNone(cli.print_cameras(cameras=[], lite=False))

    
    # No return values to test, just checking for crashes or thrown errors
    def test_print_traps(self):
        self.assertIsNone(cli.print_traps(traps=TRAPS))
        self.assertIsNone(cli.print_traps(traps=[]))

    def test_refresh_all(self):
        # No return values to test, just checking for crashes or thrown errors
        self.assertIsNone(cli.refresh_devices(devices=CAMERAS, coords=(50, -113)))
        self.assertIsNone(cli.refresh_devices(devices=TRAPS, coords=(50, -113)))

    def test_address_to_coords_valid(self):
        # Returns a tuple of floats on valid address, None otherwise
        coords = cli.address_to_coords(location="109 Street 107 Ave", logger=logger)
        expected = (53.5513149, -113.5077588)

        self.assertIsNotNone(coords)
        self.assertIsInstance(coords, tuple)
        self.assertIsInstance(coords[0], float)
        self.assertIsInstance(coords[1], float)
        self.assertEqual(coords, expected)

    def test_address_to_coords_invalid(self):
        # Returns None on empty or invalid address
        self.assertIsNone(cli.address_to_coords(location="", logger=logger))
        self.assertIsNone(cli.address_to_coords(location="INVALID-ADDRESS", logger=logger))
        self.assertIsNone(cli.address_to_coords(location=":INVALID_LATITUDE INVALID_LONGITUDE", logger=logger))