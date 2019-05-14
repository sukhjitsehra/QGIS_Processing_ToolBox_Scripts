##[Sehra]=group
##Create vector layer from postgis table=name
##Host=string localhost
##Port=number 5432
##Database=string osm
##User=string postgres
##Password=string a
##Schema=string public
##Table=string ldh_jan_2016
##Geometry_column=string geom
##Where_clause=string
##Unique_id_field_name=string id
##output=output vector
##Query_Result=output vector
#Incomplete
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from processing.tools.vector import VectorWriter

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



# get the active layer
#layer = iface.activeLayer()
    # get the underlying data provider
#iface.showAttributeTable(iface.activeLayer())

#uri = QgsDataSourceURI()
# set host name, port, database name, username and password
#uri.setConnection("localhost", "5432", "osm", "postgres", "a")
# set database schema, table name, geometry column and optionally
# subset (WHERE clause)
#uri.setDataSource("public", "ldh_jan_2016", "geom", "")
#layer = QgsVectorLayer(uri.uri(), "LayerAdded", "postgres")

provider = layer.dataProvider()
if provider.name() == 'postgres':
    uri = QgsDataSourceURI(provider.dataSourceUri())
    print uri.uri()
    #create a PostgreSQL connection using QSqlDatabase
    db = QSqlDatabase.addDatabase('QPSQL')
        # check to see if it is valid
    if db.isValid():
            #print "QPSQL db is valid"
            # set the parameters needed for the connection
            db.setHostName(uri.host())
            db.setDatabaseName(uri.database())
            db.setPort(int(uri.port()))
            db.setUserName(uri.username())
            db.setPassword(uri.password())
            # open (create) the connection
            if db.open():
                QMessageBox.information(None, "About Layer", uri.uri())
                #print "Opened %s" % uri.uri()
                # execute a simple query 
                query = db.exec_("""select gid from ldh_jan_2016 limit 5""")
                # loop through the result set and print the name
                # Create writer
                writer = VectorWriter(Query_Result, None, provider.fields(), provider.geometryType(), layer.crs())
                #qfeatures=query.getFeatures()
                while query.next():
                    feat = query.value(0)
                    
                    
                    #writer.addFeature(record)
                        
                    #print record.value(0)
                    #print record.field('name').value().toString()
            else:
                err = db.lastError()
                print err.driverText()

