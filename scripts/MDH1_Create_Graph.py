#Finding the degree centranality of the graph 
##[Struct.Analysis]=group
##layer=file
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

#create graph
G=s2nx.graph_from_shapefile(layer)
ox.save_load.save_graphml(G, filename='layer.graphml', folder=None)
G = ox.project_graph(G)
fig, ax = ox.plot_graph(G)