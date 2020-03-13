from collections import defaultdict
import read_bus_jsons as rbj
import bustohdb as bth

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





graph = Graph()


edges = [
    ("Punggol MRT", "bus 101 stop 1", 7),
    ("Punggol MRT", "bus 102 stop 1", 9),
    ("Punggol MRT", "bus 103 ", 14),
    ("bus 101 stop 1", "bus 102 stop 2", 10),
    ("bus 101 stop 1", "bus 101 stop2", 15),
    ("bus 102 stop 1", "bus 101 stop 2", 11),
    ("bus 102 stop 1", "f", 2),
    ("bus 101 stop 2", "SIT", 6),
    ("e", "f", 9)
]

for edge in edges:
    graph.add_edge(*edge)


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    CALCULATINGDISTANCE=0
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
                CALCULATINGDISTANCE='TOTAL DISTANCE: '+str(weight)

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
    path.append(CALCULATINGDISTANCE)
    return path


#theses list are used to hold data ( sotre
lastBusStopHolder=[]
allBusStopDetails=[]
BusStopDetails=[]
rbj.add_busstops_to_graph(graph,edges)

print (dijsktra(graph, 'Aft Punggol Field', 'Meridian Stn Exit B'))

#used to append the 2nd last point of the list to a list ( which is storeLast)
bth.storeLast((dijsktra(graph, 'Aft Punggol Field', 'Meridian Stn Exit B')),lastBusStopHolder)

# reads all the data of the bus and appends them in only for the bus stop description/lat/long/bus stop code to storeLast2
rbj.readBus((allBusStopDetails))

#returns in string format rather than list
bth.returnLast(lastBusStopHolder)

#This gets the last bus stop details and store it into
print bth.match(lastBusStopHolder,allBusStopDetails,BusStopDetails)

#This gets the bus stop code( after comparing)
bth.getBusCode(BusStopDetails)

#Gets the Detail via the oneMapAPI which then will be used in below
bth.oneMap_apicall(bth.getBusCode(BusStopDetails))

bth.getLong(bth.oneMap_apicall(bth.getBusCode(BusStopDetails)))

#Example usage of end point to use for distance
bth.getLat(bth.oneMap_apicall("824174"))
bth.getLong(bth.oneMap_apicall("824174"))

#Gets the distance of the both lat/long points and calculates the distance between them
x =  bth.distance(bth.getLat(bth.oneMap_apicall(bth.getBusCode(BusStopDetails))),bth.getLat(bth.oneMap_apicall("824174")),
       bth.getLong(bth.oneMap_apicall(bth.getBusCode(BusStopDetails))),bth.getLong(bth.oneMap_apicall("824174")))
print x
#some useless formula adding
print bth.addUpDist(dijsktra(graph, 'Aft Punggol Field', 'Meridian Stn Exit B'),x)