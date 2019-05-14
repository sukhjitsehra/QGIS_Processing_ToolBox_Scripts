##[Sehra]=group
#Psycopg2 to Create vector layer from postgis table=name
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
#sql =  "SELECT gid, link_id, geom from ldh_here_mergedtwo"
sql = """SELECT X.seq,Z.link_id, Y.id, ST_AsText(Z.geom) As geom,  X.cost, X.agg_cost
FROM
pgr_Dijkstra(
'SELECT gid as id, source, target, cost_column As cost FROM ldh_here_mergedtwo',
45,
673,
FALSE
)  X INNER JOIN
ldh_here_mergedtwo_vertices_pgr AS Y ON X.node = Y.id LEFT JOIN
ldh_here_mergedtwo AS Z ON X.edge = Z.gid  where  X.edge<>-1
ORDER BY seq;"""
cur.execute(sql)
result = cur.fetchall()
#QMessageBox.information(None, "About Layer", "hello")
# Create writer
writer = VectorWriter(QueryResult, None,layer.dataProvider().fields(), layer.dataProvider().geometryType(), layer.crs())

# add a feature
for row in result:
    geo=row[3]
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromWkt(geo))
    fet.setAttributes([row[0]])
    writer.addFeature(fet)