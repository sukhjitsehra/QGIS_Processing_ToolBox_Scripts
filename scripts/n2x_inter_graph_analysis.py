#Create graph using networkx 
##[Struct.Analysis]=group
##layer=vector
##Folder_to_save_graphs=folder
##Name_of_stat_file=string centrality.csv

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


layer= '{}'.format(layer)
#folder_to_save_graphml='{}'.format(folder_to_save_graphml)
#graphml_file_name='{}'.format(graphml_file_name)
#create graph
G=nx.read_shp(layer,simplify=True)
print nx.info(G)


stats={}
#Calculate the number of nodes in the graph
v= nx.number_of_nodes(G)

#Calculate the number of edges in the graph

e=nx.number_of_edges(G)

#gamma index of graph

gamma=e/float((v*v-v)/2)

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

mc=float((v*v-v)/2) - (v-1)

stats['maximum_number_of_cycles']=mc
#Redundancy Index
ri=(e-v+g)/float(((v*v-v)/2)-v+1)

stats['redundancy_Index']=ri

filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats.items())
df.to_csv(filepath)



