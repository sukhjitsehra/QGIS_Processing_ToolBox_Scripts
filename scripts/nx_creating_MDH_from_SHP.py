#Finding the degree centranality of the graph 
##[Struct.Analysis]=group
##layer=file
import osmnx as ox, geopandas as gpd, networkx as nx
from networkx.algorithms import centrality as cen
from itertools import chain
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import progressbar
import shapefile
import progressbar
import pyproj
import json

layer= '{}'.format(layer)

def coordinate_transform(geojson, in_crs, out_crs='EPSG:4326'):
    """
    Convert Coordinates to the provided CRS in a GeoJSON object.

    :param geojson: JSON object of the GeoJSON Data
    :param in_crs: CRS of the shapeFile. Should be a string in 'EPSG:{number}' format.
    :param out_crs: CRS to which the coordinates of the geometry in the shapeFile is converted.
    Should be a string in 'EPSG:{number}' format. (Default = 'EPSG:4326')
    :return: JSON object of GeoJSON data
    """
    features = geojson['features']
    result = []
    print('Progress of conversion of CRS')
    size = len(features)
    #bar = progressbar.ProgressBar(max_value=size,
     #                             widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.SimpleProgress(),
      #                                     ' Geometries', ' ', progressbar.Percentage(), ' ',
       #                                    progressbar.AdaptiveETA()])
    #bar.start()
    for feature in features:
        #bar.update(features.index(feature))
        properties = feature['properties']
        geometry = feature['geometry']
        converted_points = []
        if geometry['type'] == 'Point':
            point = geometry['coordinates']
            projfrom = pyproj.Proj(init=in_crs)
            projto = pyproj.Proj(init=out_crs)
            point = pyproj.transform(projfrom, projto, point[0], point[1])
            converted_points.append(point)
            converted_geometry = {"type": "Point", "coordinates": converted_points}
        elif geometry['type'] == 'LineString':
            for point in geometry['coordinates']:
                p1 = pyproj.Proj(init=in_crs)
                p2 = pyproj.Proj(init=out_crs)
                point = pyproj.transform(p1, p2, point[0], point[1])
                converted_points.append(point)
            converted_geometry = {"type": "LineString", "coordinates": converted_points}
        elif geometry['type'] == 'Polygon':
            for poly in geometry['coordinates']:
                converted_poly = []
                for point in poly:
                    p1 = pyproj.Proj(init=in_crs)
                    p2 = pyproj.Proj(init=out_crs)
                    point = pyproj.transform(p1, p2, point[0], point[1])
                    converted_poly.append(point)
                converted_points.append(converted_poly)
            converted_geometry = {"type": "Polygon", "coordinates": converted_points}
        else:
            converted_geometry = {}
        converted_feature = {'geometry': converted_geometry, 'properties': properties}
        result.append(converted_feature)
    #bar.finish()
    return {"type": "FeatureCollection",
            "features": result}


def verify_standard(geojson):
    return


def to_standard(field_names, standards=None):
    """
    Convert Non-Standard Field Names to Standard.

    :param field_names: array of field names.
    :param standards: dict object contain the mapping of non standard field names to standard.
    example = {
        "LINK_ID": "osm_id",
        "DIRONSIGN":"oneway"
    }
    json format Key:Value
    where
        Key is the Field Name from the shapeFile.
        Value is the standard to convert it to.

    :return: array of field names.
    """
    if isinstance(standards,str):
        standards = json.loads(standards)
    standard = standards
    fields = []
    for field in field_names:
        if field in standard:
            field = standard[field]
        fields.append(field)
    return fields

def get_geojson(buffer):
    """
    Format GeoJSON from the array object.

    :param buffer: array of features
    :return: JSON object of GeoJSON data
    """
    return {"type": "FeatureCollection",
            "features": buffer}


def node_exist(point, nodes):
    """
    Used to check of a node exist in the array of nodes.

    :param point: longitude and latitude of the node to be queried.
    :param nodes: Array object of the nodes.
    :return: Boolean
        True: if node exist.
        False: of node doesn't exist
    """
    for n in nodes:
        if n['lon'] == point[0] and n['lat'] == point[1]:
            return True
    return False


def find_node(point, nodes):
    """
    Find the node ID of a particular node from the array of nodes.

    :param point: longitude and latitude of the node to be queried.
    :param nodes: Array object of the nodes.
    :return: NodeID of the node being queried.
    """
    for n in nodes:
        if n['lon'] == point[0] and n['lat'] == point[1]:
            return n['id']


def get_node(nodeID, coordinates, properties):
    """
    Create the dict object of the node.

    :param nodeID: NodeID of the node being created.
    :param coordinates: longitude and latitude of the node to be created.
    :param properties: properties/tags of the node to be created.
    :return: dict object of the node.
    """
    return {'lon': coordinates[0],
            'id': nodeID,
            'lat': coordinates[1],
            'tags': properties,
            'type': 'node'}


