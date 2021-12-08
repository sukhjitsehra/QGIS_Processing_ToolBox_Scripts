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
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistricwiseStats/InterGraphAnalysis"


for fname in iglob(walk_dir + '**/*.graphml'):
	getfilename=os.path.basename(fname)
	Folder_to_load_from=os.path.dirname(fname)
	G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
	print 'graph loaded'
	#Calculate the Extended stats
	#Calculate the Extended stats
	stats={}
	#Calculate the number of nodes in the graph
	v= nx.number_of_nodes(G)

	#Calculate the number of edges in the graph

	e=nx.number_of_edges(G)

	#gamma index of graph

	#gamma=e/float((v*v-v)/2) for non-planer graph
	gamma=e/float(3*v-2)
	stats['edges']=e
	stats['nodes']=v
	stats['gamma']=gamma

	G1=G.to_undirected()
	#Count the number of connected components
	g=nx.number_connected_components(G1)

	stats['number_of_connected_component']=g
	print 'Calculated number of connected components'
	# Find the cyclomatic number

	cyclomatic_number= e-v+g

	stats['cyclomatic_number']=cyclomatic_number
	print 'Calculated cyclomatic_number'
	# Find The maximum number of cycles

	#mc=float((v*v-v)/2) - (v-1) #seems like for non-planer graph

	#stats['maximum_number_of_cycles']=mc
	#Redundancy Index
	# ri=(e-v+g)/float(((v*v-v)/2)-v+1) #seems like for non-planer graph

	# stats['redundancy_Index']=ri
	#Calculate Beta
	beta=e/float(v)
	stats['Beta']=beta 
	print 'Calculated beta'

	#Completeness
	Comp=e/float(v*v-v)
	stats['Completeness']=Comp
	print 'Calculated Completeness'




	#calculate alpha
	alpha= cyclomatic_number/float(2*v-5)	
	stats['alphaindex']=alpha
	filename=os.path.splitext(getfilename)[0]
	filename = (filename + ".csv")
	filepath=save_dir+'/'+filename
	df=pd.DataFrame.from_dict(stats,orient='index')
	df.to_csv(filepath)
	print 'Calculated and saved all paratmeters'

