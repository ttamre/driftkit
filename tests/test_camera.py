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
Camera unit tests
-------------------------------------------------------------------------------
"""

import unittest

from api.device import Camera, Device

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
        self.assertIsInstance(camera, Device)
    
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
        self.assertEqual(camera.get_icon(), "📷")

    def test_refresh(self):
        camera = Camera(
            site_id="TEST_REFRESH",
            speed=0,
            direction="",
            location="",
            coords=(53.54646216, -113.5085364)
        )
        camera.refresh((53.385, -113.35))
        self.assertEqual(camera.distance, 20.79587510590846)

    def test_lt(self):
        camera_1 = Camera(
            site_id="TEST_LT_FARTHER",
            speed=0,
            direction="",
            location="",
            coords=(53.54646216, -113.5085364)
        )
        camera_2 = Camera(
            site_id="TEST_LT_CLOSER",
            speed=0,
            direction="",
            location="",
            coords=(50, -100)
        )
        
        camera_1.refresh((50, -100))
        camera_2.refresh((50, -100))
        self.assertGreater(camera_1, camera_2)

    def test_le(self):
        camera_1 = Camera(
            site_id="TEST_LT_FARTHER",
            speed=0,
            direction="",
            location="",
            coords=(53.54646216, -113.5085364)
        )
        camera_2 = Camera(
            site_id="TEST_LT_CLOSER",
            speed=0,
            direction="",
            location="",
            coords=(50, -100)
        )
        camera_3 = Camera(
            site_id="TEST_LT_CLOSER_COPY",
            speed=0,
            direction="",
            location="",
            coords=(50, -100)
        )
        
        camera_1.refresh((50, -100))
        camera_2.refresh((50, -100))
        camera_3.refresh((50, -100))
        self.assertGreaterEqual(camera_1, camera_2)
        self.assertGreaterEqual(camera_2, camera_3)

    def test_eq(self):
        camera_1 = Camera(
            site_id="TEST_EQ_1",
            speed=0,
            direction="",
            location="",
            coords=(53.54646216, -113.5085364)
        )
        camera_2 = Camera(
            site_id="TEST_EQ_2",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        
        camera_1.refresh((50, -100))
        camera_2.refresh((50, -100))
        self.assertEqual(camera_1, camera_2)