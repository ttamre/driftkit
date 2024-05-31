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


Filename: test_trap.py
Description: Unit test for the trap class
"""

import unittest

from trap import Trap

class TestTrap(unittest.TestCase):

    def test_init(self):
        trap = Trap(
            site_id="TEST_INIT",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )
        self.assertIsNotNone(trap)
        self.assertIsInstance(trap, Trap)
    
    def test_getters(self):
        trap = Trap(
            site_id="TEST_GETTERS",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )
        self.assertEqual(trap.get_direction(), "Southbound")
        self.assertEqual(trap.get_location(), "156 St between 99 - 98 Ave")
        self.assertEqual(trap.get_speed(), 50)
        self.assertEqual(trap.get_coords(), (53.54646216, -113.5085364))
        self.assertEqual(trap.get_distance(), 0.0)

    def test_refresh(self):
        trap = Trap(
            site_id="TEST_REFRESH",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )

        trap.refresh((53.452, -113.51))
        self.assertEqual(trap.distance, 10.5041735513698)

    def test_lt(self):
        trap_1 = Trap(
            site_id="TEST_LT_CLOSER",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )

        trap_2 = Trap(
            site_id="TEST_LT_FARTHER",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(55.38572953, -112.0371643)
        )

        trap_1.refresh((53, -114))
        trap_2.refresh((53, -114))
        self.assertLess(trap_1, trap_2)