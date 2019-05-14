#Finding the Centrality of the graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
##Folder_to_save_graphs=folder
import osmnx as ox, geopandas as gpd, networkx as nx
from networkx.algorithms import centrality as cen
from itertools import chain
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import shp2osmnx as s2nx
import csv


Folder_to_load_from= '{}'.format(Folder_to_load_from)
Folder_to_save_graphs=str(Folder_to_save_graphs)
#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

# create an undirected Graph from the MultiDiGraph, for those metrics that require it
#G_undir = nx.Graph(G)

# create a strongly connected graph

#G_strong = ox.get_largest_component(G, strongly=True)

stats = {}
 # degree centrality for a node is the fraction of nodes it is connected to
degree_centrality = nx.degree_centrality(G)
stats['degree_centrality'] = degree_centrality
stats['degree_centrality_avg'] = sum(degree_centrality.values())/len(degree_centrality)

 # closeness centrality of a node is the reciprocal of the sum of the shortest path distances from u to all other nodes
closeness_centrality = nx.closeness_centrality(G, distance='length')
stats['closeness_centrality'] = closeness_centrality
stats['closeness_centrality_avg'] = sum(closeness_centrality.values())/len(closeness_centrality)
#calculate node betweenness centrality
# betweenness centrality of a node is the sum of the fraction of all-pairs shortest paths that pass through node
betweenness_centrality = nx.betweenness_centrality(G, weight='length')
stats['betweenness_centrality'] = betweenness_centrality
stats['betweenness_centrality_avg'] = sum(betweenness_centrality.values())/len(betweenness_centrality)



filepath=Folder_to_save_graphs+str('/Deg_Close_Between_centrality.csv')
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
