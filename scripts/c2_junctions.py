#Donot delete or over write some chagnes has been done first two queries 

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
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

# The unicode has been added to handle the multi-language name of users 
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pylab
#description     :This file creates a plot: Calculate the distance and angle between all identical junctions from tho timestamps (timestamp and 31.12.2010)	Therefore, this script extracts the second last DB-entry of each highway (for comnparison with the currently valid entry) and inserts it to an initialy created database.


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
# the field location has been changed wrt to iosmanalyzer repository as while inserting from hist_line the rd_ inter_2nd was creating error  
cur.execute(""" 
 DROP TABLE IF EXISTS rd_inter_2nd;
CREATE TABLE rd_inter_2nd
(
  id bigint,
  version smallint,
  minor smallint,
  visible boolean,
  user_id bigint,
  user_name text,
  valid_from timestamp without time zone,
  valid_to timestamp without time zone,
  tags hstore,
  z_order integer,
  geom geometry,
  typ text
)
WITH (
  OIDS=FALSE
);
  """)
conn.commit()

# Grab all OSM ids
cur.execute(" SELECT id FROM hist_line GROUP BY id ;")
osm_id = cur.fetchall()

# for each id, select the row with the second last entry of a osm highway feature. 
# This commande inserts all rows except of the currently valid version of the feature to the previously created database

# This has been executed

for idnr in osm_id:
    cur.execute("""INSERT INTO rd_inter_2nd SELECT * FROM (SELECT FROM hist_line WHERE visible = 'true' AND tags ? 'highway'  AND id =%s  ORDER BY valid_from DESC OFFSET 1 LIMIT 1) AS foo;""",(str(idnr[0]),))


conn.commit()

#working on it first table was sucessfully created, issue with second table 
# kreuzungen means crossing, doppelt means double
# kreuzungen_doppelt_2011 runs to infinit loops while execution 
# Needs thorough stepwise execution of the queries before complete run of the program 
# the 



