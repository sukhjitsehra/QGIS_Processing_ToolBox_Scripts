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
save_dir="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/OSMData/NetworkAnalysis/OSM_FEB_2017/DistricwiseStats/ExtendedStats"



for fname in iglob(walk_dir + '**/*.graphml'):
	getfilename=os.path.basename(fname)
	Folder_to_load_from=os.path.dirname(fname)
	G=ox.save_load.load_graphml(getfilename, folder=Folder_to_load_from)
	#Calculate the Extended stats
	stats=ox.extended_stats(G, connectivity=False, anc=False, ecc=False, bc=True, cc=True)
	filename=os.path.splitext(getfilename)[0]
	filename = (filename + ".csv")
	filepath=save_dir+'/'+filename
	df=pd.DataFrame.from_dict(stats)
	df.to_csv(filepath)