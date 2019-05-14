#Finding the accessibility index of the road graph 
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

import numpy as np
import matplotlib.mlab as mlab
import math
from scipy.stats import norm

Folder_to_load_from= '{}'.format(Folder_to_load_from)
Folder_to_save_graphs=str(Folder_to_save_graphs)
Name_of_stat_file='{}'.format(Name_of_stat_file)

stats={}
#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

#average shortest path length of graph

stats['average_shortest_path_length']=nx.average_shortest_path_length(G,weight='length')


# find the all_pairs_dijkstra_path_length

stats['all_pairs_dijkstra_path_length']=nx.all_pairs_dijkstra_path_length(G, cutoff=15000, weight='length')

shortlengthsum={key: sum(value.itervalues()) for key, value in length.iteritems()}

Total=sum(shortlengthsum.values())

N=G.number_of_nodes()

Mean_length_shortest=float(Total)/N

dict2 = {key:float(value)/Mean_length_shortest for key, value in shortlengthsum.items()}

z=dict2.values()


std=np.std(z)

mean=np.mean(z)

mins=min(z)
maxs=max(z)

range = np.arange(mins, maxs, 0.1)

plt.plot(range, norm.pdf(range, mean, std))

plt.show()

filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
