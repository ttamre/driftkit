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


Filename: building.py
Description: Source file to the Building class
"""

class Building:
    def __init__(self, key, name, lat, lon):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lon  = lon

    def get_key(self):
        return self.key

    def get_name(self):
        return self.name

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon
    
    def get_coords(self):
        return (self.lat, self.lon)