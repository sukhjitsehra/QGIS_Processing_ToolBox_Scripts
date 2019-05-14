#Direct distances. 
##[Sehra]=group
##Host=string localhost
##Port=number 5432
##Database=string here_routing
##User=string postgres
##Password=string a
##Schema=string public
##Table=string ldh_points_utm43
##Routing_Table=string ldh_here_mergedtwo
##Geometry_column=string geom
##Where_clause=string
##Unique_id_field_name=string id
##inputPointLayer=output vector
##point2Point_Distance=output vector

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
        inputPointLayer,
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
    conn=psycopg2.connect(database=Database, host=Host, user=User, password=Password)
      #conn = psycopg2.connect("dbname= osm host='localhost' user='postgres' password='a'")
except:
    QMessageBox.critical(None, "About Layer", "Unable to connect to DB")
    
cur = conn.cursor()

#Change table name and look for the geometry column

sql = """ select ST_AsText(g1.geom), (SELECT  s.id 
FROM {1}_vertices_pgr As s 
ORDER BY g1.geom <-> s.the_geom LIMIT 1),
(SELECT  s.id FROM {1}_vertices_pgr As s 
ORDER BY g2.geom <-> s.the_geom LIMIT 1),
COALESCE((SELECT  s.id  FROM {1}_vertices_pgr As s 
ORDER BY g1.geom <-> s.the_geom LIMIT 1) || '-' || (SELECT  s.id 
FROM {1}_vertices_pgr As s 
ORDER BY g2.geom <-> s.the_geom LIMIT 1)) as Segment,
g1.place,g2.place, 
ST_Distance(g1.geom, g2.geom)  from {0} as g1 inner join  {0} as g2 on g1.gid!=g2.gid
""".format(Table,Routing_Table)
cur.execute(sql)
result = cur.fetchall()

# Create writer

writer = VectorWriter(point2Point_Distance, None,[QgsField("Start Node Id", QVariant.Int), QgsField("End Node Id", QVariant.Int),QgsField("Segment", QVariant.String),QgsField("Source", QVariant.String), QgsField("Destination", QVariant.String),QgsField("Direct Cost", QVariant.Double)], QGis.WKBPoint, layer.crs())

# add a feature
for row in result:
    geo=row[0]
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromWkt(geo))
    fet.setAttributes([row[1],row[2],row[3],row[4],row[5],row[6]])
    writer.addFeature(fet)
del writer 

conn.close()