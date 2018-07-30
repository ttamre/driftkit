#!/usr/bin/env python3

"""
Filename: driftkit.py

Description: Intersection camera detector for the city of Edmonton
References: https://docs.python.org/3.6/library/csv.html

"""
__author__ = "Tem Tamre"
__email__ = "ttamre@ualberta.ca"

import os
import sys
import csv
from graphics import *


def main():
    print("""
  _____  _____  _____ ______ _______ _  _______ _______ 
 |  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
 | |  | | |__) | | | | |__     | |  | ' /  | |    | |   
 | |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
 | |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
 |_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 """)
    print("-" * 40)
    print("Because nobody likes speed cameras")
    print("-" * 40)

    data = load_csv()

    ui = input("Would you like to use the terminal, GUI, or webserver interface?\n> ").lower()
    if ui.startswith("t"):
        print_data(data)
    elif ui.startswith("g"):
        pass
    elif ui.startswith("w"):
        if sys.version_info[0] == 3:
            os.system("python src/page.py")
        else:
            os.system("python3 src/page.py")


def load_csv(filename="assets/data.csv"):
    datadict = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader, None)  # Skip the header
        for row in csvreader:
            site_id = row[0]
            enforcement = row[1]
            location = "{} {}".format(row[2], row[3])
            direction = row[4]
            speed = row[5]
            coordinates = eval(row[6]), eval(row[7])
            datadict[site_id] = [enforcement, location, direction, speed, coordinates]
    
    return datadict


def print_data(data):
   for site in data:
        print("Site {site}: {location} ({direction})".format(
            site=site, location=data[site][1], direction=data[site][2]))
        print("\tPosted speed: {speed}".format(speed=data[site][3]))
        print("\tGPS Coordinates: {coords}\n".format(coords=data[site][4]))


# ==================================================
# Map Functions
# ==================================================

def interactive_map(shape_IDs, shapes, stops):
    win = GraphWin("Edmonton Transit System", 630*1.5, 768*1.5)
    background = Image(Point(win.getWidth() / 2, win.getHeight() / 2), 'map.gif')
    background.draw(win)
    win.setCoords(-113.7136, 53.39576, -113.2714, 53.71605)

    while not win.isClosed():
        try:
            pt = win.getMouse()
        except GraphicsError:
            return win.close()
        if (200 < win.toScreen(pt.x, pt.y)[0] < 300)\
            and (5 < win.toScreen(pt.x, pt.y)[1] < 25):
            route_input = entry_box.getText()
            if route_input not in shape_IDs:
                print("{} isn't a route".format(route_input))
            else:
                plot_points(route_input, shape_IDs, shapes, win)
        else:
            print_draw_map_data(win, pt, stops)


def plot_points(route, shape_IDs, shapes, win):
    points = []
    largest = ""
    for shape_ID in shape_IDs[route]:
        if len(shapes[shape_ID]) > len(largest):
            largest = shapes[shape_ID]
    for coord in largest:
        point = Point(float(coord[1]), float(coord[0]))
        points.append(point)
    for i in range(len(points) - 1):
        line = Line(points[i], points[i + 1])
        line.setWidth(3)
        line.setFill("gray50")

if __name__ == "__main__":
    main()