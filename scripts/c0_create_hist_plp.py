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

#description     :This file creates a database view containing all points, lines and polygons. This is necessary for querying the whole database
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
  ALTER TABLE hist_point DROP COLUMN IF EXISTS typ CASCADE;
  ALTER TABLE hist_point DROP COLUMN IF EXISTS minor CASCADE;
  ALTER TABLE hist_line DROP COLUMN IF EXISTS typ CASCADE;
  ALTER TABLE hist_polygon DROP COLUMN IF EXISTS typ CASCADE;
 
  ALTER TABLE hist_point ADD COLUMN typ text;
  ALTER TABLE hist_point ADD COLUMN minor int;
  ALTER TABLE hist_line ADD COLUMN typ text;
  ALTER TABLE hist_polygon ADD COLUMN typ text;
  -- Insert feature type into the columns so the UNION in the next step will work
  UPDATE hist_point SET typ = 'point' WHERE typ isnull;
  UPDATE hist_point SET minor = 0 WHERE minor isnull;
  UPDATE hist_line SET typ = 'line' WHERE typ isnull;
  UPDATE hist_polygon SET typ = 'polygon' WHERE typ isnull;
  -- Create a view out of all three tables (points, lines, polygons)
  CREATE VIEW hist_plp AS SELECT * FROM
	  (
	  SELECT id, version, minor, visible, valid_from, valid_to, user_id, user_name, tags, geom, typ FROM hist_point
	  UNION ALL
	  SELECT id, version, minor, visible, valid_from, valid_to, user_id, user_name, tags, geom, typ FROM hist_line
	  UNION ALL
	  SELECT id, version, minor, visible, valid_from, valid_to, user_id, user_name, tags, geom, typ FROM hist_polygon
	  ) AS foo;
   
    CREATE OR REPLACE FUNCTION exec(text) returns text language plpgsql volatile
    AS $f$ 
    BEGIN
      EXECUTE $1;
      RETURN $1;
    END;
    $f$;
    ALTER FUNCTION exec(text) OWNER TO postgres;
  
    SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' ||
	    quote_ident(s.relname) || ' OWNER TO postgres')
    FROM (SELECT nspname, relname
	  FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) 
	WHERE nspname NOT LIKE E'pg\\_%' AND 
	      nspname <> 'information_schema' AND 
	      relkind IN ('r','S','v') ORDER BY relkind = 'S') s;     
         
  """)
 
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")
cur.close()
conn.commit()
conn.close()    


