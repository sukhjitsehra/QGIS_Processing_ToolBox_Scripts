##[Semanctic.Analysis]=group
##layer=vector
##file=output vector

from qgis.core import *
from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsFeature, QgsField, QgsFields
from processing.tools.vector import VectorWriter
from qgis.networkanalysis import (QgsLineVectorLayerDirector,QgsDistanceArcProperter, QgsGraphBuilder,QgsGraphAnalyzer)
from processing.core import GeoAlgorithmExecutionException
from qgis.gui import *
from processing.tools.vector import VectorWriter
from warnings import warn
from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
from SPARQLWrapper import SPARQLWrapper, JSON
vectorLayer = processing.getObject(layer)
provider = vectorLayer.dataProvider()


New_layer= processing.getObject(layer)
fields = QgsFields()
fields = provider.fields()
fields.append(QgsField('ID', QVariant.String,'',254))
fields.append(QgsField('NAME', QVariant.String,'',254))
#fields.append(QgsField('', QVariant.String,'',254))


writer = processing.VectorWriter(file, None, fields.toList(),QGis.WKBLineString, New_layer.crs())

features = processing.features(vectorLayer)

#if vectorLayer.featureCount() != vectorCopyLayer.featureCount():
  #  GeoAlgorithmExecutionException('Number of features in both point layers should be equal!')

progress.setInfo('accessing the vector layer..!')

feats = vectorLayer.getFeatures()
ft = QgsFeature()
#pt = QgsPoint(50,50)
#print "ft is"
#print dir(ft.attrributes())
ft.setFields(fields)

def convertProjection(x,y,from_crs,to_crs):
    crsSrc = QgsCoordinateReferenceSystem(from_crs)
    crsDest = QgsCoordinateReferenceSystem(to_crs)
    xform = QgsCoordinateTransform(crsSrc, crsDest)
    pt = xform.transform(QgsPoint(x,y))
    return pt.x(), pt.y()
idList = []
latitudeList = []
longitudeList = []

if vectorLayer.wkbType()==QGis.WKBPoint:
    print 'Layer is a pojnt layer'
    for f in feats:
        ft['ID'] = f['ID']
        ft['NAME'] = f['NAME']
        # ft['fk_region']=f['fk_region']
        #ft['ELEV']=f['ELEV']
        #ft['USE']=f['USE']
        name = f['name']
        print "name %s"%name
        if  not name:
            id = f['ID']
            idList.append(id)
            geom = f.geometry()
            latitude = round(geom.asPoint().x(),3)
            longitude = round(geom.asPoint().y(),3)
            print latitude,longitude
            latitudeList.append(latitude)
            longitudeList.append(longitude)
            print latitudeList,longitudeList
            print "empty %r"%name
            #ft['NEWNAME'] = y
        writer.addFeature(ft)
        print latitudeList,longitudeList
print '84'
b={}
feats = vectorLayer.getFeatures()
if vectorLayer.wkbType()==QGis.WKBLineString:
    print 'Layer is a line layer'
    for f in feats:
        ft['ID'] = f['osm_id']
        ft['NAME'] = f['NAME']
       # ft['fk_region']=f['fk_region']
        #ft['ELEV']=f['ELEV']
        #ft['USE']=f['USE']
        name = f['NAME']
        print "name %s"%name
        if  not name:
            id = f['osm_id']
            idList.append(id)
            geom = f.geometry()
            print geom
            latitude =geom.asPolyline()
            #longitude = round(geom.asPolyline().y(),3)
            print latitude#,longitude
            latitudeList.append(latitude[0][0])
            longitudeList.append(latitude[0][1])
            print '107'
            print latitudeList,longitudeList
            print "empty %r"%name
            #ft['NEWNAME'] = y
        writer.addFeature(ft)
        print "110"
    #print latitudeList#,longitudeList
#how to convert meters to degrees
#latitude=vectorLayer.getFeatures().geometry().asPoint().x()
#longitude=longitude
print '115'
print latitudeList#,longitudeList
print longitudeList#,longitudeList
print '119'

# Remove the "EPSG:" part

degreeCorx = []
degreeCory = []
c={}
for ix,jx in zip(latitudeList,longitudeList):
    from_crs = vectorLayer.crs()
    to_crs = 4326
    coord = convertProjection(ix,jx,from_crs, to_crs)
    print coord[0]
    print "131  "
    print coord[1]
    degreeCorx.append(coord[0])
    degreeCory.append(coord[1])
    k1=id
    b[k1]=(coord[0],coord[1])
    k2 = (str(coord[0]),str(coord[1]))
    c[k2]="NULL"

