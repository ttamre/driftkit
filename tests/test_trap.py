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
        assert trap
        assert isinstance(trap, Trap)
    
    def test_getters(self):
        trap = Trap(
            site_id="TEST_GETTERS",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )
        assert trap.get_direction() == "Southbound"
        assert trap.get_location() == "156 St between 99 - 98 Ave"
        assert trap.get_speed() == 50

    def test_refresh(self):
        trap = Trap(
            site_id="TEST_REFRESH",
            speed=50,
            direction="SB",
            location="156 St between 99 - 98 Ave",
            coords=(53.54646216, -113.5085364)
        )

        trap.refresh((53, -113))
        assert trap.distance

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
        assert trap_1 < trap_2