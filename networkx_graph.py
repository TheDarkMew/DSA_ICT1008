import matplotlib.pyplot as plt
import networkx as nx
import dijkstra as dj


#networkx
G = nx.Graph()
RouteGraph = nx.Graph()
#add the edges to the graph
#since in dijkstra.py, the edges are stored in a list(edges)
#do a for loop to add the edges into the graph
#G.add_edge(start_point, end_point,weight)
for i in range(0, len(dj.edges)):
    G.add_edge(dj.edges[i][0],dj.edges[i][1], weight=dj.edges[i][2])

#call this fucntion to plot the route from start to dest
def findRouteGraph(startPoint, endPoint):
    #store the route(nodes) into list
    route = []
    #len()-1 : to exclulde weight (distance)
    for i in range(0, len(dj.dijsktra(dj.graph, startPoint, endPoint)) - 1):
        #add in the nodes into route = []
        route.append(dj.dijsktra(dj.graph, startPoint, endPoint)[i])

    for i in range(0, len(route)):
        #add edges based on the route = []
        if (i < len(route) - 1):
            RouteGraph.add_edge(route[i], route[i + 1])



#testing
#store route into list
route = []
for i in range(0, len(dj.dijsktra(dj.graph,'NE17 PTC Punggol', '618A PUNGGOL DRIVE PUNGGOL BREEZE SINGAPORE 821618'))-1):
        route.append(dj.dijsktra(dj.graph,'NE17 PTC Punggol', '618A PUNGGOL DRIVE PUNGGOL BREEZE SINGAPORE 821618')[i])
#print(route)

for i in range(0,len(route)):
    if (i < len(route)-1):
        RouteGraph.add_edge(route[i],route[i+1])
#print(RouteGraph.edges)


elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes
#pos = nx.random_geometric_graph(200, 0.125)
# nodes
nx.draw_networkx_nodes(G, pos, node_size=100)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=2)

#weight < 0.5 : edges will be in dashed and in blue colour
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=2, alpha=0.5, edge_color='b', style='dashed')

#plot the route for the choosen start and dest
#route will be highlighted in red
nx.draw_networkx_edges(G,pos,
                       edgelist=RouteGraph.edges,
                       width=8,alpha=0.5,edge_color='r')

# labels
nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')

plt.axis('off')
#plt.show()
