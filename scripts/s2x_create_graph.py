#Finding the degree centranality of the graph 
##[Struct.Analysis]=group
##layer=vector
##CRS_of_layer=string EPSG:32643
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

layer= '{}'.format(layer)
folder_to_save_graphml='{}'.format(folder_to_save_graphml)
graphml_file_name='{}'.format(graphml_file_name)


#create graph
G=s2nx.graph_from_shapefile(layer,CRS_of_layer)
ox.save_load.save_graphml(G, filename=graphml_file_name, folder=folder_to_save_graphml)
#G = ox.project_graph(G)
#fig, ax = ox.plot_graph(G)