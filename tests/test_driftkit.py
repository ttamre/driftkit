"""
Driftkit - Edmonton intersection camera and speed zone tracker
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


Filename: test_driftkit.py
Description: Unit test for functions in driftkit.py
"""

import driftkit
import unittest

from camera import Camera
from trap import Trap

CAMERAS = [
        Camera(site_id="TEST_PRINT_1", speed=0, direction="", location="", coords=(50.54646216, -113.5085364)),
        Camera(site_id="TEST_PRINT_2", speed=0, direction="", location="", coords=(50.44646216, -113.7085364)),
        Camera(site_id="TEST_PRINT_3", speed=0, direction="", location="", coords=(50.44646216, -113.7185364)),
        Camera(site_id="TEST_PRINT_4", speed=0, direction="", location="", coords=(50.44646216, -114.0085364)),
        Camera(site_id="TEST_PRINT_5", speed=0, direction="", location="", coords=(51.44646216, -114.2085364))
]

TRAPS = [
        Trap(site_id="TEST_PRINT_1", speed=0, direction="", location="", coords=(50.54646216, -113.5085364)),
        Trap(site_id="TEST_PRINT_2", speed=0, direction="", location="", coords=(50.44646216, -113.7085364)),
        Trap(site_id="TEST_PRINT_3", speed=0, direction="", location="", coords=(50.44646216, -113.7185364)),
        Trap(site_id="TEST_PRINT_4", speed=0, direction="", location="", coords=(50.44646216, -114.0085364)),
        Trap(site_id="TEST_PRINT_5", speed=0, direction="", location="", coords=(51.44646216, -114.2085364))
]

class TestDriftkit(unittest.TestCase):

    def test_load_cameras(self):
        # Returns a populated list on 200 response code, empty list otherwise
        self.assertIsInstance(driftkit.load_cameras(), list)

    def test_load_traps(self):
        # Returns a populated list on 200 response code, empty list otherwise
        self.assertIsInstance(driftkit.load_traps(), list)

    # No return values to test, just checking for crashes or thrown errors
    def test_print_cameras(self):
        self.assertIsNone(driftkit.print_cameras(cameras=CAMERAS, lite=True))
        self.assertIsNone(driftkit.print_cameras(cameras=CAMERAS, lite=False))
        self.assertIsNone(driftkit.print_cameras(cameras=[], lite=True))
        self.assertIsNone(driftkit.print_cameras(cameras=[], lite=False))

    
    # No return values to test, just checking for crashes or thrown errors
    def test_print_traps(self):
        self.assertIsNone(driftkit.print_traps(traps=TRAPS))
        self.assertIsNone(driftkit.print_traps(traps=[]))

    def test_refresh_all(self):
        # No return values to test, just checking for crashes or thrown errors
        self.assertIsNone(driftkit.refresh_all(items=CAMERAS, location=(50, -113)))
        self.assertIsNone(driftkit.refresh_all(items=TRAPS, location=(50, -113)))

    # @unittest.skip("geopy ssl error")
    def test_address_to_coords(self):
        # Returns a tuple of floats on valid address, None otherwise
        self.assertIsNotNone(driftkit.address_to_coords("109 Street 107 Ave, Edmonton, Alberta, Canada"))
        self.assertRaises(AttributeError, driftkit.address_to_coords, "")