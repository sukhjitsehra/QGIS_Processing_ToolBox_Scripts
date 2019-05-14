#Routing Distances and Direct distances. 
##[Struct.Analysis]=group
import networkx as nx
import osmnx as mnx
import matplotlib.pyplot as plt


G=nx.Graph()
G.add_edges_from([(1,2),(1,3)])
G.add_node("spam")
nx.connected_components(G)
sorted(nx.degree(G).values())
nx.clustering(G)
nx.draw(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)

plt.show()
#print 123