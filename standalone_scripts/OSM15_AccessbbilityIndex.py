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
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
import matplotlib.pyplot as plt
from scipy.stats import norm




#walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/test"
#save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/AccessiblityIndex"

walk_dir="/Volumes/Data/experimentaldataMac/OSMDATA/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/Volumes/Data/experimentaldataMac/OSMDATA/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/AccessibilityIndex"

for fname in iglob(walk_dir + '**/*.graphml'):
    startTime = datetime.now()
    print startTime
    getfilename=os.path.basename(fname)
    Folder_to_load_from=os.path.dirname(fname)
    G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
    filename=os.path.splitext(getfilename)[0]
    stats = {}
    print 'Graph Loaded for {0}'.format(getfilename)
    #average shortest path length of graph
    print 'Started average_shortest_path_length'
    stats['average_shortest_path_length']=nx.average_shortest_path_length(G,weight='length')
    print 'Started average_shortest_path_length calculated for {0}'.format(getfilename)    # find the all_pairs_dijkstra_path_length
    length=nx.all_pairs_dijkstra_path_length(G, cutoff=15000, weight='length')
    stats['all_pairs_dijkstra_path_length']=length
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
    plt.xlabel('Normal Distribution')
    # plt.ylabel('% of indegree')
    #plt.show()
    #plt.show()
    graphname= (filename + "_AccessibilityIndex.pdf")
    out_degloc=save_dir+str('/')+graphname
    #plt.show()
    plt.savefig(out_degloc)
    # filename=os.path.splitext(getfilename)[0]
    filename = (filename + ".csv")
    filepath=save_dir+'/'+filename
    df=pd.DataFrame.from_dict(stats)
    df.to_csv(filepath)
    print datetime.now() - startTime