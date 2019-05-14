#Routing Distances and Direct distancesusing OSM Data
##[Sehra]=group
##Host=string localhost
##Port=number 5432
##Database=string pb_osm_routing_utm43
##User=string postgres
##Password=string a
##Schema=string public
##Table=string ways
##pointTable=string pb_points
##Geometry_column=string the_geom
##Where_clause=string
##Unique_id_field_name=string gid
#sql= string  'SELECT gid, link_id, ST_AsText(geom) from ldh_here_mergedtwo;'
##inputRoutingLayer=output vector
##RoutesGeomLayer=output vector
##ShortestDistanceLayer= output vector
#This Script can take data from POSTGIS database and then writes to the canvas. PLease look that in the psycopg2 connection the database name has to be given manually yet

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from processing.tools.vector import VectorWriter
import psycopg2


# Create uri from database connection options
uri = QgsDataSourceURI()
uri.setConnection(Host,str(Port),Database,User,Password)
uri.setDataSource(Schema, Table, Geometry_column, Where_clause, Unique_id_field_name)

# Create the vector layer
layer = QgsVectorLayer(uri.uri(), 'vlayer', 'postgres')
# Output the vector layer
if layer.isValid():
    # Create writer
    writer = VectorWriter(
        inputRoutingLayer,
        None,
        layer.dataProvider().fields(),
        layer.dataProvider().geometryType(),
        layer.crs()
    )

    # Export features
    features = layer.getFeatures()
    for feat in features:
        writer.addFeature(feat)

    del writer

else:
    progress.setText('<b>## The layer is invalid - Please check the connection parameters.</b>')


try:
    conn=psycopg2.connect(database=Database, host=Host, user= User, password= Password)
      #conn = psycopg2.connect("dbname= osm host='localhost' user='postgres' password='a'")
except:
    QMessageBox.critical(None, "About Layer", "Unable to connect to DB")
    
cur = conn.cursor()

#Change table name and look for the geometry column

sql= """ SELECT
X.seq,X.path_seq,ST_AsText(y.the_geom), X.start_vid, X.end_vid,x.cost, X.agg_cost, (SELECT  place 
FROM  {0} As s 
ORDER BY Z.the_geom <-> s.geom LIMIT 1),
(SELECT  place 
FROM {0} As s 
ORDER BY W.the_geom <-> s.geom LIMIT 1)
FROM pgr_dijkstra(
'SELECT gid as id, source, target,  cost, reverse_cost FROM {1}',
array(SELECT  distinct on (g2.gid)  g1.id  FROM {1}_vertices_pgr As g1,  {0} As g2 order by  g2.gid, g1.the_geom <-> g2.geom ),
array(SELECT  distinct on (g2.gid) g1.id FROM {1}_vertices_pgr As g1, {0} As g2 order by  g2.gid, g1.the_geom <-> g2.geom ),
true) as X INNER JOIN {1}_vertices_pgr As Z ON X.start_vid = Z.id 
INNER JOIN {1}_vertices_pgr As W ON X.end_vid = W.id 
inner join {1} as y on x.edge=y.gid
""".format(pointTable,Table)
cur.execute(sql)
result = cur.fetchall()

# Create writer

writer = VectorWriter(RoutesGeomLayer, None,[QgsField("Sequence", QVariant.Double),QgsField("Path_Sequence", QVariant.Double), QgsField("Start Vertex", QVariant.Double),QgsField("End Vertex", QVariant.Double),QgsField("Cost", QVariant.Double),QgsField("Aggregated Cost", QVariant.Double),QgsField("Source", QVariant.String),QgsField("Destination", QVariant.String) ], layer.dataProvider().geometryType(), layer.crs())
#writer = VectorWriter(QueryResult, None,fields, layer.dataProvider().geometryType(), layer.crs())

# add a feature
for row in result:
    geo=row[2]
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromWkt(geo))
    fet.setAttributes([row[0],row[1],row[3], row[4],row[5],row[6],row[7],row[8]])
    writer.addFeature(fet)
del writer 

#Only Aggregated Cost

sql1 = """ SELECT
X.seq, X.start_vid, X.end_vid, COALESCE(X.start_vid || '-' || X.end_vid) as Segment,
(SELECT  place FROM {0} As s 
ORDER BY Z.the_geom <-> s.geom LIMIT 1),
(SELECT  place FROM {0} As s 
ORDER BY W.the_geom <-> s.geom LIMIT 1), 
ST_AsText((SELECT  s.geom  FROM {0} As s 
ORDER BY Z.the_geom <-> s.geom LIMIT 1)) as geom,
X.agg_cost
FROM pgr_dijkstra(
'SELECT gid as id, source, target,  cost, reverse_cost FROM {1}',
array(SELECT  distinct on (g2.gid)  g1.id  FROM {1}_vertices_pgr As g1, {0} As g2 order by  g2.gid, g1.the_geom <-> g2.geom ),
array(SELECT  distinct on (g2.gid) g1.id FROM {1}_vertices_pgr As g1, {0} As g2 order by  g2.gid, g1.the_geom <-> g2.geom ),
true) as X INNER JOIN {1}_vertices_pgr As Z ON X.start_vid = Z.id 
INNER JOIN {1}_vertices_pgr As W ON X.end_vid = W.id 
where X.edge=-1
order by X.seq
""".format(pointTable,Table)
cur.execute(sql1)
result1 = cur.fetchall()
#QMessageBox.information(None, "About Layer", "Second Query Executed")
# Create writer

writer1 = VectorWriter(ShortestDistanceLayer, None,[QgsField("Sequence", QVariant.Int), QgsField("Start Vertex", QVariant.Int),QgsField("End Vertex", QVariant.Int),QgsField("Segment", QVariant.String),QgsField("Start", QVariant.String),QgsField("Destination", QVariant.String),QgsField("Aggregated Cost", QVariant.Double)], QGis.WKBPoint, layer.crs())

# add a feature
for row in result1:
    geo=row[6]
    fet1 = QgsFeature()
    fet1.setGeometry(QgsGeometry.fromWkt(geo))
    fet1.setAttributes([row[0],row[1],row[2], row[3],row[4],row[5],row[7]])
    writer1.addFeature(fet1)
del writer1 
# For converting a vector Layer to CSV
#QgsVectorFileWriter.writeAsVectorFormat(result1, "/home/a/xy.csv", "utf-8", None, "CSV", layerOptions ='GEOMETRY=AS_WKT')


conn.close()
