#!/usr/bin/env python3

"""
Filename: driftkit.py

Description: Intersection camera detector for the city of Edmonton
References: https://docs.python.org/3.6/library/csv.html

"""
__author__ = "Tem Tamre"
__email__ = "ttamre@ualberta.ca"

import sys
import csv

def main():
    if len(sys.argv) <= 1:
        filename = "assets/data.csv"
    elif len(sys.argv) >= 2:
        filename = sys.argv[1]
    
    if len(sys.argv) > 2:
        print("Unrecognized inputs:", sys.argv[2::])

    
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

    start = input("Would you like to display locations and information of all\ntraffic cameras in Edmonton? ")
    if start.lower().startswith("n"):
        print("Goodbye!")
        exit(0)

    data = load_csv(filename)
    print_data(data)

def load_csv(filename="assets/data.csv"):
    datadict = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            site_id = row[0]        # Site ID (col 1)
            enforcement = row[1]    # Enforcement Type (col 2)
            location = "{} {}".format(row[2], row[3])
            direction = row[4]
            speed = row[5]
            coordinates = row[6], row[7]
            datadict[site_id] = [enforcement, location, direction, speed, coordinates]
    
    
    return datadict

def print_data(data):
   for site in data:
        print("Site {site}: {location} ({direction})".format(
            site=site, location=data[site][1], direction=data[site][2]))
        print("\tPosted speed: {speed}".format(speed=data[site][3]))
        print("\tGPS Coordinates: {coords}".format(coords=data[site][4]))
        print()

if __name__ == "__main__":
    main()