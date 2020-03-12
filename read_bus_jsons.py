import json
import math


def read_lta_jsons(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    return [stops for stops in bus_dicts['value']]


def read_jsons_to_list(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    return bus_dicts


def convert_degtorad(deg):
    return deg * (math.pi / 180)


def checkif_in_punggol(dicts, newlist):
    count = 0
    for stops in dicts:
        if "Punggol" in stops['Description'] or "Punggol" in stops['RoadName']:
            newlist.append(stops)
            count += 1
    print(count)


def get_distancebetween_coords(lat1, lon1, lat2, lon2):
    # Approximate radius of the earth
    eRadius = 6373.0

    # Convert latitude and longitude to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = eRadius * c
    return round(distance, 3)


def save_punggol_bus_info():
    busstops = read_lta_jsons('datasets/bus/north_bus_stops_part2.json')
    punggol_buses = []
    checkif_in_punggol(busstops, punggol_buses)
    busroutes = read_jsons_to_list('datasets/bus/north_bus_routes.json')

    for stops in punggol_buses:
        templist = []
        for services in busroutes:
            if stops.get('BusStopCode') == services.get('BusStopCode'):
                if services.get('ServiceNo') not in templist:
                    templist.append(services.get('ServiceNo'))

        stops['BusServices'] = templist

    with open("datasets/bus/punggol_buses.json", "w") as f:
        f.write(json.dumps(punggol_buses))


# Get the full details of bus stops
def get_punggol_busstop_details():
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    stops_desc = {stops['Description']: stops['BusServices'] for stops in punggol_buses}
    return stops_desc


# Get the bus stops and the buses that goes through it
def get_punggol_bus_stops_with_services():
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    stops_desc = {stops['Description']: stops['BusServices'] for stops in punggol_buses}
    return punggol_buses


# Get all the bus numbers that goes through punggol
def get_punggol_busservices():
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    for stops in punggol_buses:
        if stops["Description"] == "Punggol Temp Int":
            p_bus_services = stops["BusServices"]
    return p_bus_services


# Get the bus route and distance of each bus stop of selected bus and direction
def get_punggol_busroute(busnum, direction):
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    stops_desc = {stops['Description']: stops for stops in punggol_buses}
    stops_code = {stops['BusStopCode']: stops for stops in punggol_buses}
    routes = json.loads(open('datasets/bus/north_bus_routes.json').read())
    route_map = {}

    for route in routes:
        key = (route["ServiceNo"], route["Direction"])
        if key not in route_map:
            route_map[key] = []
        route_map[key] += [route]

    print([stops_code[rx["BusStopCode"]]["Description"] for rx in route_map[(busnum, direction)] if
           rx["BusStopCode"] in stops_code])

    bus_route = [stops_code[rx["BusStopCode"]]["Description"] for rx in route_map[(busnum, direction)] if
                 rx["BusStopCode"] in stops_code]

    bus_route_with_dist = {}
    for index in range(len(bus_route)):
        if index == 0:
            bus_route_with_dist[bus_route[index]] = 0
        else:
            distance = get_distancebetween_coords(stops_desc[bus_route[index]]["Latitude"],
                                                  stops_desc[bus_route[index]]["Longitude"],
                                                  stops_desc[bus_route[index - 1]]["Latitude"],
                                                  stops_desc[bus_route[index - 1]]["Longitude"])
            bus_route_with_dist[bus_route[index]] = distance

    print(bus_route_with_dist)


get_punggol_busroute("85", 1)
# print(get_punggol_busstop_details())
