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
import os
from processing.tools.vector import VectorWriter
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pylab
#description     :This file creates a plot: For identiyfing number of distinct users per feature with last edit month

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
 -- In which year/month last edit made to a feature and how many users edited it
SELECT 
		max(version)::int,max(date_trunc('month', valid_from)::date)
                         from hist_line group by id
;
  """)
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)

    
# Plot (linechart)


# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col1', 'i4'),('date', 'S20')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

#
col1 = data['col1']


# Converts date to a manageable date-format for matplotlib
dates = mdates.num2date(mdates.datestr2num(data['date']))
fig, ax1 = plt.subplots()

# Create barchart (x-axis=dates, y-axis=col1, 
ax1.bar(dates, col1,  width=15, align='center', color = '#AA6C39')
#plt.plot(dates, col1,'r--', dates, col2,'g^' )
# Place a gray dashed grid behind the thicks (only for y-axis)
#ax1.axis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax1.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x- and y-axis
plt.xlabel('Date of latest edit')
plt.ylabel('Number of lastest avaliable version of edited a feature')

# Plot-title
#plt.title("Development of Users with their first Contribution")

# Save plot to *.jpeg-file
my_file = 'c7maxversionPerFeature.png'
plt.savefig(os.path.join(location, my_file))
plt.clf()