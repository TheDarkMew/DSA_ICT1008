import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

G.add_edge('Punggol MRT', 'bus 101 stop 1', weight=7)
G.add_edge('Punggol MRT', 'bus 102 stop 1', weight=9)
G.add_edge('Punggol MRT', 'bus 103', weight=14)
G.add_edge('bus 101 stop 1', 'bus 102 stop 2', weight=10)
G.add_edge('bus 101 stop 1', 'bus 101 stop2', weight=15)
G.add_edge('bus 102 stop 1', 'd', weight=2)
G.add_edge('bus 102 stop 1', 'd', weight=2)
G.add_edge('bus 101 stop2', 'SIT', weight=6)



elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

plt.axis('on')
plt.show()
