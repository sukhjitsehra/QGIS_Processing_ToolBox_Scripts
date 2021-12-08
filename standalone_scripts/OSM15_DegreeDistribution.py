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




walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/DegreeDistribution"

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


for fname in iglob(walk_dir + '**/*.graphml'):
    getfilename=os.path.basename(fname)
    Folder_to_load_from=os.path.dirname(fname)
    G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
    filename=os.path.splitext(getfilename)[0]
    stats = {}
    #Find the degree distribution of the road network, this is not very significant part but tell about the graph
    deg=nx.degree(G)
    in_deg=dict(G.in_degree_iter())
    out_deg=dict(G.out_degree_iter())
    # For plotting probability of node distribution
    D=degreeDis(deg)
    plt.subplot(311)
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys())
    plt.xlabel('Degree')
    plt.ylabel('% of degree')
    #plt.show()
    # degloc=save_dir+str('/degree.pdf')
    #plt.savefig(degloc)
    D=indegreeDis(in_deg)
    plt.subplot(312)
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys())
    plt.xlabel('in_degree')
    plt.ylabel('% of indegree')
    #plt.show()
    # in_degloc=save_dir+str('/indegree.pdf')
    #plt.savefig(in_degloc)

    D=outdegreeDis(out_deg)
    plt.subplot(313)
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys())
    plt.xlabel('out_degree')
    plt.ylabel('% of outdegree')
    #plt.show()
    graphname= (filename + "degreeDistribution.pdf")
    out_degloc=save_dir+str('/')+graphname
    #plt.show()
    plt.savefig(out_degloc)
    stats['node_degree_distribution']=degreeDis(deg)
    stats['node_in_degree_distribution']=indegreeDis(in_deg)
    stats['node_out_degree_distribution']=outdegreeDis(out_deg)


    # filename=os.path.splitext(getfilename)[0]
    filename = (filename + ".csv")
    filepath=save_dir+'/'+filename
    df=pd.DataFrame.from_dict(stats)
    df.to_csv(filepath)