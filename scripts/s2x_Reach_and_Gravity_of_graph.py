#Finding the reach and gravity of the road graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
##Radius_of_subgraph=number 10
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
import math as mt


Folder_to_load_from= '{}'.format(Folder_to_load_from)
Folder_to_save_graphs=str(Folder_to_save_graphs)
Name_of_stat_file='{}'.format(Name_of_stat_file)

stats={}
#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

#Calculate the center of graph, the folowing statement would return a list


center=nx.center(G)
cenpoint=center[0]
stats['center']=center

radius=nx.radius(G)

L=nx.ego_graph(G, cenpoint, radius=Radius_of_subgraph, center=True, undirected=False, distance=None)
n=L.number_of_nodes()

stats['Reach'] =n

#find the gravity

list_nodes=[n for n in L.nodes_iter()]

gravity={i:nx.single_source_dijkstra_path_length(L,i,weight='length') for i in list_nodes}
    
gravity1=gravity


for key, value in gravity1.iteritems():
    for key1, vl in value.iteritems():
        vl=1/float(mt.exp(.1813*vl))
        gravity1[key][key1]=vl  

gravity_node={key: sum([v for k, v in values.items()]) for key, values in gravity1.iteritems()}

stats['gravity_of_node']=gravity_node


total_gravity_network= float(sum(gravity_node.values()))/L.number_of_nodes()

stats['total_gravity_network']=total_gravity_network
filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
