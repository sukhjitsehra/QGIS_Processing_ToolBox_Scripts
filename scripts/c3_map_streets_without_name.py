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
from optparse import OptionParser
import sys, os, subprocess
import cStringIO
import mapnik

#description     :This file creates a map: Maps shows all streets without a name-tag


#author          :Sukhjit Singh Sehra modified the code of Christopher Barron @ http://giscience.uni-hd.de/
#date            :09.10.2016
#version         :1.0
#usage           :This script is designed to work with historic data imported into PostgreSQL database using osm-hisotry-renderer tool, for more information please visit https://github.com/sukhjitsehra/iOSMAnalyzer


db_name = Database
db_user = User
hostname = Host
db_pw = Password

# Path to OSM-XML file (should be provided in the "osm-mapnik-style"-folder providedby Mapnik
path_to_osm_xml = "/usr/share/openstreetmap-carto-common/style.xml"


# Width (in px), Height (in px), Name and Format of the output-picture
pic_output_width = 1200
pic_output_height = 800
pic_output_name = 'pics/c3_map_streets_without_name'
pic_output_format = 'jpeg'


# database-query for overlay-data
db_query = '''(
-- highways by version and the amount of highways without a name or ref
SELECT 
	geom
FROM 
	hist_line 
WHERE 
	-- List of all roads necessary for car-routing (without "other roads")
	(
	((tags->'highway') = 'motorway') OR 
	((tags->'highway') = 'motorway_link') OR
	((tags->'highway') = 'trunk') OR
	((tags->'highway') = 'trunk_link') OR
	((tags->'highway') = 'primary') OR
	((tags->'highway') = 'primary_link') OR
	((tags->'highway') = 'secondary') OR
	((tags->'highway') = 'secodary_link') OR
	((tags->'highway') = 'tertiary') OR
	((tags->'highway') = 'tertiary_link') OR
	((tags->'highway') = 'residential') OR
	((tags->'highway') = 'living_street')
	)
	AND NOT tags ? 'name' 
	AND NOT tags ? 'ref' 
	AND visible = 'true'
	AND (version = (SELECT max(version) FROM hist_line AS h WHERE h.id = hist_line.id AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null))) 
	AND minor = (SELECT max(minor) FROM hist_line AS h WHERE h.id = hist_line.id AND h.version = hist_line.version AND
		(valid_from <= CURRENT_TIMESTAMP AND (valid_to >= CURRENT_TIMESTAMP OR valid_to is null)))
	)
) AS foo'''


# Create views
dsn = ""
dbprefix = "hist"
viewprefix = "hist_view"
hstore = ""
date = 'CURRENT_TIMESTAMP'
viewcolumns = "access,addr:housename,addr:housenumber,addr:interpolation,admin_level,aerialway,aeroway,amenity,area,barrier,bicycle,brand,bridge,boundary,building,construction,covered,culvert,cutting,denomination,disused,embankment,foot,generator:source,harbour,highway,tracktype,capital,ele,historic,horse,intermittent,junction,landuse,layer,leisure,lock,man_made,military,motorcar,name,natural,oneway,operator,population,power,power_source,place,railway,ref,religion,route,service,shop,sport,surface,toll,tourism,tower:type,tunnel,water,waterway,wetland,width,wood"
extracolumns = ""

# Split columns into the osm2pgsql-database-schema for rendering with Mapnik
# This part of the code is taken from Peter Koerner's "OSM-History-Renderer" (https://github.com/MaZderMind/osm-history-renderer/blob/master/renderer/render.py)
columns = viewcolumns.split(',')
if(extracolumns):
    columns += options.extracolumns.split(',')

