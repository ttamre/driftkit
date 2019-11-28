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
        trap = Trap(50, "SB", "156 St between 99 - 98 Ave", 50)
        assert trap
        assert isinstance(trap, Trap)
    
    def test_getters(self):
        trap = Trap(50, "SB", "156 St between 99 - 98 Ave", 50)
        assert trap.get_direction() == "Southbound"
        assert trap.get_location() == "156 St between 99 - 98 Ave"
        assert trap.get_speed() == 50

    def test_lt(self):
        trap_1 = Trap(50, "SB", "156 St between 99 - 98 Ave", 50)
        trap_2 = Trap(50, "WB", "156 St between 158 - 160 St", 50)
        assert trap_1 < trap_2