#Routing Distances and Direct distances. 
##[Struct.Analysis]=group
##place_name=string gill ludhiana
##filename= string graphml_data
##location=folder 


import osmnx as ox, geopandas as gpd, pandas as pd
#matplotlib inline
#ox.config(log_file=True, log_console=True, use_cache=True)
#For converting unicode string of chracters to string
cname= place_name.encode('utf-8')
filename=filename.encode('utf-8')
location=location.encode('utf-8')

# create the street network within the city borders
G=ox.load_graphml(filename, folder=location)
# you can project the network to UTM (zone calculated automatically)
G = ox.project_graph(G)
fig, ax = ox.plot_graph(G)

# get the street network for a place, and its area in square meters
gdf = ox.gdf_from_place(cname)
gdf= ox.project_gdf(gdf)
fig, ax = ox.plot_shape(gdf)
area = ox.project_gdf(gdf).unary_union.area
# calculate basic and extended network stats, merge them together, and display
stats = ox.basic_stats(G, area=area)
df=pd.DataFrame.from_dict(stats, orient="index")
df.to_csv("/home/osmjit/Desktop/testdata/data.csv")

ex_stats=ox.extended_stats(G, connectivity=False, anc=False, ecc=False, bc=False, cc=False)
dfe=pd.DataFrame(ex_stats)
dfe.to_csv("/home/osmjit/Desktop/testdata/data_extended.csv")