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

#description     :This file creates a plot: Calculates the development if the avarage tag-number of all POIs
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
-- Amount of Tags of each POI
SELECT generate_series,
	ROUND(coalesce((SELECT 
		avg(count) 
	FROM
		(SELECT 
			id, 
			count(skeys) 
		FROM 
			(SELECT 
				id, 
				skeys(tags), 
				tags 
			FROM 
				hist_plp h 
			WHERE 
				-- POI-Tags & Keys
				-- POI-Tags & Keys
				(
				-- accomodation & gastronomy
				((tags->'amenity') = 'bar') OR
				((tags->'amenity') = 'bbq') OR
				((tags->'amenity') = 'biergarten') OR
				((tags->'amenity') = 'cafe') OR
				((tags->'amenity') = 'drinking_water') OR
				((tags->'amenity') = 'fast_food') OR
				((tags->'amenity') = 'food_court') OR
				((tags->'amenity') = 'ice_cream') OR
				((tags->'amenity') = 'pub') OR
				((tags->'amenity') = 'restaurant') OR
				
				-- education
				((tags->'amenity') = 'college') OR
				((tags->'amenity') = 'kindergarten') OR
				((tags->'amenity') = 'library') OR
				((tags->'amenity') = 'school') OR
				((tags->'amenity') = 'university') OR
				-- transport
				((tags->'amenity') = 'bicycle_parking') OR
				((tags->'amenity') = 'bicycle_rental') OR
				((tags->'amenity') = 'bus_station') OR
				((tags->'amenity') = 'car_rental') OR
				((tags->'amenity') = 'car_sharing') OR
				((tags->'amenity') = 'car_wash') OR
				((tags->'amenity') = 'ev_charging') OR
				((tags->'amenity') = 'ferry_terminal') OR
				((tags->'amenity') = 'fuel') OR
				((tags->'amenity') = 'grit_bin') OR
				((tags->'amenity') = 'parking') OR
				((tags->'amenity') = 'parking_entrance') OR
				((tags->'amenity') = 'parking_space') OR
				((tags->'amenity') = 'taxi') OR
				-- finances
				((tags->'amenity') = 'atm') OR
				((tags->'amenity') = 'bank') OR
				((tags->'amenity') = 'bureau_de_change') OR
				-- health care
				((tags->'amenity') = 'baby_hatch') OR
				((tags->'amenity') = 'clinic') OR
				((tags->'amenity') = 'dentist') OR
				((tags->'amenity') = 'doctors') OR
				((tags->'amenity') = 'hospital') OR
				((tags->'amenity') = 'nursing_home') OR
				((tags->'amenity') = 'pharmacy') OR
				((tags->'amenity') = 'social_facility') OR
				((tags->'amenity') = 'veterinary') OR
				-- art & cilture
				((tags->'amenity') = 'arts_centre') OR
				((tags->'amenity') = 'cinema') OR
				((tags->'amenity') = 'community_centre') OR
				((tags->'amenity') = 'fountain') OR
				((tags->'amenity') = 'nightclub') OR
				((tags->'amenity') = 'social_centre') OR
				((tags->'amenity') = 'stripclub') OR
				((tags->'amenity') = 'studio') OR
				((tags->'amenity') = 'swingerclub') OR
				((tags->'amenity') = 'theatre') OR
				-- shops
				tags ? 'shop' OR
				-- tourism
				tags ? 'tourism' OR
				
				-- other
				((tags->'amenity') = 'animal_boarding') OR
				((tags->'amenity') = 'animal_shelter') OR
				((tags->'amenity') = 'bench') OR
				((tags->'amenity') = 'brothel') OR
				((tags->'amenity') = 'clock') OR
				((tags->'amenity') = 'courthouse') OR
				((tags->'amenity') = 'crematorium') OR
				((tags->'amenity') = 'crypt') OR
				((tags->'amenity') = 'embassy') OR
				((tags->'amenity') = 'fire_station') OR
				((tags->'amenity') = 'grave_yard') OR
				((tags->'amenity') = 'hunting_stand') OR
				((tags->'amenity') = 'marketplace') OR
				((tags->'amenity') = 'place_of_worship') OR
				((tags->'amenity') = 'police') OR
				((tags->'amenity') = 'post_box') OR
				((tags->'amenity') = 'post_office') OR
				((tags->'amenity') = 'prison') OR
				((tags->'amenity') = 'public_building') OR
				((tags->'amenity') = 'recycling') OR
				((tags->'amenity') = 'sauna') OR
				((tags->'amenity') = 'shelter') OR
				((tags->'amenity') = 'shower') OR
				((tags->'amenity') = 'telephone') OR
				((tags->'amenity') = 'toilets') OR
				((tags->'amenity') = 'townhall') OR
				((tags->'amenity') = 'vending_machine') OR
				((tags->'amenity') = 'waste_basket') OR
				((tags->'amenity') = 'waste_disposal') OR
				((tags->'amenity') = 'watering_place') 
				)
				AND visible = 'true'
				AND
				(version = (SELECT max(version) FROM hist_plp WHERE typ = h.typ AND h.id = hist_plp.id) AND
					( valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))
				AND minor = (SELECT max(minor) from hist_plp where typ = h.typ AND h.id = hist_plp.id AND h.version = hist_plp.version AND
					( valid_from <= generate_series AND (valid_to >= generate_series OR valid_to is null))))
			) AS foo 
		GROUP BY id) AS foo2
	), 0), 2)::float AS avg
	
FROM generate_series(
	(SELECT date_trunc ('month',(
		SELECT MIN(valid_from) FROM hist_plp)) as foo),  -- Select minimum date (month)
	(SELECT MAX(valid_from) FROM hist_plp)::date,	-- Select maximum date
	interval '1 month')
;

  """)

except:
    QMessageBox.critical(None, "About Layer", "First Query could not be executed")

# Getting a list of tuples from the database-cursor (cur)
data_tuples = []
for row in cur:
    data_tuples.append(row)
    
#Plot (Barchart)


# Datatypes of the returning data: column 1(col1) --> integer, column 2(date) --> string
datatypes = [('date', 'S20'), ('col1', 'double')]

# Data-tuple and datatype
data = np.array(data_tuples, dtype=datatypes)

# Date comes from 'col1'
col1 = data['col1']

# Converts date to a manageable date-format for matplotlib
dates = mdates.num2date(mdates.datestr2num(data['date']))
fig, ax1 = plt.subplots()

# Create barchart (x-axis=dates, y-axis=col1, 
ax1.plot(dates, col1,  linewidth=2, color = '#2dd700')

# Place a gray dashed grid behind the thicks (only for y-axis)
ax1.yaxis.grid(color='gray', linestyle='dashed')

# Set this grid behind the thicks
ax1.set_axisbelow(True) 

# Rotate x-labels on the x-axis
fig.autofmt_xdate()

# Label x and y axis
plt.xlabel('Date')
plt.ylabel('Average number of Tags')

# Plot-title
plt.title("Development of the average Tag-Number of all POIs for Punjab OSM")

# Save plot to *.jpeg-file
plt.savefig('pics/c5_poi_tags.jpeg')

plt.clf()