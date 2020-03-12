from collections import defaultdict
import read_bus_jsons


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


read_bus_jsons.add_busstops_to_graph(graph,edges)
print (dijsktra(graph, 'Aft Punggol Field', 'Soo Teck Stn'))