##[OSM-History]=Group
##Host=String localhost
##Port=Number 5432
##Database=String hist_osm_pb 
##User=String postgres
##Password=String a
##location=folder

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from processing.tools.vector import VectorWriter
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pylab
import os
#description     :This file creates a plot: Number of contributers and their cummulated percentage of contributions. This is calculated for object-creations and -edits ordered (DESC) by contributions


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

# New cursor method for sql
cur = conn.cursor()

# Execute SQL query. For more than one row use three '"'
try:
  cur.execute(""" 
 -- (1) created objects
-- Add up the percentage of created objects of every user beginning with the user with the most edits. Then user with 2nd most, ...
-- Start with first row of the partition (UNBOUNDED PRECEDING) and end with the current row (CURRENT ROW)
--
SELECT user_name, perc_accumul::float FROM 
	(SELECT user_name, 
	created::int, 
	perc_total,
	SUM(perc_total)
	OVER (ORDER BY perc_total DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS perc_accumul
	FROM 
		-- Total amount of created objects per user and the percentage of all created within the database
		(SELECT 
		DISTINCT(user_name) AS user_name,
		COUNT(id) AS created,
		COUNT(id) * 100.0 / (SELECT COUNT(id) FROM hist_plp WHERE version = 1 AND minor = 0) AS perc_total	
		FROM 
			hist_plp
		WHERE
			version = 1 AND minor = 0
		GROUP BY 
			user_name) AS foo
	) AS foo2;
    
  """)

except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")
    
# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)
  

# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col1', 'string'),('col2', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1']
col2 = data['col2']


# New cursor method for sql
cur2 = conn.cursor()

# Execute SQL query. For more than one row use three '"'
try:
  cur2.execute(""" 
  
-- (2) edited objects
-- Add up the percentage of edited objects of every user beginning with the user with the most edits. Then user with 2nd most, ...
-- Start with first row of the partition (UNBOUNDED PRECEDING) and end with the current row (CURRENT ROW)
-- 
SELECT user_name, perc_accumul::float FROM 
	(SELECT user_name, 
	edits, 
	perc_total,
	SUM(perc_total) OVER (ORDER BY perc_total DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS perc_accumul
	FROM 
		-- Total amount of edited objects per user and the percentage of all edits within the database
		(SELECT 
		DISTINCT(user_name) AS user_name,
		COUNT(id) AS edits,
		COUNT(id) * 100.0 / (SELECT COUNT(id) FROM hist_plp WHERE NOT (version = 1 AND minor = 0)) AS perc_total	
		FROM 
			hist_plp
		WHERE
			NOT (version = 1 AND minor = 0)
		GROUP BY 
			user_name) AS foo
	) AS foo2;
  """)
  

except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")
  

# Getting a list of tuples from the database-cursor (cur2)
data_tuples = []
for row in cur2:
    data_tuples.append(row)

# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col3', 'string'),('col4', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col3 = data['col3']
col4 = data['col4']

fig, ax = plt.subplots()

# set figure size
fig.set_size_inches(12,8)


# Plot (Line-Chart)



# Plot Line-Chart
plt.plot(col2, color = '#2dd700', linewidth=2, label = 'Created Features')
plt.plot(col4, color = '#FF6700', linewidth=2, label = 'Feature-Edits')



# START calculate tresholds


cur.execute("""
SELECT count(user_name) FROM 
	(SELECT user_name, 
	edits, 
	perc_total,
	SUM(perc_total) OVER (ORDER BY perc_total DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS perc_accumul
	FROM 
		-- Total amount of edited objects per user and the percentage of all edits within the database
		(SELECT 
		DISTINCT(user_name) AS user_name,
		COUNT(id) AS edits,
		COUNT(id) * 100.0 / (SELECT COUNT(id) FROM hist_plp WHERE NOT (version = 1 AND minor = 0)) AS perc_total	
		FROM 
			hist_plp
		WHERE
			NOT (version = 1 AND minor = 0)
		GROUP BY 
			user_name) AS foo
	) AS foo2
WHERE perc_accumul <= 98
	;
""")
global tresh_edit
tresh_edit = cur.fetchone()[0]


cur.execute("""
SELECT count(user_name) FROM 
	(SELECT user_name, 
	created::int, 
	perc_total,
	SUM(perc_total)
	OVER (ORDER BY perc_total DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS perc_accumul
	FROM 
		-- Total amount of created objects per user and the percentage of all created within the database
		(SELECT 
		DISTINCT(user_name) AS user_name,
		COUNT(id) AS created,
		COUNT(id) * 100.0 / (SELECT COUNT(id) FROM hist_plp WHERE version = 1 AND minor = 0) AS perc_total	
		FROM 
			hist_plp
		WHERE
			version = 1 AND minor = 0
		GROUP BY 
			user_name) AS foo
	) AS foo2
WHERE perc_accumul <= 98
;
""")
global tresh_created
tresh_created = cur.fetchone()[0]


# END calculate tresholds



# draw a default vline at x= that spans the yrange for created features <= 98%
l = plt.axvline(x=tresh_created, linestyle='dashed', color='#2dd700', label = '98% Threshold (Feature-Creations)')

# draw a default hline at y=1 that spans the xrange for feature-edits <= 98%
l = plt.axvline(x=tresh_edit, linestyle='dashed', color = '#FF6700', label = '98% Threshold (Feature-Edits)')


# Title of the pie chart
plt.title('Contributer-Distribution of created OSM-Features and OSM-Feature-Edits')

# Label x and y axis
ax.set_xlabel('Number of Contributers')
ax.set_ylabel('Accumulated Number of created OSM-Features and OSM-Features-Edits [%]')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Legend
plt.legend(loc = 7)

# Save plot to *.jpeg-file
my_file = 'c7_user_created_edited_98.jpeg'
plt.savefig(os.path.join(location, my_file))


plt.clf()
