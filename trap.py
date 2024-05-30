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

from haversine import haversine

class Trap:

    MAPPINGS = {"NB": "Northbound", "EB": "Eastbound", "SB": "Southbound", "WB": "Westbound"}

    def __init__(self, site_id, speed, direction, location, coords, distance=None):
        """
        :param site_id      str     Site ID of the speed trap zone
        :param speed        int     Speed limit of the speed trap zone
        :param direction    str     Direction of the road that approaches the trap zone
        :param location     str     Address of the trap zone
        :param coords       tuple   GPS coordinates of the trap zone(latitude, longitude)
        :param distance     float   Approximate distance between the user and the trap zone
        """
        self.site_id = site_id
        self.direction = self.MAPPINGS[direction]
        self.location = location
        self.coords = coords
        self.speed = speed
        self.distance = distance

    def get_direction(self):
        return self.direction
        
    def get_location(self):
        return self.location

    def get_coords(self):
        return self.coords

    def get_speed(self):
        return self.speed
    
    def refresh(self, position):
        '''
        Recalculate the distance between the user and the trap zone

        Parameter(s):   position<tuple><float>  Current position of the user
        Return:         None
        '''
        self.distance = haversine(position, self.coords)

    def __lt__(self, other):
        # return self.order[self.direction] < other.order[other.direction]
        if self.distance is None or other.distance is None:
            raise TypeError("Cannot compare object(s) with distance=None")
        return self.distance < other.distance

    def __repr__(self):
        return "{}\n{} km/h ({})\n".format(self.location, self.speed, self.direction)