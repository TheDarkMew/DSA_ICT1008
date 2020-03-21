from pyvis.network import Network
import dijkstra as dj



net = Network(height='2000px', width='2000px')
    #store the route from start to end in a list
route = []
    #len(dj...)-1 : total distance is excluded
for i in range(0, len(dj.dijsktra(dj.graph,'NE17 PTC Punggol', '213C PUNGGOL WALK PUNGGOL WAVES SINGAPORE 823213'))-1):
        #appending each node into route[]
    route.append(dj.dijsktra(dj.graph,'NE17 PTC Punggol', '213C PUNGGOL WALK PUNGGOL WAVES SINGAPORE 823213')[i])

    #setting the route as red colour node with a bigger size
for i in range(0,len(route)):
    net.add_node(route[i],color='red',size=10)


for i in range (0,len(route)):
    if (i < len(route)-1):
        net.add_edge(route[i],route[i+1],width=2)

    #aading all the nodes and edges to the network graph
for i in range(0, len(dj.edges)):
        #all address will be shown
    net.add_node(dj.edges[i][0], size=5)
    net.add_node(dj.edges[i][1], size=5)
        #only route addresses will be shown
        #net.add_node(dj.edges[i][0],size=5,hidden=True)
        #net.add_node(dj.edges[i][1],size=5,hidden=True)

    #edges line is hidden, only route edges will be shown
    net.add_edge(dj.edges[i][0],dj.edges[i][1], weight=dj.edges[i][2],hidden=True)
    # all edges will be shown
    #net.add_edge(dj.edges[i][0], dj.edges[i][1], weight=dj.edges[i][2], hidden=True)
#print(net.edges)


#net.toggle_physics(True)
net.show("plotlyFlask.html")

