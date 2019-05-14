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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pylab
import os
#description     :his file creates a plot: Calculates the development of active distinct contributers per month
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
 -- How many distinct Users have been activ in the area per month/year
SELECT count(DISTINCT t.user_id)::int AS count
      ,date_trunc('month', s.day)::date AS month --http://ben.goodacre.name/tech/Group_by_day,_week_or_month_%28PostgreSQL%29
      
FROM  (
   SELECT generate_series(min(valid_from)::date
                         ,max(valid_from)::date
                         ,interval '1 day'
          )::date AS day
   FROM   hist_point t
   ) s
LEFT   JOIN hist_point t ON t.valid_from::date = s.day
GROUP  BY month
ORDER  BY month
;
  """)
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)

    
datatypes = [('col1', 'i4'), ('date', 'S20')]
data1 = np.array(data_tuples, dtype=datatypes)
col1_1 = data1['col1']


# Plot (Line-Chart)


# Create Subplot
fig = plt.figure()
ax = fig.add_subplot(111)

# Data-tuple and datatype
data1 = np.array(data_tuples, dtype=datatypes)

# Converts date to a manageable date-format for matplotlib
dates = mdates.num2date(mdates.datestr2num(data1['date']))

# Create barchart (x-axis=dates, y-axis=col1, 
plt.plot(dates, col1_1,  color = '#2dd700', linewidth=2, label='created nodes')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x and y axis
plt.xlabel('Date')
plt.ylabel('Number of distinct Contributors')

# Plot-title
#plt.title("Development of distinct Contributors per Month")

# Save plot to *.jpeg-file
my_file = 'c7_distinct_users.jpeg'
plt.savefig(os.path.join(location, my_file))


plt.clf()