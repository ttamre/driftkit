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


Filename: test_camera.py
Description: Unit test for the camera class
"""

import unittest

from camera import Camera

class TestCamera(unittest.TestCase):
    def test_init(self):
        camera = Camera(
            site_id="TEST_INIT",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        self.assertIsNotNone(camera)
        self.assertIsInstance(camera, Camera)
    
    def test_getters(self):
        camera = Camera(
            site_id="TEST_GETTERS",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        self.assertEqual(camera.get_location(), "109 Street at 104 Avenue")
        self.assertEqual(camera.get_direction(), "Southbound")
        self.assertEqual(camera.get_speed(), 50)
        self.assertEqual(camera.get_coords(), (53.54646216, -113.5085364))
        self.assertEqual(camera.get_distance(), 0.0)

    def test_refresh(self):
        camera = Camera(
            site_id="TEST_REFRESH",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        camera.refresh((53.385, -113.35))
        self.assertEqual(camera.distance, 20.79587510590846)

    def test_lt(self):
        camera_1 = Camera(
            site_id="TEST_LT_FARTHER",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        camera_2 = Camera(
            site_id="TEST_LT_CLOSER",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(50, -100)
        )
        
        camera_1.refresh((50, -100))
        camera_2.refresh((50, -100))
        self.assertGreater(camera_1, camera_2)