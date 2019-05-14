#Finding the degree centranality of the graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
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

Folder_to_load_from= '{}'.format(Folder_to_load_from)

#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)
G = ox.project_graph(G)
fig, ax = ox.plot_graph(G)