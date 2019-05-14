#Finding the extended stats of the road graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
#Polygon_layer=file 
#Polygon_in_crs=string EPSG:32643
#Buffer_around_polygon=number 0
##connectivity=Boolean False
##average_node_connectivity=Boolean False
##eccentricity=Boolean False
##betweenness_centrality=Boolean False
##closeness_centrality=Boolean False
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

#Polygon_layer='{}'.format(Polygon_layer)
#Polygon_in_crs='{}'.format(Polygon_in_crs)
#Folder_to_load_from= '{}'.format(Folder_to_load_from)
Folder_to_save_graphs=str(Folder_to_save_graphs)
Name_of_stat_file='{}'.format(Name_of_stat_file)


#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

#Calculate the extended stats
stats=ox.extended_stats(G, connectivity=connectivity, anc=average_node_connectivity, ecc=eccentricity, bc=betweenness_centrality, cc=closeness_centrality)
#statsfile=Graphml_File_Name+str('/centrality.csv')
filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