print c
print "degree",degreeCorx,degreeCory
#latitude.append(52)
#longitude.append(69)
results = []
for i,j in zip(degreeCorx,degreeCory):
     #   for item in idList:            
       #     coordinate = {item:{'lon'+str(item):i,'lat'+str(item):j}}
         #   print coordinate
            #from_crs = vectorLayer.crs()
            #to_crs = 4326
            #coord = convertProjection(i,j,from_crs, to_crs)
            #print coord[0]
            #print coord[1]
            print '135'
            print i,j
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery("""
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX bif: <bif:>
            select  *
            where{
                        ?place a owl:Thing;
                        foaf:name ?name ;
                        rdfs:label ?label ;
                        geo:geometry ?geo;    
                        geo:lat ?lat ;
                        geo:long ?long.  
                       # FILTER (xsd:float(?lat) = 35)
                        #FILTER (xsd:float(?long) = 47.45)
             #          FILTER(
            #           xsd:float(?lat) - 73 <= 0.05 && 73 - xsd:float(?lat) <= 0.05
            #        && xsd:float(?long) - 19 <= 0.05 && 19 - xsd:float(?long) <= 0.05 && lang(?label) = "en"
            #)
                  FILTER (bif:st_intersects (?geo, bif:st_point("""+str(i)+""","""+str(j)+"""), 2) && lang(?label) = "en")
            }
                    """)
            sparql.setReturnFormat(JSON)
            results.append(sparql.query().convert())
           # print results
            print "end" 
            print i,j
            
#print coord            
lat_results= []
long_results= []
name_results= []
label_results= []
d={}
#print results
for eachresult in results:
    for result in eachresult["results"]["bindings"]:
        #key = ("longitude","latitude","name")
        #value = [result["long"]["value"],result["lat"]["value"],result["label"]["value"]]
        name_results.append(result["name"]["value"])
        label_results.append(result["label"]["value"])
        lat_results.append(result["lat"]["value"])
        long_results.append(result["long"]["value"])
        d1=str(result["long"]["value"])
        d2=str(result["lat"]["value"])
        key=(d1, d2)
        #d ={}
        #d[key]=value
        d[key]=str(result["label"]["value"])
        for key in d:
            if k2 in c:
                print c[k2]
                c[k2]=str(result["label"]["value"])
                print c[k2]
        print i,j        
        print "Place results:",name_results
        print "Label results:",label_results
        print "Latitude results:",lat_results
        print "Longitude results:",long_results
        print d 
        #y1 = label_results[0]
        #y2 = label_results[1]
        #y3 = label_results[2]
        #print y

feat = vectorLayer.getFeatures()
print feat   
a={}
l = []
for word in d:
    l.append(d[word])
    print l
    
#for var in l:
 #   print var
my_dict=[]
for g in feat:
    my_id = g['osm_id']
    name=g['NAME']
    for saved_id,n in zip(idList,l):
        if saved_id == my_id:
            print saved_id
            print n
            vectorLayer.startEditing()
            index = vectorLayer.fieldNameIndex("NAME")
            g.setAttribute(index,n)
            vectorLayer.updateFeature(g)
            vectorLayer.commitChanges()                            
print my_dict
feat = vectorLayer.getFeatures()
for g in feat:
    for m in my_dict:
        print m
        vectorLayer.startEditing()
        index = vectorLayer.fieldNameIndex("NAME")
        if saved_id == my_id:
            g.setAttribute(index,m)
        vectorLayer.updateFeature(g)
            #Call commit to save the changes
        vectorLayer.commitChanges()                            


'''
for g in feat:
    vars = [v  for v in l]
    AddId = g['osm_id']
    print AddId
    #print var,vars
    print "a"
    #print dir(file)
    vectorLayer.startEditing()
    index = vectorLayer.fieldNameIndex("NAME")
    for item in idList:
        if AddId == item:
            g.setAttribute(index,vars)
            print vars
            #break
            #vector.changeAttributeValue(g.id(), index,vars )
            vectorLayer.updateFeature(g)
            #Call commit to save the changes
            vectorLayer.commitChanges()                            
            #p  rint ft['NAME']
                    


        
s = set(a)
print s
t = set(d)
print t
#if key1 == key:
#for n in s.intersection(t):
print '254'
#print n,d[n]
print '252'
    #   a[key1]=d[key]
    #  print AddId
    #  print "a"
#for key in c.viewkeys() & d.viewkeys():
#    if c[key] == d[key]:
        vectorLayer.startEditing()
        index = vectorLayer.fieldNameIndex("NAME")
        g.setAttribute(index,d[key])
        vectorLayer.updateFeature(g)
        #Call commit to save the changes
        vectorLayer.commitChanges()                            
        #print ft['NAME'] 
'''
del writer

