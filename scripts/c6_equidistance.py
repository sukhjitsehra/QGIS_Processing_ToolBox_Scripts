##[OSM-History]=Group
##Host=String localhost
##Port=Number 5432
##Database=String hist_osm_pb 
##User=String postgres
##Password=String a

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from processing.tools.vector import VectorWriter
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pylab

#description     :This file creates a plot: Calculates the development of the equidistance between version 1 an the currently valid version of a polygon with a "natural" or "landuse"-tag
#author          :Sukhjit Singh Sehra modified the code of Christopher Barron @ http://giscience.uni-hd.de/
#date            :11.10.2016
#version         :1.0
#usage           :This script is designed to work with historic data imported into PostgreSQL database using osm-hisotry-renderer tool, for more information please visit https://github.com/sukhjitsehra/iOSMAnalyzer
#Notes            : mind that by default DB user is considered as "postgres". please look at "OWNER TO postres" in the code.

#For creating connection with DB
try:
  conn_string="dbname= %s user= %s host= %s password= %s" %(Database, User, Host, Password)
  #conn_string="dbname= %s user= %s host= %s password= %s" %(db.g_my_dbname, db.g_my_username, db.g_my_hostname, db.g_my_dbpassword)
  #print "Connecting to database\n->%s" % (conn_string)
      
# Verbindung mit der DB mittels psycopg2 herstellen
  conn = psycopg2.connect(conn_string)
  #QMessageBox.critical(None, "About Layer", "Connection to DB Sucessful")
except:
 QMessageBox.critical(None, "About Layer", "Connection to database Failed")

# New cursor method for sql
cur = conn.cursor()

# Execute SQL query. For more than one row use three '"'
try:
  cur.execute(""" 
 -- If a polygon was merged or split new polygons arise. Their size and amount of vertices can differ considerably from each other
  -- Therefore: If the difference in size of the two polygons is +- 50 % a split or merge is most likely. The value was tested iterative
  -- Join currently valid osm-id of an natural or landuse polygon with their first version and calculate the difference
  SELECT 
	  round(T2.equidistance_first::numeric, 3)::float AS equidistance_first,
	  round(T1.equidistance_new::numeric, 3)::float AS equidistance_new
  FROM 
	  -- equidistance, amount of vertices and perimeter of the currently valid natural and landuse-tags
	  (SELECT id, version, minor, 
	  ((ST_Perimeter(geom))/(ST_NPoints(geom))) as equidistance_new, 
	  (ST_NPoints(geom)) AS vertices_new, 
	  (ST_Perimeter(geom)) AS Umfang,
	  (ST_Area(ST_GeographyFromText(ST_AsText(ST_Transform(geom,4326))))) AS flaeche_new -- area in m²
	  FROM 
		  hist_polygon 
	  WHERE visible = 'true' AND
		  (tags ? 'natural' OR tags ? 'landuse') AND 
		  (version = (SELECT max(version) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND
			  (valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		  AND minor = (SELECT max(minor) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND h.version = hist_polygon.version AND
			  (valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))))) 
  T1 
  JOIN 
	  -- equidistance and amount of vertices of every natural and landuse-tags ever created
	  (SELECT id, version, minor, 
	  ((ST_Perimeter(geom))/(ST_NPoints(geom))) AS equidistance_first, 
	  (ST_NPoints(geom)) AS vertices_first,
	  (ST_Area(ST_GeographyFromText(ST_AsText(ST_Transform(geom,4326))))) AS flaeche_first -- area in m²
	  FROM 
		  hist_polygon 
	  WHERE 
		  (tags ? 'natural' OR tags ? 'landuse') AND version=1 AND minor=0
	  ORDER BY id asc) 
  T2
  ON T1.id = T2.id 
  WHERE
	  -- Filter: only choose polygons where the newest polygon is within the range of +- 50% of the created polygon
	  (50 < (T1.flaeche_new / T2.flaeche_first *100.00)) AND ((T1.flaeche_new / T2.flaeche_first *100.00) < 150)
  ORDER BY equidistance_first ASC;

  """)

except:
    QMessageBox.critical(None, "About Layer", "First Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)
    
# Plot (Line-Chart)


# Datatypes of the returning data
datatypes = [('col1', 'double'),('col2', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1']
col2 = data['col2']

# Development of the equidistance. Subtract equidistance from the initially created polygon from its corresponding one which is recently valid
devel_equ = col1 - col2

fig, ax = plt.subplots()

# Create linechart
plt.plot(devel_equ, color = '#ff6700', linewidth=2, label='Development of the Equidistance')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.xaxis.grid(color='gray', linestyle='dashed')
ax.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x and y axis
plt.xlabel('Polygons with a "natural" or "landuse"-Tag')
plt.ylabel('Change of Equidistance [m]')

# place legend
ax.legend(loc='upper center', prop={'size':12})

# Plot-title
plt.title('Equidistance Development of Polygons with "natural" or "landuse"-Tag"')

# Save plot to *.jpeg-file
plt.savefig('pics/c6_equidistance.jpeg')

plt.clf()