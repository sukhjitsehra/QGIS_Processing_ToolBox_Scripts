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

#Calculate the center of graph, the folowing statement would return a list


stats['center']= nx.center(G)

#calculate the diameter

stats['diameter']=nx.diameter(G)

#caluculate the eccentricity
stats['eccentricity']=nx.eccentricity(G)

#calculate the periphery of the graph

stats['periphery']= nx.periphery(G)

# caluculate the radius 

stats['radius']= nx.radius(G, e=None)
# #statsfile=Graphml_File_Name+str('/centrality.csv')
filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
