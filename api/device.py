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
Class definitions
-------------------------------------------------------------------------------
"""

from haversine import haversine

MAPPINGS = {"NB": "Northbound", "EB": "Eastbound", "SB": "Southbound", "WB": "Westbound"}

"""
Parent class for speed camera and speed trap classes
In order to be calculable and comparable, we need a common base class with the following

    - self.distance:    float       distance between device and user
    - self.refresh():   function    recalculates the distance between the user and the device
    - comparators:
        __lt__():       function    defines less than + greater than
        __le__():       function    defines less than or equal + greater than or equal
        __eq__():       function    defines equal or not equal
"""
class Device:
    def __init__(self, site_id, speed, direction, location, coords, distance=0.0, icon=""):
        """
        :param site_id      str     Site ID of the speed trap
        :param speed        int     Speed limit of the speed trap
        :param direction    str     Direction of the road that approaches the camera
        :param location     str     Address of the camera 
        :param coords       tuple   GPS coordinates of the camera (latitude, longitude)
        :param distance     float   Approximate distance between the user and the camera
        """
        self.site_id = site_id
        self.speed = speed
        self.direction = direction
        self.location = location
        self.coords = coords
        self.distance = distance
        self.icon = icon

    # Getters
    def get_site_id(self):
        return self.site_id
    
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
    
    def get_icon(self):
        return self.icon
    

    # Class methods
    def refresh(self, position):
        '''
        Recalculate the distance between the user and the camera device
        
        :param position     tuple   lat/lon of the user as floats
        '''
        self.distance = haversine(position, self.coords)

    # Comparison methods
    def __lt__(self, other):
        return self.distance < other.distance
    
    def __le__(self, other):
        return self.distance <= other.distance
    
    def __eq__(self, other):
        return self.distance == other.distance


class Camera(Device):

    def __init__(self, site_id, speed, direction, location, coords, distance=0.0, icon="📷"):
        """
        :param site_id      str     Site ID of the speed trap zone
        :param speed        int     Speed limit of the speed trap zone
        :param direction    str     Direction of the road that approaches the trap zone
        :param location     str     Address of the trap zone
        :param coords       tuple   GPS coordinates of the camera (lat:float, lon:float)
        :param distance     float   Approximate distance between the user and the trap zone
        :param icon         str     Unicode icon for camera
        """
        Device.__init__(self,
                        site_id=site_id,
                        speed=speed,
                        direction=direction,
                        location=location,
                        coords=coords,
                        distance=distance,
                        icon=icon)

    # String representation of the Camera object
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

class Trap(Device):

    def __init__(self, site_id, speed, direction, location, coords, distance=0.0, icon="🪤"):
        """
        :param site_id      str     Site ID of the speed trap zone
        :param speed        int     Speed limit of the speed trap zone
        :param direction    str     Direction (abbreviation) of the road that approaches the trap zone
        :param location     str     Address of the trap zone
        :param coords       tuple   GPS coordinates of the trap zone (lat:float, lon:float)
        :param distance     float   Approximate distance between the user and the trap zone
        :param icon         str     Unicode icon for trap
        """
        Device.__init__(self,
                        site_id=site_id,
                        speed=speed,
                        direction=MAPPINGS.get(direction, ""),
                        location=location,
                        coords=coords,
                        distance=distance,
                        icon=icon)


    # String representation of the Trap object
    def __repr__(self):
        return "{}\n{} km/h ({})\n".format(self.location, self.speed, self.direction)
    