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


walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistricwiseStats/eccentricity"

for fname in iglob(walk_dir + '**/*.graphml'):
    getfilename=os.path.basename(fname)
    Folder_to_load_from=os.path.dirname(fname)
    G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
    G_strong = ox.get_largest_component(G, strongly=True)
    print 'graph and strnog graph success'
    #Calculate the Extended stats
    stats={}
    #sp = {source:dict(nx.single_source_dijkstra_path_length(G_strong, source, weight='length')) for source in G_strong.nodes()}
    #eccentricity=nx.eccentricity(G_strong, sp=sp)
    eccentricity=nx.eccentricity(G_strong)
    stats['eccentricity_avg'] = sum(eccentricity.values())/len(eccentricity)
    # stats['eccentricity']=eccentricity
    print 'calculated eccentricity'
    diameter = nx.diameter(G_strong, e=eccentricity)
    stats['diameter'] = diameter
    # radius is the minimum eccentricity
    radius = nx.radius(G_strong, e=eccentricity)
    stats['radius'] = radius
    # center is the set of nodes with eccentricity equal to radius
    center = nx.center(G_strong, e=eccentricity)
    stats['center'] = center
    # periphery is the set of nodes with eccentricity equal to the diameter
    periphery = nx.periphery(G_strong, e=eccentricity)
    stats['periphery'] = periphery
    filename=os.path.splitext(getfilename)[0]
    filename = (filename + ".csv")
    filepath=save_dir+'/'+filename
    df=pd.DataFrame.from_dict(stats,orient='index')
    df.to_csv(filepath)