def get_way(wayID, nodesIndex, properties):
    """
    Create the dict object of the way.

    :param wayID: WayID of the way to be created
    :param nodesIndex: Array of nodes IDs that forms the way.
    :param properties: properties/tags of the way to be created.
    :return: dict object of the way.
    """
    return {'type': 'way',
            'nodes': nodesIndex,
            'id': wayID,
            'tags': properties}


def polygon():
    return {}


osm_id_field_name = None

# Default standard for some known variations of field names in shapeFile
default_standard = {"LINK_ID": "osm_id",
                    "DIRONSIGN": "oneway",
                    "HIGHWAY_NM": "name",
                    "SUB_TYPE": "highway",
                    "FUNC_CLASS": "highway"}


def shp2geojson(shape_file_path, standards=None):
    """
    Convert ShapeFile to GeoJSON.

    :param shape_file_path: Path of the shapeFile to be converted.
    :param standards: Dict object used to convert non standard properties attributes to standard
    example = {
        "LINK_ID": "osm_id",
        "DIRONSIGN":"oneway"
    }
    json format Key:Value
    where:
        Key is the Field Name from the shapeFile.
        Value is the standard to convert it to.
    See documentation for more.
    :return: JSON object of GeoJSON Data
    """
    reader = shapefile.Reader(shape_file_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    if standards is not None:
        field_names = to_standard(field_names, standards=standards)
    buffer = []
    global osm_id_field_name
    if "osm_id" in field_names:
        osm_id_field_name = "osm_id"
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    return get_geojson(buffer)


def geojson2osm_json(geojson):
    """
    Convert GeoJSON to OSM JSON format.

    :param geojson: JSON object of the GeoJSON Data
    :return: JSON object of OSM JSON Data
    """
    features = geojson['features']
    n_index = 0
    nodes = []
    ways = []
    #print('Progress of conversion of shapeFile to OSM JSON')
    relations = []
    size = len(features)
    #bar = progressbar.ProgressBar(max_value=size,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.SimpleProgress(),' Geometries', ' ', progressbar.Percentage(), ' ',progressbar.AdaptiveETA()])
    #bar.start()
    for feature in features:
        # bar.update(features.index(feature))
        properties = feature['properties']
        if 'oneway' in properties:
            if isinstance(properties['oneway'], int):
                properties['oneway'] = str(properties['oneway'])
            elif isinstance(properties['oneway'], str):
                properties['oneway'] = str(properties['oneway']).lower()
        geometry = feature['geometry']
        if geometry['type'] == 'Point':
            #bar.update(features.index(feature))
            point = geometry['coordinates']
            if osm_id_field_name is not None:
                osmid = properties[osm_id_field_name]
            else:
                osmid = n_index
                n_index += 1
            if not node_exist(point, nodes):
                new_node = get_node(osmid, point, properties)
                nodes.append(new_node)
            else:
                find_node(point, nodes)  # if nodes exist at that point
        elif geometry['type'] == 'LineString':
            #bar.update(features.index(feature))
            nodes_index = []
            for point in geometry['coordinates']:
                if not node_exist(point, nodes):
                    emptynode = get_node(n_index, point, {})  # TODO find properties of new node is not exist
                    nodes_index.append(n_index)
                    n_index += 1
                    nodes.append(emptynode)
                else:
                    nodes_index.append(find_node(point, nodes))
            if osm_id_field_name is not None:
                osmid = properties[osm_id_field_name]
            else:
                osmid = n_index
                n_index += 1
            ways.append(get_way(osmid, nodes_index, properties))
        elif geometry['type'] == 'Polygon':
            #bar.update(features.index(feature))
            nodes_index = []
        elif geometry['type'] == 'MultiPolygon':
            #bar.update(features.index(feature))
            nodes_index = []
    final = []
    for n in nodes:
        final.append(n)
    for w in ways:
        final.append(w)
    #bar.finish()
    return [{'elements': final}]


def gdf_from_shapefile(path, in_crs=None, gdf_name='unnamed', buffer_dist=None):
    """
    Create a GeoDataFrame from a shapeFile.

    :param path: Path of the shapeFile.
    :param in_crs: CRS of the shapeFile. Should be a string in 'EPSG:{number}' format. (Default = 'EPSG:4326')
    :param gdf_name: Name of the GDF to be created.(default = unnamed)
    :param buffer_dist: distance to buffer around the place geometry, in meters. (default = None)
    :return: GeoDataFrame object of the shapeFile.
    """
    geojson = shp2geojson(path)
    if in_crs is not None:
        geojson = coordinate_transform(geojson, in_crs=in_crs)
    features = geojson['features']
    if len(features) > 0:
        gdf = gpd.GeoDataFrame.from_features(features)
        gdf.gdf_name = gdf_name
        gdf.crs = {'init': 'epsg:4326'}
        if buffer_dist is not None:
            gdf_utm = ox.project_gdf(gdf)
            gdf_utm['geometry'] = gdf_utm['geometry'].buffer(buffer_dist)
            gdf = ox.project_gdf(gdf_utm, to_latlong=True)
        return gdf
    else:
        gdf = gpd.GeoDataFrame()
        gdf.gdf_name = gdf_name
        return gdf


def graph_from_shapefile(path, custom_standards=None, name='unnamed', simplify=True):
    """
    Create Networkx Graph from the shapeFile provided.

    :param path: Path of the shapeFile.
    :param custom_standards: Dict object used to convert non standard properties attributes to standard
    example = {
        "LINK_ID": "osm_id",
        "DIRONSIGN":"oneway"
    }
    json format Key:Value
    where:
        Key is the Field Name from the shapeFile.
        Value is the standard to convert it to.
    See documentation for more.
    :param name: Name of the Graph to be created.(default = unnamed)
    :param simplify: Simplify the graph. (default = True)
    :return: Networkx MultiDiGraph
    """
    geojson = shp2geojson(path, custom_standards)
    json_data = geojson2osm_json(geojson)
    g = ox.create_graph(json_data, name)
    if simplify is True:
        g = ox.simplify_graph(g)
    return g

def get_largest_component(G, strongly=False):
    """
    Return the largest weakly or strongly connected component from a directed graph.
    Parameters
    ----------
    G : networkx multidigraph
    strongly : bool
        if True, return the largest strongly instead of weakly connected component
    Returns
    -------
    networkx multidigraph
    """


    original_len = len(list(G.nodes()))

    if strongly:
        # if the graph is not connected and caller did not request retain_all, retain only the largest strongly connected component
        if not nx.is_strongly_connected(G):
            G = max(nx.strongly_connected_component_subgraphs(G), key=len)
            
    else:
        # if the graph is not connected and caller did not request retain_all, retain only the largest weakly connected component
        if not nx.is_weakly_connected(G):
            G = max(nx.weakly_connected_component_subgraphs(G), key=len)
            
    return G



#create graph
G=graph_from_shapefile(layer)

# create an undirected Graph from the MultiDiGraph, for those metrics that require it
G_undir = nx.Graph(G)

# create a strongly connected graph

G_strong = get_largest_component(G, strongly=True)

stats = {}
#Find the degree distribution of the road network, this is not very significant part but tell about the graph
deg=nx.degree(G)
in_deg=dict(G.in_degree_iter())
out_deg=dict(G.out_degree_iter())
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




# For plotting probability of node distribution 
D=degreeDis(deg)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('Degree')
plt.ylabel('Fraction of nodes')
plt.show()


D=indegreeDis(in_deg)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('in_degree')
plt.ylabel('Fraction of nodes')
plt.show()

D=outdegreeDis(in_deg)
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.xlabel('out_degree')
plt.ylabel('Fraction of nodes')
plt.show()
stats['node_degree_distribution']=degreeDis(deg)
stats['node_in_degree_distribution']=indegreeDis(in_deg)
stats['node_out_degree_distribution']=outdegreeDis(out_deg)


joined_in_out_deg = defaultdict(list)
for k, v in chain(in_deg.items(), out_deg.items()):
    joined_in_out_deg[k].append(v)

# average degree of the neighborhood of each node, and average for the graph
avg_neighbor_degree = nx.average_neighbor_degree(G)
stats['avg_neighbor_degree'] = avg_neighbor_degree
stats['avg_neighbor_degree_avg'] = sum(avg_neighbor_degree.values())/len(avg_neighbor_degree)
	
#print("avg_neighbor_degree_avg:",stats['avg_neighbor_degree_avg'])
#print(G.degree())


# degree centrality for a node is the fraction of nodes it is connected to
degree_centrality = nx.degree_centrality(G)
stats['degree_centrality'] = degree_centrality
stats['degree_centrality_avg'] = sum(degree_centrality.values())/len(degree_centrality)

#print("degree_centrality_avg:",stats['degree_centrality_avg'])

# calculate clustering coefficient for the nodes
stats['clustering_coefficient'] = nx.clustering(G_undir)

# average clustering coefficient for the graph
stats['clustering_coefficient_avg'] = nx.average_clustering(G_undir)

# calculate weighted clustering coefficient for the nodes
#stats['clustering_coefficient_weighted'] = nx.clustering(G_undir, weight='length')
#print(stats['clustering_coefficient_avg'])
# node connectivity is the minimum number of nodes that must be removed to disconnect G or render it trivial
stats['node_connectivity'] = nx.node_connectivity(G_strong)
# # edge connectivity is equal to the minimum number of edges that must be removed to disconnect G or render it trivial
stats['edge_connectivity'] = nx.edge_connectivity(G_strong)
# # if True, calculate average node connectivity


# # mean number of internally node-disjoint paths between each pair of nodes in G
# # i.e., the expected number of nodes that must be removed to disconnect a randomly selected pair of non-adjacent nodes
stats['node_connectivity_avg'] = nx.average_node_connectivity(G)

# print(stats['node_connectivity'])
# print(stats['edge_connectivity'])
# print(stats['node_connectivity_avg'])
# print(nx.info(G_strong))
# print(stats['node_degree_distribution'])
