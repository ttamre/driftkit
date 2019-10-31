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


Filename: trap.py
Description: Source file to the Trap class
"""

class Trap:
    def __init__(self, direction, location, speed):
        """
        :param direction    str     Direction the camera is facing (NB, SB, EB, WB) (Converted into full text on initialization)
        :param location     str     Location of the camera (address)
        :param speed        int     Speed limit of the camera
        """
        self.direction = self._format_direction(direction)
        self.location = location
        self.speed = speed
        self.order = {"Northbound": 1, "Southbound": 2, "Eastbound": 3, "Westbound": 4}

    def get_direction(self):
        return self.direction
        
    def get_location(self):
        return self.location

    def get_speed(self):
        return self.speed

    def _format_direction(self, direction):
        '''
        Parameter(s):   direction<>
        Return:         value<string>
        '''
        mappings = {"NB": "Northbound", "EB": "Eastbound", "SB": "Southbound", "WB": "Westbound"}
        return mappings[direction]

    def __lt__(self, other):
        '''
        Comparator method
        NOTE: Should be changed to use GPS coordinates and the haversine formula for comparisons
        '''
        return self.order[self.direction] < other.order[other.direction]

    def __repr__(self):
        return "{}\n  {}\n  Posted Speed: {} kilometres\n".format(self.location, self.direction, self.speed)