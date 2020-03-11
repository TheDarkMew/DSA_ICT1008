import json
import math
import geopy.distance


def read_lta_jsons(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    return [stops for stops in bus_dicts['value']]


def read_jsons_into_dicts(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    #print(type(bus_dicts))
    return bus_dicts


def convert_degtorad(deg):
    return deg * (math.pi / 180)


def checkif_in_punggol(dicts, newdict):
    count = 0
    for stops in dicts:
        if 1.39 < stops['Latitude'] < 1.42 and 103.90 < stops['Longitude'] < 103.92:
            count += 1
            #print(stops)
            newdict.append(stops)
    #print(count)

def get_distancebetween_coords(lat1,lon1,lat2,lon2):
    # Approximate radius of the earth
    eRadius = 6373.0

    #Convert latitude and longitude to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = eRadius * c
    return distance




testdict = read_lta_jsons('datasets/bus/north_bus_stops_part2.json')
newdict = []
checkif_in_punggol(testdict, newdict)
busesdict = read_jsons_into_dicts('datasets/bus/bus-stops-services.json')

#print(busesdict)
count = 0
for stops in newdict:
    if stops.get('BusStopCode') in busesdict:
        count += 1
        #print(busesdict[stops.get('BusStopCode')])
        stops['BusServices'] = busesdict[stops.get('BusStopCode')]
        print(stops)

#print(count)
#print(newdict)

print(get_distancebetween_coords(1.40370629859822,103.90224337575333,1.39308440832899,103.90129355204087))
coord1 = (1.40370629859822,103.90224337575333)
coord2 = (1.39308440832899,103.90129355204087)
print(geopy.distance.vincenty(coord1,coord2).km)

