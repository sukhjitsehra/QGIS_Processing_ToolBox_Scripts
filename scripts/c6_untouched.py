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
#description     :This file creates a plot: Calculates the development of untouched points, lines and polygons of all OSM-features
#author          :Sukhjit Singh Sehra modified the code of Christopher Barron @ http://giscience.uni-hd.de/
#date            :09.10.2016
#version         :1.0
#usage           :This script is designed to work with historic data imported into PostgreSQL database using osm-hisotry-renderer tool, for more information please visit https://github.com/sukhjitsehra/iOSMAnalyzer

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

cur = conn.cursor()

# Execute SQL query. For more than one row use three '"'
try: 
      cur.execute("""
 SELECT 
	generate_series,
	--
	-- Points
	--
	-- To prevent a "division by zero" error this CASE WHEN ... THEN is needed
	CASE WHEN 
		(SELECT 
			count (id) 
		FROM 
			hist_point 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_point AS h WHERE h.id = hist_point.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_point AS h WHERE h.id = hist_point.id AND h.version = hist_point.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) <> 0 THEN
	ROUND(
		(SELECT 
			count (id) 
		FROM 
			hist_point 
		WHERE 
			version = 1 AND 
			minor = 0 AND
			(version = (SELECT max(version) FROM hist_point AS h WHERE h.id = hist_point.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_point AS h WHERE h.id = hist_point.id AND h.version = hist_point.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) *100.00/
		(SELECT 
			count (id) 
		FROM 
			hist_point 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_point AS h WHERE h.id = hist_point.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_point AS h WHERE h.id = hist_point.id AND h.version = hist_point.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		)
	, 2)  ELSE 100 END::float AS count_point,
	--
	-- Lines
	--
	-- To prevent a "division by zero" error this CASE WHEN ... THEN is needed
	CASE WHEN 
		(SELECT 
			count (id) 
		FROM 
			hist_line 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) <> 0 THEN
	ROUND(
		(SELECT 
			count (id) 
		FROM 
			hist_line 
		WHERE 
			version = 1 AND 
			minor = 0 AND
			(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) *100.00/
		(SELECT 
			count (id) 
		FROM 
			hist_line 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		)
	, 2)  ELSE 100 END::float AS count_line,
	--
	-- Polygons
	--
	-- To prevent a "division by zero" error this CASE WHEN ... THEN is needed
	CASE WHEN 
		(SELECT 
			count (id) 
		FROM 
			hist_polygon 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND h.version = hist_polygon.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) <> 0 THEN
	ROUND(
		(SELECT 
			count (id) 
		FROM 
			hist_polygon 
		WHERE 
			version = 1 AND 
			minor = 0 AND
			(version = (SELECT max(version) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND h.version = hist_polygon.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		) *100.00/
		(SELECT 
			count (id) 
		FROM 
			hist_polygon 
		WHERE 	visible = 'true' AND
			(version = (SELECT max(version) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))) 
			AND minor = (SELECT max(minor) FROM hist_polygon AS h WHERE h.id = hist_polygon.id AND h.version = hist_polygon.version AND
				(valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
		)
	, 2)  ELSE 100 END::float AS count_polygon
	
FROM generate_series(
	(SELECT date_trunc ('month',(
		SELECT MIN(valid_from) FROM hist_plp)) as foo),  -- Select minimum date (month)
	(SELECT MAX(valid_from) FROM hist_plp)::date,	-- Select maximum date
	interval '1 month') 
;
  """)
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)

#
# Plot (Multiline-Chart)


# Datatypes of the returning data
datatypes = [('date', 'S20'),('col2', 'double'), ('col3', 'double'), ('col4', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col2 = data['col2']
col3 = data['col3']
col4 = data['col4']


# Converts date to a manageable date-format for matplotlib
dates = mdates.num2date(mdates.datestr2num(data['date']))
fig, ax = plt.subplots()

# Create linechart
plt.plot(dates, col2, color = '#2dd700', linewidth=2, label='Points')
plt.plot(dates, col3, color = '#00a287', linewidth=2, label='Lines')
plt.plot(dates, col4, color = '#f5001d', linewidth=2, label='Polygons')

# Forces the plot to start from 0 and end at 100
pylab.ylim([0,100])

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x and y axis
plt.xlabel('Date')
plt.ylabel('Untouched Points, Lines and Polygons [%]')

# place legend
ax.legend(loc='upper right',  prop={'size':12})

# Plot-title
plt.title('Development of untouched Points, Lines and Polygons')

# Save plot to *.jpeg-file
plt.savefig('pics/c6_untouched.jpeg')

plt.clf()