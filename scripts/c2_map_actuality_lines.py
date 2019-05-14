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
import mapnik
import psycopg2


#description     :This file creates a map: Actuality of all lines
#author          :Sukhjit Singh Sehra modified the code of Christopher Barron @ http://giscience.uni-hd.de/
#date            :09.10.2016
#version         :1.0
#usage           :This script is designed to work with historic data imported into PostgreSQL database using osm-hisotry-renderer tool, for more information please visit https://github.com/sukhjitsehra/iOSMAnalyzer

# Width (in px), Height (in px), Name and Format of the output-picture
pic_output_width = 800
pic_output_height = 400
pic_output_name = 'pics/c2_map_actuality_lines'
pic_output_format = 'jpeg'


# create a map with a given width and height in pixels
# note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
# the 'map.srs' is the target projection of the map and can be whatever you wish
m = mapnik.Map(pic_output_width,pic_output_height) 

# Background color of the data
m.background = mapnik.Color('White') 
# set background colour to. List of RGB-Colors: http://gucky.uni-muenster.de/cgi-bin/rgbtab

# style object to hold rules
s = mapnik.Style() 
s2 = mapnik.Style() 
s3 = mapnik.Style() 
s4 = mapnik.Style() 

# rule object to hold symbolizers
r = mapnik.Rule() 
r2 = mapnik.Rule() 
r3 = mapnik.Rule() 
r4 = mapnik.Rule() 



# Color of the lines

line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.fill = mapnik.Color('green')
line_symbolizer2 = mapnik.LineSymbolizer()
line_symbolizer2.fill = mapnik.Color('yellow')
line_symbolizer3 = mapnik.LineSymbolizer()
line_symbolizer3.fill = mapnik.Color('orange')
line_symbolizer4 = mapnik.LineSymbolizer()
line_symbolizer4.fill = mapnik.Color('red')


# add the line_symbolizer to the rule object
r.symbols.append(line_symbolizer)
r2.symbols.append(line_symbolizer2)
r3.symbols.append(line_symbolizer3) 
r4.symbols.append(line_symbolizer4) 

# now add the rule(s) to the style and we're done
s.rules.append(r)
s2.rules.append(r2)
s3.rules.append(r3)
s4.rules.append(r4)

# Styles are added to the map
m.append_style('My Style',s) 
m.append_style('My Style2',s2)
m.append_style('My Style3',s3)
m.append_style('My Style4',s4)


# START Layer 1

lyr = mapnik.Layer('Geometry from PostGIS')
# note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

# database-query for overlay-data
db_query = '''(
SELECT geom FROM
	(SELECT 
		geom, 
		-- select latest edit in the whole database as timestamp of the dataset
		extract(days FROM(SELECT max(valid_from) FROM hist_plp) - valid_from) AS age
	FROM 
		hist_line 
	WHERE 
		visible = 'true' AND
		(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))))
	) AS foo
WHERE
	age <= 183 -- less than 6 months
	--age > 183 AND age <= 365 -- older than 6 months and les than 1 year
	--age > 365 AND age <= 730 -- older than 1 year and less than 2 years
	--age > 730 -- older than 2 years
) AS foo'''

lyr.datasource = mapnik.PostGIS(host='localhost',user='postgres',password='a',dbname='hist_osm_pb',table=db_query)

# Append Style to layer
lyr.styles.append('My Style')


# END Layer 1
# START Layer 2


lyr_2 = mapnik.Layer('Geometry from PostGIS')
# note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

# database-query for overlay-data
db_query2 = '''(
SELECT geom FROM
	(SELECT 
		geom, 
		-- select latest edit in the whole database as timestamp of the dataset
		extract(days FROM(SELECT max(valid_from) FROM hist_plp) - valid_from) AS age
	FROM 
		hist_line 
	WHERE 
		visible = 'true' AND
		(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))))
	) AS foo
WHERE
	--age <= 183 -- less than 6 months
	age > 183 AND age <= 365 -- older than 6 months and les than 1 year
	--age > 365 AND age <= 730 -- older than 1 year and less than 2 years
	--age > 730 -- older than 2 years
) AS foo'''


lyr_2.datasource = mapnik.PostGIS(host='localhost',user='postgres',password='a',dbname='hist_osm_pb',table=db_query2)

# Append Style to layer
lyr_2.styles.append('My Style2')

# END Layer 2




# START Layer 3


lyr_3 = mapnik.Layer('Geometry from PostGIS')
# note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

# database-query for overlay-data
db_query3 = '''(
SELECT geom FROM
	(SELECT 
		geom, 
		-- select latest edit in the whole database as timestamp of the dataset
		extract(days FROM(SELECT max(valid_from) FROM hist_plp) - valid_from) AS age
	FROM 
		hist_line 
	WHERE 
		visible = 'true' AND
		(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))))
	) AS foo
WHERE
	--age <= 183 -- less than 6 months
	--age > 183 AND age <= 365 -- older than 6 months and les than 1 year
	age > 365 AND age <= 730 -- older than 1 year and less than 2 years
	--age > 730 -- older than 2 years
) AS foo'''


lyr_3.datasource = mapnik.PostGIS(host='localhost',user='postgres',password='a',dbname='hist_osm_pb',table=db_query3)

# Append Style to layer
lyr_3.styles.append('My Style3')



# END Layer 3




# START Layer 4


lyr_4 = mapnik.Layer('Geometry from PostGIS')
# note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

# database-query for overlay-data
db_query4 = '''(
SELECT geom FROM
	(SELECT 
		geom, 
		-- select latest edit in the whole database as timestamp of the dataset
		extract(days FROM(SELECT max(valid_from) FROM hist_plp) - valid_from) AS age
	FROM 
		hist_line 
	WHERE 
		visible = 'true' AND
		(version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
		AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
			(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))))
	) AS foo
WHERE
	--age <= 183 -- less than 6 months
	--age > 183 AND age <= 365 -- older than 6 months and les than 1 year
	--age > 365 AND age <= 730 -- older than 1 year and less than 2 years
	age > 730 -- older than 2 years
) AS foo'''


lyr_4.datasource = mapnik.PostGIS(host='localhost',user='postgres',password='a',dbname='hist_osm_pb',table=db_query4)

# Append Style to layer
lyr_4.styles.append('My Style4')

#END Layer 4




# Append overlay-layers to the map

m.layers.append(lyr)
m.layers.append(lyr_2)
m.layers.append(lyr_3)
m.layers.append(lyr_4)

# Zoom to all
m.zoom_all()


# Write the map with its overlays to a png image 
mapnik.render_to_file(m,pic_output_name, pic_output_format)

del m
