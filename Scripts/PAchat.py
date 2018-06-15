iris = iface.addVectorLayer(".\PAchat\IRIS.shp","IRIS","ogr")
communes = iface.addVectorLayer(".\PAchat\COMMUNES.csv","COMMUNES","ogr")
reviris = iface.addVectorLayer(".\PAchat\REV_IRIS.csv","REV_IRIS","ogr")
popiris = iface.addVectorLayer(".\PAchat\POP_IRIS.csv","POP_IRIS","ogr")

num = 955980101
it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = {0}'.format(num) ))
iris.setSelectedFeatures( [ f.id() for f in it ] )

from qgis.utils import iface 
from qgis.analysis import QgsGeometryAnalyzer 
import processing

QgsGeometryAnalyzer().buffer(iris, ".\PAchat\Buffer.shp",10000, True, False, -1)
buffer = iface.addVectorLayer(".\PAchat\Buffer.shp","Buffer","ogr")

iris.removeSelection()

processing.runalg('qgis:extractbylocation', iris, buffer, u'within', 0, ".\PAchat\Perim.shp")
perim = iface.addVectorLayer(".\PAchat\Perim.shp","Perim","ogr")

perimField='depcom'
communesField='field_1'
joinObject = QgsVectorJoinInfo()
joinObject.joinLayerId = communes.id()
joinObject.joinFieldName = communesField
joinObject.targetFieldName = perimField
joinObject.memoryCache = True
perim.addJoin(joinObject)

perimField='dcomiris'
popirisField='field_1'
joinObject = QgsVectorJoinInfo()
joinObject.joinLayerId = popiris.id()
joinObject.joinFieldName = popirisField
joinObject.targetFieldName = perimField
joinObject.memoryCache = True
perim.addJoin(joinObject)

perimField='dcomiris'
revirisField='field_1'
joinObject = QgsVectorJoinInfo()
joinObject.joinLayerId = reviris.id()
joinObject.joinFieldName = revirisField
joinObject.targetFieldName = perimField
joinObject.memoryCache = True
perim.addJoin(joinObject)

from qgis.PyQt.QtCore import QVariant
perim.dataProvider().addAttributes([QgsField("P_Achat", QVariant.Int), QgsField("Distance", QVariant.Int),QgsField("Potentiel", QVariant.Int)])
perim.updateFields()

it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = {0}'.format(num) ))
for feature in it:
	centro = feature.geometry().centroid()

n=2

distance = QgsDistanceArea()

features = perim.getFeatures()
for feature in features:
	if not feature['COMMUNES_Field_2'] is None:
		if feature['REV_IRIS_Field_2'] is None:
			perim.dataProvider().changeAttributeValues({ feature.id() : { 8 : feature['COMMUNES_Field_3']*(feature['POP_IRIS_Field_2']-0.4*feature['POP_IRIS_Field_3']) } })
		else: 
			perim.dataProvider().changeAttributeValues({ feature.id() : { 8 : feature['REV_IRIS_Field_2']*(feature['POP_IRIS_Field_2']-0.4*feature['POP_IRIS_Field_3']) } })		
	
	centest = feature.geometry().centroid()
	perim.dataProvider().changeAttributeValues({ feature.id() : { 9 : distance.measureLine(centro.asPoint(), centest.asPoint()) } })
	
features = perim.getFeatures()
for feature in features:
	if not feature['COMMUNES_Field_2'] is None:
		perim.dataProvider().changeAttributeValues({ feature.id() : { 10 : feature['P_Achat']/(feature['Distance']+500)^n } })

QgsVectorFileWriter.writeAsVectorFormat(perim, r'.\PAchat\Perim.csv', "utf-8", None, "CSV")

