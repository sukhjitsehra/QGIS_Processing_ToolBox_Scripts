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
from pylab import *
import matplotlib

#description     :This file creates a plot: Calculates the length [km] of all streets without a name. Results are grouped by street category
#author          :Sukhjit Singh Sehra modified the code of Christopher Barron @ http://giscience.uni-hd.de/
#date            :11.10.2016
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
 SELECT(
	SELECT 
		coalesce(SUM
				(ST_Length
					(ST_GeographyFromText
						(ST_AsText 
							(ST_Transform(geom, 4326))
						)
					)
				/1000)
			, 0) AS length_spheroid 
	FROM 
		hist_line 
	WHERE 
		-- List of all roads necessary for car-routing (without "other roads")
		(
		((tags->'highway') = 'motorway') 
		)
		AND NOT tags ? 'name' 
		AND NOT tags ? 'ref' 
		AND visible = 'true'
		AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
		)
) AS motorway,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'motorway_link') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS motorway_link,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'trunk') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS trunk,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'trunk_link') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS trunk_link,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'primary') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS primary,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'primary_link') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS primary_link,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'secondary') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS secondary,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'secondary_link') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS secondary_link,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'tertiary') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS tertiary,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'tertiary_link') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS tertiary_link,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'unclassified') 
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS unclassified,
(SELECT 
	coalesce(SUM
			(ST_Length
				(ST_GeographyFromText
					(ST_AsText 
						(ST_Transform(geom, 4326))
					)
				)
			/1000)
		, 0) AS length_spheroid 
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	( 
	((tags->'highway') = 'residential')
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS residential;
  """)
except:
    QMessageBox.critical(None, "About Layer", "Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)
    

# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('col1', 'double'),('col2', 'double'), ('col3', 'double'), ('col4', 'double'), ('col5', 'double'), ('col6', 'double'), ('col7', 'double'), ('col8', 'double'), ('col9', 'double'), ('col10', 'double'), ('col11', 'double'), ('col12', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1']
col2 = data['col2']
col3 = data['col3']
col4 = data['col4']
col5 = data['col5']
col6 = data['col6']
col7 = data['col7']
col8 = data['col8']
col9 = data['col9']
col10 = data['col10']
col11 = data['col11']
col12 = data['col12']



# Plot (Barchart)


fig, ax = plt.subplots()

val = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12]
pos = arange(len(val))

# Plot Scatterplot
plt.bar(pos,val, color = '#2dd700')

# Manually plot xticks
plt.xticks(pos+0.5, ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential'))

# Title of the pie chart
plt.title('Street Length without Name or Route Number by Street Category')

# Label x and y axis
ax.set_xlabel('Street Category')
ax.set_ylabel('Length [km]')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Set this grid behind the thicks
ax.set_axisbelow(True) 

# Save plot to *.jpeg-file
savefig('pics/c3_streets_without_name.jpeg')

plt.clf()
