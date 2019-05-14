##Roads_layer=vector
##Speed_field_in_kmh=field Roads_layer
##Starting_points_layer=vector
##Resolution_in_meters_per_pixel=number 50
##Extent=extent
##Ouput_time_raster_in_minutes=output raster
##Style_unit=selection Minutes;Hours
##Style_max_travel_time=number 120
##Multiple_styles_travel_time_intervals=string 5,15,30
#Generate_polygons_isochrones=boolean False


import processing
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import os

"""
#TODO
-comment styliser la sortie chargée automatiquement par le script plutot qu'ajouter une seconde fois la couche ds la TOC
-bug avec grosse extent @ saga raster calc pixel time --> le raster est correctement générer, la légende indique NAN mais
value tool montre des valeur correctes. Impossible d'ouvrir les propriétés (bad alloc) ça doit être pour ça que rcost génére un fichier vide
soit c'est un problème de saga, soit de qgis
-option to choose raster calc engine (saga or gdal_calc) --> pb comment avec gdal_calc assigner une valeur à du nodata?
-compute vector isochrone --> reclass, vectorize and smooth
"""


#Assign parameters to shortest variable name
vrsx = Roads_layer
speedField = Speed_field_in_kmh
startPts = Starting_points_layer
res = Resolution_in_meters_per_pixel
extent = Extent
rcost = Ouput_time_raster_in_minutes
maxTime = Style_max_travel_time
timeIntervals = Multiple_styles_travel_time_intervals


#CHECK if one or more starting pt are in extent
xmin, xmax, ymin, ymax = map(float, Extent.split(','))
extentRect = QgsRectangle (xmin, ymin, xmax, ymax)
vl = processing.getObject(Starting_points_layer)
"""
# Methode 1
within = False
for feat in vl.getFeatures():
	if extentRect.contains(feat.geometry().asPoint()):
		within = True
if not within:
	raise GeoAlgorithmExecutionException('err starting points not in extent')
"""
# Methode 2 : Request feature with spatial filter
request = QgsFeatureRequest()
request.setFilterRect(extentRect)
subsetFeats = list(vl.getFeatures(request))
if len(subsetFeats) == 0:
	raise GeoAlgorithmExecutionException('err starting points not in extent')



#CLIP
progress.setPercentage(0)
extent_vrsx = processing.getObject(vrsx).extent()
extent_vrsx = ','.join(map(str,[extent_vrsx.xMinimum(), extent_vrsx.xMaximum(), extent_vrsx.yMinimum(), extent_vrsx.yMaximum()]))
if extent_vrsx != extent: #revoir cette condition, faire qqchose de + précis
	progress.setText('Clip road layer')
	vclip = None
	options = "" #QGIS >= 2.14 else use "options = None"
	result = processing.runalg('gdalogr:clipvectorsbyextent', vrsx, extent, options, vclip)
	if not result:
		raise GeoAlgorithmExecutionException('err ogr clip')
	else:
		vclip = result["OUTPUT_LAYER"]
else:
	vclip = vrsx
progress.setPercentage(20)


