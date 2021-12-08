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
import progressbar
from time import sleep
import math as mt
import numpy as np
# impor bigfloat
from math import exp, log
import numpy as np 

bar = progressbar.ProgressBar(maxval=20, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])




walk_dir = "/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/test"
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_NOV_2015/DistrictwiseNetworkAnalysisGraphml/ReachGravity"

bar.start()
for fname in iglob(walk_dir + '**/*.graphml'):
	getfilename=os.path.basename(fname)
	Folder_to_load_from=os.path.dirname(fname)
	G_simple=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
	print "Graph laoded"
	G = ox.get_largest_component(G_simple, strongly=True)
	print "G strong found"
	stats={}
	#Calculate the center of graph, the folowing statement would return a list
	center=nx.center(G)
	cenpoint=center[0]
	stats['center']=center 
	print "Calculated center"

	#radius=nx.radius(G)

	stats['radius_used']=10

	L=nx.ego_graph(G, cenpoint, radius=10, center=True, undirected=False, distance=None)
	n=L.number_of_nodes()

	stats['Reach'] =n
	print "Calculated Reach"

	#find the gravity

	list_nodes=[n for n in L.nodes_iter()]

	gravity={i:nx.single_source_dijkstra_path_length(L,i,weight='length') for i in list_nodes}
	print "start Calculating gravity"
	gravity1=gravity
	for key, value in gravity1.iteritems():
		for key1, vl in value.iteritems():
			#m=np.exp(.1813*vl)
			vl=(1/(np.exp(.1813*vl)))
			gravity1[key][key1]=vl  

	gravity_node={key: sum([v for k, v in values.items()]) for key, values in gravity1.iteritems()}

	#stats['gravity_of_node']=gravity_node


	total_gravity_network= float((sum(gravity_node.values())))/L.number_of_nodes() 
	print "Calculated total_gravity_network"
	print total_gravity_network

	stats['total_gravity_network']=total_gravity_network
	filename=os.path.splitext(getfilename)[0]
	filename = (filename + ".csv")
	filepath=save_dir+'/'+filename
	df=pd.DataFrame.from_dict(stats)
	df.to_csv(filepath)
bar.finish()

print "Success"

