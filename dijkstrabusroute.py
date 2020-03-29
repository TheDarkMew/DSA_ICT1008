import json
from collections import defaultdict
import csv
from math import radians, cos, sin, asin, sqrt
import re

import read_bus_jsons
from read_bus_jsons import read_stop_info

#READING THE BUS ROUTE
def add_busstops_to_graph(graph,edges):
    for stops in read_stop_info("datasets/bus/punggol_bus_stops.json"):
        edges.append(stops)
    for edge in edges:
        graph.add_edge(*edges)

#FOR BUS-STOP TO HDB BLOCKS
def readHDBSGforbusstop(databus, edges):
    with open("sg_zipcode_mapper.csv") as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    return add_edges_hdbbus(data, databus, edges)
#FOR BUS-STOP TO HDB BLOCKS WEIGHT
def add_edges_hdbbus(hdbsg, databus, edges):
    new_hdb = []  # new_hdb[searchval, lat1, lo
    for rowbus in databus:
        for rowhdb in hdbsg:
            x = distance(float(rowbus[1]), float(rowhdb[1]), float(rowbus[2]), float(rowhdb[2]))
            x = float("%.2f" % round(x, 2))
            if x < 0.15:
                edges.append((rowbus[0], rowhdb[7], x))



    edges = list(dict.fromkeys(edges))  # remove duplicates
    edges.sort(key=sortFirst)  # sort first element ascending order
    return edges

def sortFirst(val):
    return val[0]


def get_path_coords(bus_stop,hdb,path):
    path_coords = []
    for i in range(0, len(path)):
        node = path[i]
        if "SINGAPORE" not in node:
            for row in bus_stop:
                if row[0] == node:
                    path_coords.append([row[1], row[2]])
                    break
        else:
            for row in hdb:
                if row[7] == node:
                    path_coords.append([float(row[1]), float(row[2])])
                    break
    return path_coords


#FORMULA FOR LAT AND LONG
def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight




def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    CALCULATINGDISTANCE = 0
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
                CALCULATINGDISTANCE = 'TOTAL DISTANCE: ' + str(weight)

            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return ["Route Not Possible"]
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []

    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    # Reverse path
    path = path[::-1]
    path.append(CALCULATINGDISTANCE)
    return path



graph = Graph()
edges=[]


#TESTING FOR BUS TO HDB
read_bus_jsons.add_busstops_to_graph(graph, edges)
hdbbus = []
buslist = []  # BUS LIST GOT BUS STOP,LATITUDE,LONGTITUDE
punggol_buses = (json.loads(open('datasets/bus/punggol_buses.json').read()))
# print(punggol_buses)
# [{'BusStopCode': '64371', 'Description': 'Opp Punggol CC', 'Latitude': 1.37447444021165, 'Longitude': 103.89289427356103, 'RoadName': 'Hougang Ave 6', 'BusServices': ['113', '161', '27', '62', '62A', '6N']},
for test in punggol_buses:
    if ('Description' in test):
        buslist.append((test['Description'], test['Latitude'], test['Longitude']))

# ADDING BUS-STOP TO HDB BLOCKS
hdbbus = readHDBSGforbusstop(buslist, hdbbus)
# print(hdbbus)
for edge in hdbbus:
    graph.add_edge(*edge)

#print (dijsktra(graph, 'Punggol Temp Int', '25 PUNGGOL FIELD WALK WATERWOODS SINGAPORE 828751'))

