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
import psycopg2
from pylab import *
import os
#description     :This file creates a plot: Calculates the total amount and percentage of node-contributions by each contributer. Results are grouped by three mappertypes: ""Senior-Mappers", "Junior-Mappers" and "Nonrecurring-Mappers"

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
	-- Senior Mapper
	(SELECT 
		COUNT(user_name) 
	FROM 
		(SELECT 
			user_name, 
			COUNT(user_name) AS edits_absolut
		FROM 
			hist_point 
		WHERE
			visible = 'true'
		GROUP BY 
			user_name
		) as foo1
	WHERE 
		edits_absolut >=1000) AS senior_mappers,
	-- Junior Mapper
	(SELECT 
		COUNT(user_name) 
	FROM 
		(SELECT 
			user_name, 
			COUNT(user_name) AS edits_absolut
		FROM 
			hist_point
		WHERE
			visible = 'true'
		GROUP BY 
			user_name
		) AS foo2 
	WHERE 
		edits_absolut <1000 AND edits_absolut >=10) AS junior_mappers,
	-- Nonrecurring Mapper
	(SELECT 
		COUNT(user_name) 
	FROM 
		(SELECT 
			user_name, 
			COUNT(user_name) AS edits_absolut
		FROM 
			hist_point
		WHERE
			visible = 'true'
		GROUP BY 
			user_name) AS foo3 
	WHERE 
		edits_absolut <10) as Nonrecurring_mappers

;
  """)
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")

# Return the results of the query. Fetchall() =  all rows, fetchone() = first row
records = cur.fetchone()
cur.close()
    
# Get data from query
senior_m = records[0]
junior_m = records[1]
nonrecurring_m = records[2]


# make a square figure and axes
figure(1, figsize=(6,6))
ax = axes([0.2, 0.2, 0.6, 0.6])

# pie-labelling
labels = 'Senior Mappers', 'Junior Mappers', 'Nonrecurring Mappers'

# get db-values as fracs
fracs = [senior_m, junior_m, nonrecurring_m]

# explode values
explode=(0.05, 0.05, 0.05)

# Color in RGB. not shure about the values (counts). Source: http://stackoverflow.com/questions/5133871/how-to-plot-a-pie-of-color-list
data = {(0, 210, 0): 110, (236, 0, 0): 4, (234, 234, 0): 11} # values in hexa: #2DD700 ,#00A287, #FF6700

colors = []
counts = []

for color, count in data.items():
    # matplotlib wants colors as 0.0-1.0 floats, not 0-255 ints
    colors.append([float(x)/255 for x in color])
    counts.append(count)
    
# Percentage (and total values)
def my_autopct(pct):
    total=sum(fracs)
    val=int(pct*total/100.0)
    return '{p:.1f}%  ({v:d})'.format(p=pct,v=val)
    

# The pie chart (DB-values, explode pies, Labels, decimal places, add shadows to pies
pie(fracs, explode=explode, colors=colors, autopct=my_autopct, labels=labels, shadow=True)

# Title of the pie chart
#title('Mappertypes based on their Node-Contribution')

# Save plot to *.jpeg-file
my_file = 'c7_mappertyp.jpeg'
plt.savefig(os.path.join(location, my_file))

plt.clf()