
from collections import defaultdict
import csv
from math import radians, cos, sin, asin, sqrt
import re


def readMRTSG():
    new_area = []
    with open("mrtfaretime.csv", 'r') as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    for row in data:
        row[0] = row[0].replace('\xa0', ' ')
        row[0] = re.sub(' {2,}', ' ', row[0])  # remove unnecessary spacing
        row[1] = row[1].replace('\xa0', ' ')
        row[1] = re.sub(' {2,}', ' ', row[1])
        row[8] = row[8].replace('\xa0', '')
        row[11] = row[11].replace('\xa0', '')
        if "NE17" in row[8]:
            new_area.append(row)
    new_area = calculate_distance_mrt(new_area)
    return new_area


def readHDBSG():  # add to data only for punggol area
    # latitude, longitude
    # Centre
    # 1.405816, 103.907353
    # Top
    # 1.420598, 103.907353
    # Bottom
    # 1.389810, 103.907353
    # Right
    # 1.405816, 103.924800
    # Left
    # 1.405816, 103.891821
    new_area = []
    with open("sg_zipcode_mapper.csv") as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    for row in data:
        lat = float(row[1])
        long = float(row[2])
        if 1.389810 < lat < 1.420598 and 103.891821 < long < 103.924800:
            new_area.append(row)
    return new_area


def sortFirst(val):
    return val[0]


def get_path_coords(hdb,mrt,path):
    path_coords = []
    path_coords.append([1.40527,103.90236]) #NE17 PTC Punggol
    for i in range(1,len(path)):
        node = path[i]
        if "NE17" in node or "PE" in node or "PW" in node:
            for row in mrt:
                if row[1] == node:
                    path_coords.append([float(row[12]),float(row[13])])
                    break
        else:
            for row in hdb:
                if row[7] == node:
                    path_coords.append([float(row[1]),float(row[2])])
                    break
    return path_coords



def add_edges_mrt_hdb(hdbsg, mrtsg, edges):
    new_hdb = []  # new_hdb[searchval, lat1, lo
    for rowmrt in mrtsg:
        for rowhdb in hdbsg:
            if rowmrt[0] == "NE17 PTC Punggol":
                x = distance(float(rowmrt[9]), float(rowhdb[1]), float(rowmrt[10]), float(rowhdb[2]))
                x = float("%.2f" % round(x, 2))
                if x < 0.2 and rowmrt:
                    edges.append((rowmrt[0], rowhdb[7], x))
    edges = list(dict.fromkeys(edges))  # remove duplicates
    edges.sort(key=sortFirst)  # sort first element ascending order
    return edges


def add_edges_hdb(hdbsg, edges): # add edges hdb to hdb that is less than 0.1km
    new_hdb = []
    for rowhdb in hdbsg:
        for rowhdb1 in hdbsg:
            x = distance(float(rowhdb[1]), float(rowhdb1[1]), float(rowhdb[2]), float(rowhdb1[2]))
            if x < 0.1:
                edges.append((rowhdb[7], rowhdb1[7], x))


    return edges


def calculate_distance_mrt(mrtsg):
    for row in mrtsg:
        x = distance(float(row[9]), float(row[12]), float(row[10]), float(row[13]))
        x = float("%.2f" % round(x, 2))
        row.insert(14, x)
    return mrtsg


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


# print (dijsktra(graph, 'Punggol MRT', 'SIT'))
graph = Graph()
edges =[]
datamrt = readMRTSG()
datahdb = readHDBSG()
edges = add_edges_hdb(datahdb, edges)
edges = add_edges_mrt_hdb(datahdb, datamrt, edges)
for edge in edges:
    graph.add_edge(*edge)

#print (dijsktra(graph, 'NE17 PTC Punggol', '260C PUNGGOL WAY PUNGGOL TOPAZ SINGAPORE 823260'))