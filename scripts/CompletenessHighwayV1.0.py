## Sehra=Group
##Host=String localhost
##Port=Number 5432
##Database=String here_routing
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

# import db connection parameters
#import db_conn_para as db

###
### Connect to database with psycopg2. Add arguments from parser to the connection-string
###
try:
  conn_string="dbname= %s user= %s host= %s password= %s" %(Database, User, Host, Password)
  #conn_string="dbname= %s user= %s host= %s password= %s" %(db.g_my_dbname, db.g_my_username, db.g_my_hostname, db.g_my_dbpassword)
  #print "Connecting to database\n->%s" % (conn_string)
      
# Verbindung mit der DB mittels psycopg2 herstellen
  conn = psycopg2.connect(conn_string)
  QMessageBox.critical(None, "About Layer", "Connection to DB Sucessfull")
except:
 QMessageBox.critical(None, "About Layer", "Connection to database Failed")