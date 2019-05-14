#Finding the density of the road graph 
##[Struct.Analysis]=group
##Folder_to_load_from=folder
##Graphml_File_Name=string graph.graphml
##Polygon_layer=file 
##Polygon_in_crs=string EPSG:32643
##Buffer_around_polygon=number 0
##Folder_to_save_graphs=folder
##Name_of_stat_file=string centrality.csv
import osmnx as ox, geopandas as gpd, networkx as nx
from networkx.algorithms import centrality as cen
from itertools import chain
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import shp2osmnx as s2nx
import csv

Polygon_layer='{}'.format(Polygon_layer)
Polygon_in_crs='{}'.format(Polygon_in_crs)
Folder_to_load_from= '{}'.format(Folder_to_load_from)
Folder_to_save_graphs=str(Folder_to_save_graphs)
Name_of_stat_file='{}'.format(Name_of_stat_file)
#Creating geodataframe from polygon shapefile

Poly_area=s2nx.gdf_from_shapefile(Polygon_layer,in_crs=Polygon_in_crs, buffer_dist=Buffer_around_polygon)
#calulate the area of the a

area = ox.project_gdf(Poly_area).unary_union.area

print area

#create graph
G=ox.save_load.load_graphml(Graphml_File_Name, folder=Folder_to_load_from)

#Calculate the basic stats
stats = ox.basic_stats(G, area=area)

stats['area']=area
#statsfile=Graphml_File_Name+str('/centrality.csv')
filepath=Folder_to_save_graphs+'/'+Name_of_stat_file
df=pd.DataFrame.from_dict(stats)
df.to_csv(filepath)
