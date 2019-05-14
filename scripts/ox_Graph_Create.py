#Finding the degree centranality of the graph 
##[Struct.Analysis]=group
##Name_of_Place=string Patiala,Punjab
##folder_to_save_graphml=folder 
##graphml_file_name=string graph.graphml

import osmnx as ox, geopandas as gpd, networkx as nx
from networkx.algorithms import centrality as cen
from itertools import chain
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import progressbar
import shapefile
import progressbar
import pyproj
import json
import shp2osmnx as s2nx

Name_of_Place=str(Name_of_Place)
# get the boundary polygon for project it to UTM, and plot it
city = ox.gdf_from_place(Name_of_Place)
city = ox.project_gdf(city)
fig, ax = ox.plot_shape(city, figsize=(3,3))
figpoly=folder_to_save_graphml+str('/polygon.pdf')
plt.savefig(figpoly)
G = ox.graph_from_place(Name_of_Place,network_type='drive')
G_projected = ox.project_graph(G)
fig, ax = ox.plot_graph(G_projected)
fignet=folder_to_save_graphml+str('/network.pdf')
plt.savefig(fignet)

#save graph

ox.save_load.save_graphml(G, filename=graphml_file_name, folder=folder_to_save_graphml)
