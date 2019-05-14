#Routing Distances and Direct distances. 
##[Struct.Analysis]=group
##place_name=string gill ludhiana
##network_type=string drive_service
##filename= string graphml_data
##location=folder 

#download and construct street networks
# OSMnx lets you download street network data and build topologically-corrected street networks, project and plot the networks, and save the street network as SVGs, GraphML files, or shapefiles for later use. The street networks are directed and preserve one-way directionality. For a more in-depth demonstration of creating street networks, see this notebook.
# You can download a street network by providing OSMnx any of the following (demonstrated in the examples below):
# a bounding box
# a lat-long point plus a distance
# an address plus a distance
# a place name or list of place names (to automatically geocode and get the boundary of)
# a polygon of the desired street network's boundaries
# You can also specify several different network types:
# 'drive' - get drivable public streets (but not service roads)
# 'drive_service' - get drivable streets, including service roads
# 'walk' - get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
# 'bike' - get all streets and paths that cyclists can use
# 'all' - download all non-private OSM streets and paths (this is the default network type unless you specify a different one)
# 'all_private' - download all OSM streets and paths, including private-access ones
import osmnx as ox, geopandas as gpd, pandas as pd
#matplotlib inline
ox.config(log_file=True, log_console=True, use_cache=True)
#For converting unicode string of chracters to string
cname= place_name.encode('utf-8')
nettype=network_type.encode('utf-8')
filename=filename.encode('utf-8')
location=location.encode('utf-8')

# create the street network within the city borders
G = ox.graph_from_place(cname, network_type=nettype)

# you can project the network to UTM (zone calculated automatically)
G = ox.project_graph(G)
fig, ax = ox.plot_graph(G)

#Save the graph as Graphml
ox.save_graphml(G, filename=filename, folder=location)