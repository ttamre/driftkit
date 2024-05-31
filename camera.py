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


Filename: camera.py
Description: Source file to the Camera class
"""

from haversine import haversine

class Camera:
    def __init__(self, site_id, speed, direction, location, coords, distance=0.0):
        """
        :param site_id      str     Site ID of the speed trap
        :param speed        int     Speed limit of the speed trap
        :param direction    str     Direction of the road that approaches the camera
        :param location     str     Address of the camera 
        :param coords       tuple   GPS coordinates of the camera (latitude, longitude)
        :param distance     float   Approximate distance between the user and the camera
        """
        self.site_id = site_id
        self.location = location
        self.direction = direction
        self.speed = speed
        self.coords = coords
        self.distance = distance

    
    def get_speed(self):
        return self.speed

    def get_direction(self):
        return self.direction

    def get_location(self):
        return self.location
    
    def get_coords(self):
        return self.coords

    def get_distance(self):
        return self.distance
    

    def refresh(self, position):
        '''
        Recalculate the distance between the user and the camera device

        Parameter(s):   position<tuple><float>  Current position of the user
        Return:         None
        '''
        self.distance = haversine(position, self.coords)

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        return """Site {site}:\t{location} ({direction})
        \tSpeed:    {speed} km/h
        \tDistance: {distance} km\n
        """.format(
            site = self.site_id,
            location = self.location,
            direction = self.direction,
            speed = self.speed,
            distance = "%.3f" % self.distance
        )