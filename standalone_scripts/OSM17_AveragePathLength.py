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
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
import matplotlib.pyplot as plt
from scipy.stats import norm





walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistricwiseStats/AveragepathLength"

for fname in iglob(walk_dir + '**/*.graphml'):
    getfilename=os.path.basename(fname)
    Folder_to_load_from=os.path.dirname(fname)
    G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
    filename=os.path.splitext(getfilename)[0]
    stats = {}
    print 'script started'
    #average shortest path length of graph
    mean=nx.average_shortest_path_length(G,weight='length')

    stats['average_shortest_path_length']=mean
    # find the all_pairs_dijkstra_path_length
    
    # filename=os.path.splitext(getfilename)[0]
    filename = (filename + ".csv")
    filepath=save_dir+'/'+filename
    df=pd.DataFrame.from_dict(stats,orient='index')
    df.to_csv(filepath)