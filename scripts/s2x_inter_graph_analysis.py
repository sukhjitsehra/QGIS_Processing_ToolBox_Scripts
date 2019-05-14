#Finding the Information centrality of the road graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
##Folder_to_save_graphs=folder
##Name_of_stat_file=string centrality.csv
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
Name_of_stat_file='{}'.format(Name_of_stat_file)

stats={}
#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

stats={}
#Calculate the number of nodes in the graph
v= nx.number_of_nodes(G)

#Calculate the number of edges in the graph

e=nx.number_of_edges(G)

#gamma index of graph

#gamma=e/float((v*v-v)/2) for non-planer graph
gamma=e/float(3*v-2)
stats['edges']=e
stats['nodes']=v
stats['gamma']=gamma

G1=G.to_undirected()
#Count the number of connected components
g=nx.number_connected_components(G1)

stats['number_of_connected_component']=g
# Find the cyclomatic number

cyclomatic_number= e-v+g

stats['cyclomatic_number']=cyclomatic_number

# Find The maximum number of cycles

#mc=float((v*v-v)/2) - (v-1) #seems like for non-planer graph

#stats['maximum_number_of_cycles']=mc
#Redundancy Index
#ri=(e-v+g)/float(((v*v-v)/2)-v+1) #seems like for non-planer graph

#stats['redundancy_Index']=ri

#calculate alpha
alpha= cyclomatic_number/float(2*v-5)
stats['alphaindex']=alpha




filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats.items())
df.to_csv(filepath)
