from pyvis.network import Network
import dijkstra as dj

#if set the graph edges to hidden=True, only routing edges will be shown, nodes colour will be different (more obvious)

#if set the grpah edges to hidden=False(by default to false), all edges will be shown but ONLY NODE can have colour,
#thus, it will leads to all the routing nodes will be red and only the correct pathing edges will be thicken
#you can uncomment 41 and comment 39 to see ^ this result
def findRouteGraph(start,end):

    net = Network(height='2000px', width='2000px')
    #store the route from start to end in a list
    route = []
    #len(dj...)-1 : total distance is excluded
    for i in range(0, len(dj.dijsktra(dj.graph,start, end))-1):
        #appending each node into route[]
        route.append(dj.dijsktra(dj.graph,start, end)[i])

    #setting the route as red colour node with a bigger size
    for i in range(0,len(route)):
        #only node can be coloured
        if (i == 0):
            net.add_node(route[i],size=10,color='green',title="Starting Point")
        elif (i == len(route)-1):
            net.add_node(route[i], size=10, color='green', title="Ending Point")
        else:
            net.add_node(route[i], size=10, color='green')
        #net.add_node(route[i], size=10)

    for i in range (0,len(route)):
        if (i < len(route)-1):
            net.add_edge(route[i],route[i+1],width=2)

    #aading all the nodes and edges to the network graph

    # net.add_node('NE17 PTC Punggol', hidden=False, size=5)
    # net.add_node('PE1 Cove', hidden=False, size=5)
    # net.add_node('PE2 Meridian', hidden=False, size=5)
    # net.add_node('PE3 Coral Edge', hidden=False, size=5)
    # net.add_node('PE4 Riviera', hidden=False, size=5)
    # net.add_node('PE7 Damai', hidden=False, size=5)
    # net.add_node('PW1 Sam Kee', hidden=False, size=5)
    # net.add_node('PW3 Punggol Point', hidden=False, size=5)
    # net.add_node('PW4 Samudera', hidden=False, size=5)
    # net.add_node('PW5 Nibong', hidden=False, size=5)
    # net.add_node('PW6 Sumang', hidden=False, size=5)
    # net.add_node('PW7 Soo Teck', hidden=False, size=5)
    # net.add_node('PE5 Kadaloor', hidden=False, size=5)
    # net.add_node('PE6 Oasis', hidden=False, size=5)

        # aading all the nodes and edges to the network graph
        for i in range(0, len(dj.edges)):
            # all address will be shown
            net.add_node(dj.edges[i][0], size=5)
            net.add_node(dj.edges[i][1], size=5)
            # only route addresses will be shown
            # net.add_node(dj.edges[i][0],size=5,hidden=True)
            # net.add_node(dj.edges[i][1],size=5,hidden=True)

            # edges line is hidden, only route edges will be shown
            # net.add_edge(dj.edges[i][0],dj.edges[i][1], weight=dj.edges[i][2],hidden=True)
            # all edges will be shown
            net.add_edge(dj.edges[i][0], dj.edges[i][1], weight=dj.edges[i][2])
    # show network graph is there is a route
    if (len(route) > 0):
        net.show("plotlyFlask.html")

