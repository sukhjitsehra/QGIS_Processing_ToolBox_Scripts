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

#The inforamtion centrality needs undirected graph 
G1=G.to_undirected()

#Need Undirected graph
stats['current_flow_closeness_centrality']=cen.current_flow_closeness_centrality(G1,weight='length')
stats['current_flow_betweenness_centrality']=cen.current_flow_betweenness_centrality(G1, normalized=True, weight='length')
#statsfile=Graphml_File_Name+str('/centrality.csv')
filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