# Execute SQL query. For more than one row use three '"'
try:
  cur.execute("""   
DROP TABLE IF EXISTS kreuzungen_doppelt_today;
     CREATE TABLE kreuzungen_doppelt_today AS SELECT ST_Intersection(a.geom, b.geom) AS geom, a.street_name AS street_a, b.street_name AS street_b
    FROM  (SELECT street_name, (ST_LineMerge(ST_Collect(geom))) AS geom  FROM    (SELECT id, version, minor, valid_from, valid_to, tags -> 'name' AS street_name, geom FROM hist_line WHERE 
 version = (SELECT max(version) from hist_line as h where h.id = hist_line.id AND  ( valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) AND minor = (SELECT max(minor) from hist_line as h where h.id = hist_line.id AND h.version = hist_line.version AND 
 (valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) AND tags ? 'highway') AS foo
GROUP BY COALESCE(street_name), street_name ORDER By street_name DESC) AS a,  (SELECT street_name, (ST_LineMerge(ST_Collect(geom))) AS geom 
FROM   (SELECT id, version, minor, valid_from, valid_to, tags -> 'name' AS street_name, geom FROM hist_line   WHERE 
  version = (SELECT max(version) from hist_line as h where h.id = hist_line.id AND
   ( valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
   AND minor = (SELECT max(minor) from hist_line as h where h.id = hist_line.id AND h.version = hist_line.version AND
   (valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
   AND tags ? 'highway') AS foo
   GROUP BY COALESCE(street_name), street_name ORDER By street_name DESC) AS b
    WHERE
 (ST_Crosses(a.geom, b.geom) OR ST_Touches(a.geom, b.geom)) AND a.street_name <> '' AND b.street_name <> ''
    GROUP BY
  ST_Intersection(a.geom, b.geom), a.street_name, b.street_name ;
ALTER TABLE kreuzungen_doppelt_today ADD COLUMN pky serial NOT NULL PRIMARY KEY;
CREATE INDEX idx_kreuzungen_doppelt_today_geom ON kreuzungen_doppelt_today USING gist (geom);




 --
-- Find the road-intersections of the 2010-12-31 where lines touch or intersect each other. Only choose roads with a name-tag. 
-- The names of both roads is choosen as a road-intersection identifier.
-- There are duplicate road-intersections in this table (e.g. Kleiststr. - Schubertstr. & Schubertstr. - Kleiststr.)
  --
    DROP TABLE IF EXISTS kreuzungen_doppelt_2011;
    CREATE TABLE kreuzungen_doppelt_2011 AS SELECT      
	    ST_Intersection(a.geom, b.geom) as geom, a.street_name AS street_a, b.street_name AS street_b
    FROM
	    (SELECT street_name, (ST_LineMerge(ST_Collect(geom))) AS geom 
	    FROM 
		    (SELECT id, version, valid_from, valid_to, minor, tags -> 'name' AS street_name, geom FROM rd_inter_2nd) AS foo2
	    GROUP BY COALESCE(street_name), street_name ORDER BY street_name DESC) AS a,
	    (SELECT street_name, (ST_LineMerge(ST_Collect(geom))) AS geom 
	    FROM 
		    (SELECT id, version, valid_from, valid_to, minor, tags -> 'name' AS street_name, geom FROM rd_inter_2nd) AS foo2
	    GROUP BY COALESCE(street_name), street_name ORDER BY street_name DESC) AS b
    WHERE
	    (ST_Crosses(a.geom, b.geom) OR ST_Touches(a.geom, b.geom)) AND a.street_name <> '' AND b.street_name <> ''
    GROUP BY
	    ST_Intersection(a.geom, b.geom), a.street_name, b.street_name
    ;
    ALTER TABLE kreuzungen_doppelt_2011 ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_kreuzungen_doppelt_2011_geom ON kreuzungen_doppelt_2011 USING gist (geom);


    --
    -- Delete duplicates from current timestamp (e.g. Kleiststr. - Schubertstr. & Schubertstr. - Kleiststr.) because only non-recurring intersections are choosen
    --
    DROP TABLE IF EXISTS kreuzungen_today;
    CREATE TABLE kreuzungen_today AS SELECT geom, street_a, street_b
    FROM
	    kreuzungen_doppelt_today
    WHERE
	    pky NOT IN
	    (SELECT MAX(dup.pky) FROM kreuzungen_doppelt_today AS dup GROUP BY dup.geom)
    ;
    ALTER TABLE kreuzungen_today ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_kreuzungen_today_geom ON kreuzungen_today USING gist (geom);



    --
    -- Delete duplicates from 2010-12-31 (e.g. Kleiststr. - Schubertstr. & Schubertstr. - Kleiststr.) because only non-recurring intersections are choosen
    --
    DROP TABLE IF EXISTS kreuzungen_2011;
    CREATE TABLE kreuzungen_2011 AS SELECT geom, street_a, street_b
    FROM 	
	    kreuzungen_doppelt_2011
    WHERE 	
	    pky NOT IN
	    (SELECT MAX(dup.pky) FROM kreuzungen_doppelt_2011 AS dup GROUP BY dup.geom)
    ;
    ALTER TABLE kreuzungen_2011 ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_kreuzungen_2011_geom ON kreuzungen_2011 USING gist (geom);



    --
    -- For further calculations: create points out of multipoints 
    --
    DROP TABLE IF EXISTS kreuzungen_2011_dump;
    CREATE TABLE kreuzungen_2011_dump AS SELECT (ST_Dump(geom)).geom AS geom, street_a, street_b, street_a ||', '|| street_b AS street_a_b
    FROM 
	    kreuzungen_doppelt_2011 
    GROUP BY 
	    geom, street_a, street_b 
    HAVING COUNT(street_b) >= 1;
    ALTER TABLE kreuzungen_2011_dump ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_kreuzungen_2011_dump_geom ON kreuzungen_2011_dump USING gist (geom);



    --
    -- For further calculations: create points out of multipoints 
    --
    DROP TABLE IF EXISTS kreuzungen_today_dump;
    CREATE TABLE kreuzungen_today_dump AS SELECT (ST_Dump(geom)).geom AS geom, street_a, street_b, street_a ||', '|| street_b AS street_a_b
    FROM 
	    kreuzungen_today 
    GROUP BY 
	    geom, street_a, street_b 
    HAVING COUNT(street_b) >= 1;
    ALTER TABLE kreuzungen_today_dump ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_kreuzungen_today_dump_geom ON kreuzungen_today_dump USING gist (geom);



    --
    -- Create a new Table with duplicates ...
    --
    DROP TABLE IF EXISTS doppelte_2011;
    CREATE TABLE doppelte_2011 AS SELECT street_a, street_b, street_a_b 
    FROM 
	    kreuzungen_2011_dump AS k 
    GROUP BY 
	    k.street_a, k.street_b, k.street_a_b 
    HAVING COUNT (street_a_b)>1;
    DROP TABLE IF EXISTS doppelte_today;
    CREATE TABLE doppelte_today AS SELECT street_a, street_b, street_a_b 
    FROM 
	    kreuzungen_today_dump AS k 
    GROUP BY 
	    k.street_a, k.street_b, k.street_a_b 
    HAVING COUNT (street_a_b)>1;



    --
    -- ... and remove them from the points
    --
    DELETE FROM kreuzungen_2011_dump WHERE street_a_b IN (SELECT street_a_b FROM doppelte_2011);
    DELETE FROM kreuzungen_today_dump WHERE street_a_b IN (SELECT street_a_b FROM doppelte_today);
    --
    -- Delete the old pky and create a new one
    --
    ALTER TABLE kreuzungen_2011_dump DROP COLUMN pky;
    ALTER TABLE kreuzungen_today_dump DROP COLUMN pky;
    ALTER TABLE kreuzungen_2011_dump ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    ALTER TABLE kreuzungen_today_dump ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    --
    -- 
    --



    DROP TABLE IF EXISTS street_x_y_2012;
    CREATE TABLE street_x_y_2012 AS SELECT
	    t1.geom AS geom_2011,
	    t1.street_a AS street_a_2011,
	    t1.street_b AS street_b_2011,
	    t2.geom AS geom_2012,
	    t2.street_a AS street_a_2012,
	    t2.street_b AS street_b_2012,
	    ST_Distance(T1.geom, T2.geom)
    FROM 
	    kreuzungen_2011_dump T1 
	    JOIN 
	    kreuzungen_today_dump T2 
    ON T1.street_a_b = T2.street_a_b;
    --
    -- Delete roads which intersect more than once with an other one
    -- Therefore only distinct road-intersections remain
    --
    DELETE FROM street_x_y_2012 a                  
    WHERE  1 < (SELECT count(*) FROM street_x_y_2012 b WHERE a.street_a_2011 = b.street_a_2011);
    DELETE FROM street_x_y_2012 a                  
    WHERE 1 < (SELECT count(*) FROM street_x_y_2012 b WHERE a.street_b_2011 = b.street_b_2011);  
    ALTER TABLE street_x_y_2012 ADD COLUMN pky serial NOT NULL PRIMARY KEY;
    CREATE INDEX idx_street_x_y_2012_geom ON street_x_y_2012 USING gist (st_distance);
    



    --
    -- Create or replace function for altering all tables to the same user
    --
    CREATE OR REPLACE FUNCTION exec(text) returns text language plpgsql volatile
    AS $f$ 
    BEGIN
      EXECUTE $1;
      RETURN $1;
    END;
    $f$;
    ALTER FUNCTION exec(text) OWNER TO hiwi1102;
    -- Run function
    SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' ||
	    quote_ident(s.relname) || ' OWNER TO hiwi1102')
    FROM (SELECT nspname, relname
	  FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) 
	WHERE nspname NOT LIKE E'pg\\_%' AND 
	      nspname <> 'information_schema' AND 
	      relkind IN ('r','S','v') ORDER BY relkind = 'S') s; 




    -- Select the distinct road-intersections and their distance between each other
    -- degrees is ST_Azimuth function and calculates the angle between the same junctions
    -- ALSO Table with
    
    SELECT st_distance, degrees(ST_Azimuth(geom2011, geom2012)) FROM (
	    SELECT T2.geom_2011 AS geom2011, T1.geom_2012 AS geom2012, T2.st_distance, T2.count 
	    FROM 
		    (SELECT geom_2012, st_distance
		    FROM street_x_y_2012
		    ) AS T1 
	    JOIN 
		    (SELECT geom_2011, st_distance, count(*)
		    FROM street_x_y_2012
		    GROUP by  geom_2011, st_distance) AS T2
	    
    ON T1.st_distance = T2.st_distance) AS foo
    WHERE st_distance <> '0' order by st_distance;
  """)


  
except: 
    QMessageBox.critical(None, "About Layer", "Could not last execute query")
  
# Getting a list of tuples from the database-cursor (cur)
conn.commit()
data_tuples = []
for row in cur:
    data_tuples.append(row)

# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col1', 'double'),('col2', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1'] # Distance between two junctions
col2 = data['col2'] # Degree of Distance


# Plot (Scatter-Plot)


ax = subplot(111, polar=True)

# Scatterplot: degree in Polar-Scatter (degree between different junctions), y-axis in Scatter (length betweeen different junctions), color, size of circles, color-map:
c = scatter(col2, col1, c=col1, s=100, cmap=cm.hsv)

# Set Opacity of circles
c.set_alpha(0.75)

# Plot-title
plt.title("Directional Scatterplot of Degree and Distance [m] between two Junctions")

# Save plot to *.png-file
plt.savefig('pics/c2_junctions.jpeg')

plt.clf()


    
