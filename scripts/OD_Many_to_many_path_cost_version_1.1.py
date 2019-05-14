#Routing Distances and Direct distances. 
##[Sehra]=group
##Host=string localhost
##Port=number 5432
##Database=string here_routing
##User=string postgres
##Password=string a
##Schema=string public
##Table=string ldh_here_mergedtwo
##Geometry_column=string geom
##Where_clause=string
##Unique_id_field_name=string id
#sql= string  'SELECT gid, link_id, ST_AsText(geom) from ldh_here_mergedtwo;'
##output=output vector
##QueryResult=output vector
#This Script can take data from POSTGIS database and then writes to the canvas. PLease look that in the psycopg2 connection the database name has to be given manually yet

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from processing.tools.vector import VectorWriter
import psycopg2


# Create uri from database connection options
uri = QgsDataSourceURI()
uri.setConnection(Host, str(Port), Database, User, Password)
uri.setDataSource(Schema, Table, Geometry_column, Where_clause, Unique_id_field_name)

# Create the vector layer
layer = QgsVectorLayer(uri.uri(), 'vlayer', 'postgres')
# Output the vector layer
if layer.isValid():

    # Create writer
    writer = VectorWriter(
        output,
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
    conn=psycopg2.connect(database=Database, host="localhost", user="postgres", password="a")
      #conn = psycopg2.connect("dbname= osm host='localhost' user='postgres' password='a'")
except:
    QMessageBox.critical(None, "About Layer", "Unable to connect to DB")
    
cur = conn.cursor()

#Change table name and look for the geometry column

sql = """ SELECT x.seq,x.end_vid, ST_AsText(y.geom) as geom, x.agg_cost FROM pgr_dijkstra(
 'SELECT gid as id, source, target,  cost FROM ldh_here_mergedtwo',
 array (SELECT DISTINCT ON(g2.gid)  g1.id FROM ldh_here_mergedtwo_vertices_pgr As g1, ldh_points_utm43 As g2   
 WHERE g1.id <> g2.gid   
 ORDER BY g2.gid, ST_Distance(g1.the_geom,g2.geom) ),
 array (SELECT DISTINCT ON(g2.gid)  g1.id FROM ldh_here_mergedtwo_vertices_pgr As g1, ldh_points_utm43 As g2   
 WHERE g1.id <> g2.gid   
 ORDER BY g2.gid, ST_Distance(g1.the_geom,g2.geom) ),
 false) as x left join ldh_here_mergedtwo as y on x.edge=y.gid
 where x.edge<>-1
"""
cur.execute(sql)
result = cur.fetchall()
#QMessageBox.information(None, "About Layer", cur.rowcount())
# Create writer

writer = VectorWriter(QueryResult, None,[QgsField("Sequence", QVariant.Int), QgsField("End Vertex", QVariant.Int), QgsField("COst", QVariant.Int)], layer.dataProvider().geometryType(), layer.crs())
#writer = VectorWriter(QueryResult, None,fields, layer.dataProvider().geometryType(), layer.crs())

# add a feature
for row in result:
    geo=row[2]
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromWkt(geo))
    fet.setAttributes([row[0],row[1],row[3]])
    writer.addFeature(fet)

conn.close()