#RASTERIZE
progress.setText('Rasterize road layer')
resUnits = 1 # 0 = Output size in pixels, 1 = Output resolution in map units per pixel
#Attention -9999 considéré nodata uniquement avec int16 et pas uint16
depth = 1 #	0 - Byte, 1 - Int16, 2 - UInt16, 3 - UInt32, 4 - Int32, 5 - Float32, 6 - Float64
noData = -9999
compress = 0 # 0 - NONE, 1 - JPEG, 2 - LZW, 3 - PACKBITS, 4 - DEFLATE
#compression options
jepgCompress = 75
deflateCompress = 6
predictor = 1
#output file options
tiled = False
bigtiff = 3 # 1 - YES, 2 - NO, 3 - IF_NEEDED, 4 - IF_SAFER
tfw = False
extra = ""
#
rrsx = None
#result = processing.runalg("gdalogr:rasterize", vclip, speedField, resUnits, res, res, depth, str(noData), compress, jepgCompress, deflateCompress, predictor, tiled, bigtiff, tfw, rrsx)
#update qgis 2.14
result = processing.runalg("gdalogr:rasterize", vclip, speedField, resUnits, res, res, tfw, depth, str(noData), compress, jepgCompress, deflateCompress, predictor, tiled, bigtiff, extra, rrsx)
#output = None pour temp file, nom de variable de la toobox (ex rrsx si ##rrsx=output raster) ou chemin du fichier de sortie
#runalg renvoie un dictionnaire Python avec pour clés les noms des sorties et pour valeurs leurs chemins.
#Pour connaitre le nom de la sortie (dict key) il faut utiliser alghelp
#ex: processing.alghelp("gdalogr:rasterize") --> OUTPUT <OutputRaster> --> le nom de la sortie est 'OUTPUT'
if not result:#empty dict
	raise GeoAlgorithmExecutionException('err gdal rasterize')
else:
	rrsx = result["OUTPUT"]
	progress.setPercentage(40)


#SET NODATA SPEED
progress.setText('Map algebra -> Assign speed to offroad areas (nodata)')
noDataSpeed = 20 #kmh
mainGrid = rrsx
otherGrids = None
formula = "ifelse(eq(a,"+str(noData)+"),"+str(noDataSpeed)+",a)" # 'a' refers to mainGrid
useNoData = True
depth = 3 #0=bit, 1=uint8, 2=sint8, 3=uint16, 4=sint16, 5=uint32, 6=sint32, 7=float32, 8=float64
rrsx2 = None
result = processing.runalg("saga:rastercalculator", mainGrid, otherGrids, formula, useNoData, depth, rrsx2)
if not result:
	raise GeoAlgorithmExecutionException('err saga raster calc 1')
else:
	rrsx2 = result["RESULT"]
progress.setPercentage(60)


#PIXEL TIME
progress.setText('Map algebra -> Compute pixel time travel')
#temps de parcours d'un pixel en minutes via la calculatrice raster et la formule  (distance * 60) / (vitesse * 1000)
mainGrid = rrsx2
formula = "("+str(res)+"*60)/(a*1000)"
useNoData = False
depth = 7 #0=bit, 1=uint8, 2=sint8, 3=uint16, 4=sint16, 5=uint32, 6=sint32, 7=float32, 8=float64
pixelTime = None
result = processing.runalg("saga:rastercalculator", mainGrid, otherGrids, formula, useNoData, depth, pixelTime)
if not result:
	raise GeoAlgorithmExecutionException('err saga raster calc 2')
else:
	pixelTime = result["RESULT"]
progress.setPercentage(80)


#COST RASTER
progress.setText('Compute cost time travel')
knightMove = False
keepNull = False
grassRes = 0 #default
ogrSnap = -1 #no snap
ogrMinArea = 0.0001
result = processing.runalg("grass7:r.cost.full", pixelTime, startPts, knightMove, keepNull, extent, grassRes, ogrSnap, ogrMinArea, rcost)
if not result or not os.path.isfile(rcost):#result dict can be not empty but there is no file !
	raise GeoAlgorithmExecutionException('err grass rcost')
progress.setPercentage(100)



#STYLE (-->méthodo alternative, charger un fichier de style préparé à l'avance)
progress.setText('Stylizing output raster')
#costLay = processing.getObject(rcost)
costLay = processing.load(rcost)#Attention du coup la couche est chargée 2 fois: une fois ici et une fois par runalg

sm = costLay.styleManager()

timeIntervals = timeIntervals.split(',')
timeIntervals = map(int,timeIntervals)
maxTime = int(maxTime)

if Style_unit == 1:#Hours
	#convertir en minutes
	maxTime=maxTime*60
	timeIntervals=[interval*60 for interval in timeIntervals]

