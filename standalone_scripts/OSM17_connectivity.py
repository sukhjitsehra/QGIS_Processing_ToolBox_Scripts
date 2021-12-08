import osmnx as ox, geopandas as gpd, networkx as nx
from networkx.algorithms import centrality as cen
from itertools import chain
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import shp2osmnx as s2nx
import csv
import os
import sys
from glob import iglob
import time




walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistricwiseStats/ExtendedStats/others"


start_time = time.time()

for fname in iglob(walk_dir + '**/*.graphml'):
    getfilename=os.path.basename(fname)
    Folder_to_load_from=os.path.dirname(fname)
    G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
    stats={}
    G_strong = ox.get_largest_component(G, strongly=True)
    print "G_strong found"
    stats['node_connectivity'] = nx.node_connectivity(G_strong)

    # edge connectivity is equal to the minimum number of edges that must be
    # removed to disconnect G or render it trivial
    stats['edge_connectivity'] = nx.edge_connectivity(G_strong)
    print 'edge_connectivity calculated'
    stats['node_connectivity_avg'] = nx.average_node_connectivity(G)
    print 'node_connectivity_avg calcualted'
    # closeness_centrality = nx.closeness_centrality(G, distance='length')
    # stats['closeness_centrality'] = closeness_centrality
    # stats['closeness_centrality_avg'] = sum(closeness_centrality.values())/len(closeness_centrality)
    # betweenness_centrality = nx.betweenness_centrality(G, weight='length')
    # stats['betweenness_centrality'] = betweenness_centrality
    # stats['betweenness_centrality_avg'] = sum(betweenness_centrality.values())/len(betweenness_centrality)
    filename=os.path.splitext(getfilename)[0]
    filename = (filename + "CC.csv")
    filepath=save_dir+'/'+filename
    df=pd.DataFrame.from_dict(stats)
    df.to_csv(filepath)
    print 'all done - success'

print("%f seconds" % (time.time() - start_time))