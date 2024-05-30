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
        assert camera
        assert isinstance(camera, Camera)
    
    def test_getters(self):
        camera = Camera(
            site_id="TEST_GETTERS",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        assert camera.get_location() == "109 Street at 104 Avenue"
        assert camera.get_direction() == "Southbound"
        assert camera.get_speed() == 50
        assert camera.get_coords() == (53.54646216, -113.5085364)
        assert camera.get_distance() == None

    def test_refresh(self):
        camera = Camera(
            site_id="TEST_REFRESH",
            speed=50,
            direction="Southbound",
            location="109 Street at 104 Avenue",
            coords=(53.54646216, -113.5085364)
        )
        new_position = (50, -100)
        camera.refresh(new_position)
        assert camera.get_distance() == 1007.6272078568426

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
        assert camera_1 > camera_2