for timeInterval in timeIntervals:

	if Style_unit == 1:#Hours
		styleName = str(timeInterval/60)+" hours"
	else:
		styleName = str(timeInterval)+" minutes"
	sm.addStyleFromLayer(styleName)#Add style by cloning the current one
	sm.setCurrentStyle(styleName)

	values = range(timeInterval, maxTime+timeInterval, timeInterval)
	nbClasses = len(values)

	"""
	# create a new colorramp
	blue = QColor(0,0,255)
	red = QColor(255,0,0)
	green = QColor(0,255,0)
	yellow = QColor(255,255,0)
	stop1 = QgsGradientStop(0.3, green)
	stop2 = QgsGradientStop(0.6, yellow)
	stops = [stop1, stop2]
	discrete = False
	colorRamp = QgsVectorGradientColorRampV2(blue, red, discrete, stops)
	myStyle = QgsStyleV2().defaultStyle()
	myStyle.addColorRamp("Name", colorRamp)
	"""

	#Get existing ramp
	myStyle = QgsStyleV2().defaultStyle()
	defaultColorRampNames = myStyle.colorRampNames()
	ramp = myStyle.colorRamp(defaultColorRampNames[defaultColorRampNames.index('RdYlBu')]) #QgsVectorGradientColorRampV2
	#reverse ramp
	discrete = False
	revStops = []
	for stop in ramp.stops()[::-1]:
		revStops.append(QgsGradientStop(1-stop.offset, stop.color))
	revRamp = QgsVectorGradientColorRampV2(ramp.color2(), ramp.color1(), discrete, revStops)
	#myStyle.addColorRamp("Rev", revRamp)

	#Classify
	step=1/float((nbClasses-1))
	cvals=[i*step for i in range(nbClasses)]#ramp relative color between [0,1] (include 0 and 1)
	classes=[]
	for i in range(nbClasses):
		c = revRamp.color(cvals[i])#.getRgb() #return Qcolor()
		if Style_unit == 1:#Hours
			label = str(values[i]/60)+' hours'
		else:
			label = str(values[i])+' minutes'
		classes.append(QgsColorRampShader.ColorRampItem(values[i], c, label))

	#Apply to raster
	shader = QgsRasterShader()
	colorRamp = QgsColorRampShader()
	colorRamp.setColorRampItemList(classes)
	colorRamp.setColorRampType(QgsColorRampShader.DISCRETE)
	shader.setRasterShaderFunction(colorRamp)
	renderer = QgsSingleBandPseudoColorRenderer(costLay.dataProvider(), costLay.type(), shader)
	costLay.setRenderer(renderer)
	costLay.triggerRepaint()


	"""
	#################################
	if Generate_polygons_isochrones:
		#reclassify
		progress.setText('Reclassify')
		values = range(0, maxTime+timeInterval, timeInterval)
		nbClasses = len(values)
		reclassTable=[]
		for i in range(nbClasses-1):
			lowVal=values[i]
			highVal=values[i+1]
			if Style_unit == 1:#Hours
				newVal=highVal/60
			else:
				newVal=highVal
			reclassTable.append([lowVal,highVal,newVal])

		reclassTableStr= ','.join([str(v) for lines in reclassTable for v in lines])
		reclassMethod=2#Low value <= grid value < high value
		result = processing.runalg("saga:changegridvalues", rcost ,reclassMethod ,reclassTableStr, None)
		if not result:
			raise GeoAlgorithmExecutionException('err saga reclass')
		else:
			output = result["GRID_OUT"]
			#outLay = processing.load(output)
			#Apply style
			#renderer = QgsSingleBandPseudoColorRenderer(outLay.dataProvider(), outLay.type(), shader)
			#outLay.setRenderer(renderer)
			#outLay.triggerRepaint()
		#Polygonize
		progress.setText('Polygonize')
		result = processing.runalg("gdalogr:polygonize", output ,"timeClass", None)
		if not result:
			raise GeoAlgorithmExecutionException('err gdal_polygonize')
		else:
			output = result["OUTPUT"]
			outLay = processing.load(output)
	"""
