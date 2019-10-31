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


Filename: test_building.py
Description: Unit test for the building class
"""

import unittest

from building import Building

class TestBuilding(unittest.TestCase):
    def test_init(self):
        building = Building(
            key='csc',
            name='Computing Science Center',
            lat=53.526757,
            lon=-113.529391
        )
        assert building
        assert isinstance(building, Building)

    def test_getters(self):
        building = Building(
            key='csc',
            name='Computing Science Center',
            lat=53.526757,
            lon=-113.529391
        )
        assert building.get_key() == 'csc'
        assert building.get_name() == 'Computing Science Center'
        assert building.get_lat() == 53.526757
        assert building.get_lon() == -113.529391
        assert building.get_coords() == (53.526757, -113.529391)