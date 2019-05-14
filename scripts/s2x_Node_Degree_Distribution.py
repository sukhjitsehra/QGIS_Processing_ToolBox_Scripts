#Finding the degree distribution of the graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
##Folder_to_save_graphs=folder
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
from processing.tools.vector import VectorWriter

Folder_to_load_from= '{}'.format(Folder_to_load_from)
#Folder_to_save_graphs='{}',format(Folder_to_save_graphs)
Folder_to_save_graphs=str(Folder_to_save_graphs)
#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

# create an undirected Graph from the MultiDiGraph, for those metrics that require it
#G_undir = nx.Graph(G)

# create a strongly connected graph

#G_strong = ox.get_largest_component(G, strongly=True)

stats = {}
statsdegree={}
#Find the degree distribution of the road network, this is not very significant part but tell about the graph
deg=nx.degree(G)
in_deg=dict(G.in_degree_iter())
out_deg=dict(G.out_degree_iter())
def degreeDis(deg):
    N=len(deg)
    n=max(deg.values())
    degcnt={}
    '''chnage the range from 2 to n+1 if you want to only nodes more that one degree'''
    degcnt={i: sum( x == i for x in deg.values()) for i in range(1,n+1)}
    for key, value in degcnt.items():
    	# This returns here the probability distribution of network
        degcnt[key] = float(value)/N
    return degcnt

def indegreeDis(deg):	#Function to find the in_degree of network
    N=len(deg)
    n=max(in_deg.values())
    in_degcnt={}
    in_degcnt={i: sum( x == i for x in in_deg.values()) for i in range(0,n+1)}
    for key, value in in_degcnt.items():
        in_degcnt[key] = float(value)/N
    return in_degcnt

def outdegreeDis(deg):	#Function to find the out_degree of network
    N=len(deg)
    n=max(out_deg.values())
    out_degcnt={}
    out_degcnt={i: sum( x == i for x in out_deg.values()) for i in range(0,n+1)}
    for key, value in out_degcnt.items():
        out_degcnt[key] = float(value)/N
    return out_degcnt




# For plotting probability of node distribution 

D=degreeDis(deg)
plt.subplot(311)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('Degree')
plt.ylabel('% of total degree')
#plt.show()
degloc=Folder_to_save_graphs+str('/degree.pdf')
#plt.savefig(degloc)
D=indegreeDis(in_deg)
plt.subplot(312)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('in_degree')
plt.ylabel('% of  in-degree')
#plt.show()
in_degloc=Folder_to_save_graphs+str('/indegree.pdf')
#plt.savefig(in_degloc)

D=outdegreeDis(out_deg)
plt.subplot(313)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('out_degree')
plt.ylabel('% of  out-degree')
#plt.show()
out_degloc=Folder_to_save_graphs+str('/outdegree.pdf')
plt.show()
plt.savefig(out_degloc)
statsdegree['node_degree_distribution']=degreeDis(deg)
statsdegree['node_in_degree_distribution']=indegreeDis(in_deg)
statsdegree['node_out_degree_distribution']=outdegreeDis(out_deg)


# joined_in_out_deg = defaultdict(list)
# for k, v in chain(in_deg.items(), out_deg.items()):
#     joined_in_out_deg[k].append(v)

# average degree of the neighborhood of each node, and average for the graph
avg_neighbor_degree = nx.average_neighbor_degree(G)
stats['avg_neighbor_degree'] = avg_neighbor_degree
stats['avg_neighbor_degree_avg'] = sum(avg_neighbor_degree.values())/len(avg_neighbor_degree)

# average weighted degree of the neighborhood of each node, and average for the graph
avg_weighted_neighbor_degree = nx.average_neighbor_degree(G, weight='length')
stats['avg_weighted_neighbor_degree'] = avg_weighted_neighbor_degree
stats['avg_weighted_neighbor_degree_avg'] = sum(avg_weighted_neighbor_degree.values())/len(avg_weighted_neighbor_degree)


# # degree centrality for a node is the fraction of nodes it is connected to
degree_centrality = nx.degree_centrality(G)
stats['degree_centrality'] = degree_centrality
stats['degree_centrality_avg'] = sum(degree_centrality.values())/len(degree_centrality)

# #print("degree_centrality_avg:",stats['degree_centrality_avg'])

# # calculate clustering coefficient for the nodes
# stats['clustering_coefficient'] = nx.clustering(G_undir)

# # average clustering coefficient for the graph
# stats['clustering_coefficient_avg'] = nx.average_clustering(G_undir)

# # calculate weighted clustering coefficient for the nodes
# #stats['clustering_coefficient_weighted'] = nx.clustering(G_undir, weight='length')
# #print(stats['clustering_coefficient_avg'])
# # node connectivity is the minimum number of nodes that must be removed to disconnect G or render it trivial
# stats['node_connectivity'] = nx.node_connectivity(G_strong)
# # # edge connectivity is equal to the minimum number of edges that must be removed to disconnect G or render it trivial
# stats['edge_connectivity'] = nx.edge_connectivity(G_strong)
# # # if True, calculate average node connectivity


# # # mean number of internally node-disjoint paths between each pair of nodes in G
# # # i.e., the expected number of nodes that must be removed to disconnect a randomly selected pair of non-adjacent nodes
# stats['node_connectivity_avg'] = nx.average_node_connectivity(G)

# # print(stats['node_connectivity'])
# # print(stats['edge_connectivity'])
# # print(stats['node_connectivity_avg'])
# # print(nx.info(G_strong))
# # print(stats['node_degree_distribution'])
import csv
filepath=Folder_to_save_graphs+str('/Degree_other.csv')
filepath1=Folder_to_save_graphs+str('/Degree_dis.csv')
df=pd.DataFrame.from_dict(stats)
df1=pd.DataFrame.from_dict(statsdegree)
df.to_csv(filepath)
df1.to_csv(filepath1)
