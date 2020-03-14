from collections import defaultdict
import csv
from math import radians, cos, sin, asin, sqrt
import re


# np.set_printoptions(threshold=np.inf)

# display only punggol area mrt lrt
def readMRTSG():
    new_area = []
    with open("mrtfaretime.csv", 'r') as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    for row in data:
        row[0] = row[0].replace('\xa0', ' ').encode('utf-8')
        row[0] = re.sub(' {2,}', ' ', row[0])  # remove unnecessary spacing
        row[1] = row[1].replace('\xa0', ' ').encode('utf-8')
        row[1] = re.sub(' {2,}', ' ', row[1])
        row[8] = row[8].replace('\xa0', '').encode('utf-8')
        row[11] = row[11].replace('\xa0', '').encode('utf-8')
        if "PE" in row[8] and "PE" in row[11]:
            new_area.append(row)
        if "PW" in row[8] and "PW" in row[11]:
            new_area.append(row)
        elif "PE" in row[8] and "PW" in row[11]:
            new_area.append(row)
        elif "PW" in row[8] and "PE" in row[11]:
            new_area.append(row)
        elif "PE" in row[8] and "NE17" in row[11]:
            new_area.append(row)
        elif "PW" in row[8] and "NE17" in row[11]:
            new_area.append(row)
        elif "NE17" in row[8] and "PE" in row[11]:
            new_area.append(row)
        elif "NE17" in row[8] and "PW" in row[11]:
            new_area.append(row)
    new_area = calculate_distance_mrt(new_area)
    return new_area


def readHDBSG(datamrt, edges):
    with open("sg_zipcode_mapper.csv") as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    return add_edges_hdb(data, datamrt, edges)


def sortFirst(val):
    return val[0]


def add_edges_hdb(hdbsg, mrtsg, edges):
    new_hdb = []  # new_hdb[searchval, lat1, lo
    for rowmrt in mrtsg:
        for rowhdb in hdbsg:
            x = distance(float(rowmrt[9]), float(rowhdb[1]), float(rowmrt[10]), float(rowhdb[2]))
            x = float("%.2f" % round(x, 2))
            if x < 0.2:
                edges.append((rowmrt[0], rowhdb[7], x))
    edges = list(dict.fromkeys(edges)) # remove duplicates
    edges.sort(key=sortFirst)   # sort first element ascending order
    print edges
    return edges


def calculate_distance_mrt(mrtsg):
    for row in mrtsg:
        x = distance(float(row[9]), float(row[12]), float(row[10]), float(row[13]))
        x = float("%.2f" % round(x, 2))
        row.insert(14, x)
    return mrtsg


def add_edges_mrt(mrtsg, edges):
    PW = ("NE17", "PW1", "PW3", "PW4", "PW5", "PW6", "PW7", "NE17")
    PE = ("NE17", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PE7", "NE17")
    i = 0
    j = 8
    k = 0
    l = 7
    for row in mrtsg:
        if (row[8] == PE[i]) and (row[11] == PE[i + 1]):
            edges.append((row[0], row[1], row[14]))
            i += 1
        elif (row[8] == PE[j]) and (row[11] == PE[i - 1]):
            edges.append((row[0], row[1], row[14]))
            j -= 1
        elif (row[8] == PW[k]) and (row[11] == PW[k + 1]):
            edges.append((row[0], row[1], row[14]))
            k += 1
        elif (row[8] == PW[l]) and (row[11] == PW[l - 1]):
            edges.append((row[0], row[1], row[14]))
            l -= 1
    return edges


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
    global weight
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
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
    print("%.2fKM" % (weight))
    return path


graph = Graph()
edges = [
    ("274D PUNGGOL PLACE PUNGGOL REGALIA SINGAPORE 824274", "bus 101 stop 1", 2.3),
    ("274D PUNGGOL PLACE PUNGGOL REGALIA SINGAPORE 824274", "bus 102 stop 1", 3),
    ("NE17 PTC Punggol", "bus 103 ", 0.2),
    ("bus 101 stop 1", "bus 102 stop 2", 3.1),
    ("bus 101 stop 1", "bus 101 stop2", 1.2),
    ("bus 102 stop 1", "bus 101 stop 2", 0.9),
    ("bus 102 stop 1", "f", 1),
    ("bus 101 stop 2", "SIT", 1.2),
]

datamrt = readMRTSG()
edges = add_edges_mrt(datamrt, edges)
edges = readHDBSG(datamrt, edges)
for edge in edges:
    graph.add_edge(*edge)
print (dijsktra(graph, 'PW4 Samudera', 'SIT'))