def create_views(dsn, dbprefix, viewprefix, hstore, columns, date):
    try:
      conn_string="dbname= %s user= %s host= %s password= %s" %(Database, User, Host, Password)
      #print "Connecting to database\n->%s" % (conn_string)
      con = psycopg2.connect(conn_string)
      QMessageBox.critical(None, "About Layer", "Connection to database sucessful")
    except:
      QMessageBox.critical(None, "About Layer", "Connection to database Failed")
    cur = con.cursor()
    columselect = ""
    for column in columns:
        columselect += "tags->'%s' AS \"%s\", " % (column, column)
    
    cur.execute("DELETE FROM geometry_columns WHERE f_table_catalog = '' AND f_table_schema = 'public' AND f_table_name IN ('%s_point', '%s_line', '%s_roads', '%s_polygon');" % (viewprefix, viewprefix, viewprefix, viewprefix))
    
    cur.execute("DROP VIEW IF EXISTS %s_point" % (viewprefix))
    cur.execute("CREATE OR REPLACE VIEW %s_point AS SELECT id AS osm_id, %s geom AS way FROM %s_point WHERE %s BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31');" % (viewprefix, columselect, dbprefix, date))
    cur.execute("INSERT INTO geometry_columns (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, type) VALUES ('', 'public', '%s_point', 'way', 2, 900913, 'POINT');" % (viewprefix))
    
    cur.execute("DROP VIEW IF EXISTS %s_line" % (viewprefix))
    cur.execute("CREATE OR REPLACE VIEW %s_line AS SELECT id AS osm_id, %s z_order, geom AS way FROM %s_line WHERE %s BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31');" % (viewprefix, columselect, dbprefix, date))
    cur.execute("INSERT INTO geometry_columns (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, type) VALUES ('', 'public', '%s_line', 'way', 2, 900913, 'LINESTRING');" % (viewprefix))
    
    cur.execute("DROP VIEW IF EXISTS %s_roads" % (viewprefix))
    cur.execute("CREATE OR REPLACE VIEW %s_roads AS SELECT id AS osm_id, %s z_order, geom AS way FROM %s_line WHERE %s BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31');" % (viewprefix, columselect, dbprefix, date))
    cur.execute("INSERT INTO geometry_columns (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, type) VALUES ('', 'public', '%s_roads', 'way', 2, 900913, 'LINESTRING');" % (viewprefix))
    
    cur.execute("DROP VIEW IF EXISTS %s_polygon" % (viewprefix))
    cur.execute("CREATE OR REPLACE VIEW %s_polygon AS SELECT id AS osm_id, %s z_order, area AS way_area, geom AS way FROM %s_polygon WHERE %s BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31');" % (viewprefix, columselect, dbprefix, date))
    cur.execute("INSERT INTO geometry_columns (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, type) VALUES ('', 'public', '%s_polygon', 'way', 2, 900913, 'POLYGON');" % (viewprefix))
    
    # bbox-extent of database. Global variable for bbox extent
    cur.execute("SELECT ST_XMin(ST_Extent(ST_Transform(geom, 4326))) FROM %s_point;" % (dbprefix))
    global xmin
    xmin = cur.fetchone()[0]
        
    cur.execute("SELECT ST_YMin(ST_Extent(ST_Transform(geom, 4326))) FROM %s_point;" % (dbprefix))
    global ymin
    ymin = cur.fetchone()[0]
    
    cur.execute("SELECT ST_XMax(ST_Extent(ST_Transform(geom, 4326))) FROM %s_point;" % (dbprefix))
    global xmax
    xmax = cur.fetchone()[0]
    
    cur.execute("SELECT ST_YMax(ST_Extent(ST_Transform(geom, 4326))) FROM %s_point;" % (dbprefix))
    global ymax
    ymax = cur.fetchone()[0]
 
    con.commit()
    cur.close()
    con.close()


# Call function to create the views
create_views(dsn, dbprefix, viewprefix, hstore, columns, date)

# Create map with width height
m = mapnik.Map(pic_output_width, pic_output_height)

# Load osm-xml-stylesheet for rendering the views
mapnik.load_map(m, path_to_osm_xml)

# Define projection
prj = mapnik.Projection("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")

# Map bounds. Bound values come from SQL-query
if hasattr(mapnik, 'Box2d'):
    bbox = mapnik.Box2d(xmin,ymin,xmax,ymax)
else:
    bbox = mapnik.Envelope(xmin,ymin,xmax,ymax)

# Project bounds to map projection
e = mapnik.forward_(bbox, prj)

# Zoom map to bounding box
m.zoom_to_box(e)

#START Layer 1


# style object to hold rules
s = mapnik.Style() 

# rule object to hold symbolizers
r = mapnik.Rule() 

# Lines (outlines of polygons and/or simple lines. Line-Color (RGB) line-thickness
line_symbolizer = mapnik.LineSymbolizer()
line_symblizer.fill=mapnik.Color(mapnik.Color('#f5001d'),4)

# add the line_symbolizer to the rule object
r.symbols.append(line_symbolizer) 

# now add the rule(s) to the style
s.rules.append(r) 

# Styles are added to the map
m.append_style('My Style',s) 

# Projection from PostGIS-Layer-Data
lyr = mapnik.Layer('Geometry from PostGIS', '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
QMessageBox.critical(None, "About Layer", "Check point")
# PostGIS-Connection + DB-Query
lyr.datasource = mapnik.PostGIS(host=hostname, user=db_user, password=db_pw, dbname=db_name,table=db_query) 

# Append Style to layer
lyr.styles.append('My Style')


# END Layer 1


# Append overlay-layers to the map
m.layers.append(lyr)


# START scale

# center of the image
label_x = xmin + ((xmax - xmin) / 2)

# bottom of the image
label_y = ymin + ((ymax - ymin) / 30)

# create PointDatasource
pds = mapnik.PointDatasource()

# place scale at the bottom-center of the map
pds.add_point(label_x, label_y, 'Name', "Scale: 1:" + str(m.scale_denominator()))

# create label symbolizers
if mapnik.mapnik_version() >= 800:
    text = mapnik.TextSymbolizer(mapnik.Expression('[Name]'),'DejaVu Sans Bold',12,mapnik.Color('black'))
else:
    text = mapnik.TextSymbolizer('Name','DejaVu Sans Bold',12,mapnik2.Color('black'))

s3 = mapnik2.Style()
r3 = mapnik2.Rule()
r3.symbols.append(text)
s3.rules.append(r3)

lyr3 = mapnik2.Layer('Memory Datasource')
lyr3.datasource = pds
lyr3.styles.append('Style')
m.layers.append(lyr3)
m.append_style('Style',s3)


# END scale



# Render Mapnik-map to png-file
mapnik2.render_to_file(m, pic_output_name, pic_output_format)

m = 0