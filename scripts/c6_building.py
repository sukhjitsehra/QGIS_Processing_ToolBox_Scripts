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

#description     :This file creates a plot: Calculates the development of all objects with a "building"-tag
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
SELECT
	(SELECT COUNT(id)
		
	FROM 
		hist_polygon 
	WHERE  tags ? 'building' AND visible = 'true' AND
		((version = (SELECT max(version) from hist_polygon as h where h.id = hist_polygon.id AND
		valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
		AND minor = (SELECT max(minor) from hist_polygon as h where h.id = hist_polygon.id AND h.version = hist_polygon.version AND
		(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))	
	) AS length, date_trunc('month', generate_series)::date
	
FROM generate_series(
	(SELECT date_trunc ('month',(
		SELECT MIN(valid_from) FROM hist_polygon)) as foo),  -- Select minimum date (month)
	(SELECT MAX(valid_from) FROM hist_polygon)::date,	-- Select maximum date
	interval '1 month')
;

  """)

except:
    QMessageBox.critical(None, "About Layer", "First Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)
    
# Plot (Bar-Chart)


# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col1', 'i4'), ('date', 'S20')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1']

# Converts date to a manageable date-format for matplotlib
dates = mdates.num2date(mdates.datestr2num(data['date']))
fig, ax = plt.subplots()

# Create barchart (x-axis=dates, y-axis=col1, ...)
ax.bar(dates, col1, width=15, align='center', color = '#2dd700')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x and y axis
plt.xlabel('Date')
plt.ylabel('Number of Buildings')

# Plot-title
plt.title("Development of the Number of Buildings")

# Save plot to *.jpeg-file
plt.savefig('pics/c6_building.jpeg')

plt.clf()