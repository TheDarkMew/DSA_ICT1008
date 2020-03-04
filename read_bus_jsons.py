import json
import math


def read_jsons(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)


    return [stops for stops in bus_dicts['value']]


def convert_degtorad(deg):
    return deg * (math.pi / 180)


def checkif_in_punggol(dicts, newdict):
    earthradius = 6371
    punggol_lat = convert_degtorad(1.3984)
    punggol_lon = convert_degtorad(103.9072)
    count = 0
    for stops in dicts:
        if 1.39 < stops['Latitude'] < 1.42 and 103.90 < stops['Longitude'] < 103.92:
            count += 1
            print(stops)
            newdict.append(stops)
    print(count)


testdict = read_jsons('datasets/bus/north_bus_stops_part2.json')
newdict = []
checkif_in_punggol(testdict, newdict)

