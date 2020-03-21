import json
from decimal import Decimal, getcontext

# Checks if the bus stops from the dataset is in the Punggol Area
def checkif_in_punggol(dicts, newlist):
    count = 0
    for stops in dicts:
        if "Punggol" in stops['Description'] or "Punggol" in stops['RoadName']:
            newlist.append(stops)
            count += 1
    print(count)


# Get the full details of bus stops
def get_punggol_busstop_details():
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    print(punggol_buses)
    return punggol_buses


# Get the bus stops and the buses that goes through it
def get_punggol_bus_stops_with_services():
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    stops_desc = {stops['Description']: stops['BusServices'] for stops in punggol_buses}
    return stops_desc


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
    stops_code = {stops['BusStopCode']: stops for stops in punggol_buses}
    routes = json.loads(open('datasets/bus/north_bus_routes.json').read())
    route_map = {}

    for route in routes:
        key = (route["ServiceNo"], route["Direction"])
        if key not in route_map:
            route_map[key] = []
        route_map[key] += [route]

    if (busnum, direction) in route_map:
        bus_route = [(stops_code[rx["BusStopCode"]]["Description"], rx["Distance"]) for rx in
                     route_map[(busnum, direction)] if rx["BusStopCode"] in stops_code]

    else:
        bus_route = []

    if bus_route:
        getcontext().prec = 3
        bus_route_with_dist = [
            (bus_route[index - 1][0], bus_route[index][0],
             float(Decimal(bus_route[index][1]) - Decimal(bus_route[index - 1][1])))
            for index in range(len(bus_route)) if index > 0]

    else:
        bus_route_with_dist = []

    # print(bus_route_with_dist)
    return bus_route_with_dist


# ----------------------------- Main function for Bus Stops-------------------------------------------
# Just need to call this function with the graph and edges as parameters to add bus stops to the graph
def add_busstops_to_graph(graph, edges):
    for stops in read_stop_info("datasets/bus/punggol_bus_stops.json"):
        edges.append(stops)

    for edge in edges:
        graph.add_edge(*edge)


# Reading and Writing to JSON files Misc Functions
# -Writing to JSON
def save_busnodes_to_json():
    templist = []
    for services in get_punggol_busservices():
        routelist = get_punggol_busroute(services, 1)
        if routelist:
            for route in routelist:
                templist.append(route)

    for services in get_punggol_busservices():
        routelist = get_punggol_busroute(services, 2)
        if routelist:
            for route in routelist:
                templist.append(route)

    with open("datasets/bus/punggol_bus_stops.json", "w") as f:
        f.write(json.dumps(templist))


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


# -Reading from JSONs
def read_lta_jsons(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    return [stops for stops in bus_dicts['value']]


def read_jsons_to_list(jsonlink):
    with open(jsonlink, 'r') as test:
        bus_dicts = json.load(test)
    return bus_dicts


def read_stop_info(jsonlink):
    with open(jsonlink, 'r') as temp:
        tempholder = json.load(temp)
    return [tuple(items) for items in tempholder]

# graph = dijkstra.Graph()
# edges = []
# print(dijkstra.dijsktra(graph,'Opp The Rivervale', 'Aft TPE'))

# stores the bus data into desciprtion,long,lat,buscode to be used in other code)
def readBus(newdict):
    punggol_buses = json.loads(open('datasets/bus/punggol_buses.json').read())
    for bus in punggol_buses:
        if bus['Description'] and bus['Longitude'] and bus['Latitude'] and bus['BusStopCode']:
            newdict.append(bus['Description'])
            newdict.append(bus['Longitude'])
            newdict.append(bus['Latitude'])
            newdict.append(bus['BusStopCode'])
    return newdict