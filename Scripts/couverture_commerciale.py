from base import *
from fct_qgis import *
from qgis.core import *
from qgis.utils import iface 
from qgis.analysis import QgsGeometryAnalyzer
from qgis.PyQt.QtCore import QVariant
import processing

def couverture_commerciale(GEO_IRIS, POP_IRIS, PAR_IRIS, PAR_COM, COM_IRIS, COM_COM, SAN_IRIS, SAN_COM, TRA_IRIS, TRA_COM, Isochrone10P):
	
	##Traitement bdd
  	sup_lignes(POP_IRIS,5)
	sup_lignes(PAR_IRIS,5)
  	sup_lignes(PAR_COM,5)
	sup_lignes(COM_IRIS,5)
	sup_lignes(COM_COM,5)
  	sup_lignes(SAN_IRIS,5)
	sup_lignes(SAN_COM,5)
	sup_lignes(TRA_IRIS,5)
  	sup_lignes(TRA_COM, 5)
  	keep_col(POP_IRIS, [1,13])
  	merge_col(PAR_IRIS, [22,23,24,37,40,41,42,43])
  	merge_col(PAR_COM, [20,21,22,35,38,39,40,41])
  	merge_col(COM_IRIS, [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40])
  	merge_col(COM_COM, [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38])
  	merge_col(SAN_IRIS, [20])
  	merge_col(SAN_COM, [18])
  	merge_col(TRA_IRIS, [11,14])
  	merge_col(TRA_COM, [9,12])
	
	##importation de la couche IRIS
	iris = iface.addVectorLayer("GEO_IRIS","IRIS","ogr")
	popiris = iface.addVectorLayer("POP_IRIS","POP_IRIS","ogr")
	pariris = iface.addVectorLayer("PAR_IRIS","PAR_IRIS","ogr")
	parcom = iface.addVectorLayer("PAR_COM","PAR_COM","ogr")
	comiris = iface.addVectorLayer("COM_IRIS","COM_IRIS","ogr")
	comcom = iface.addVectorLayer("COM_COM","COM_COM","ogr")
	saniris = iface.addVectorLayer("SAN_IRIS","SAN_IRIS","ogr")
	sancom = iface.addVectorLayer("SAN_COM","SAN_COM","ogr")
	trairis = iface.addVectorLayer("TRA_IRIS","TRA_IRIS","ogr")
	tracom = iface.addVectorLayer("TRA_COM","TRA_COM","ogr")
	
	##Restriction au périmètre 10 min à pieds
	iso10p = iface.addVectorLayer("Isochrone10P", "ISO10P", "ogr")
	iris.removeSelection()
  	processing.runalg('qgis:extractbylocation', iris, iso10p, u'intersects', 0, "iris10p.shp")
  	iris10p = iface.addVectorLayer("iris10p.shp", "IRIS10P", "ogr")
	
	##Jointures
	jointure(iris10p, popiris, dcomiris, field_1)
	jointure(iris10p, pariris, dcomiris, field_1)
	jointure(iris10p, parcom, depcom, field_1)
	jointure(iris10p, comiris, dcomiris, field_1)
	jointure(iris10p, comcom, depcom, field_1)
	jointure(iris10p, saniris, dcomiris, field_1)
	jointure(iris10p, sancom, depcom, field_1)
	jointure(iris10p, trairis, dcomiris, field_1)
	jointure(iris10p, tracom, depcom, field_1)
	
	##Ajout de champs
	iris10p.dataProvider().addAttributes([QgsField("NbCom", QVariant.Int), QgsField("Compteur", QVariant.Int)])
	iris10p.updateFields()
	
	##Remplissage des champs (somme de commerces et 1)
	features = iris10p.getFeatures()
	for feature in features:
		if not feature['POP_IRIS_Field_2] is None:
			if feature['PAR_IRIS_Field_2'] is None:
				iris10p.dataProvider().changeAttributeValues({ feature.id() : { 8 : (feature['PAR_COM_Field_2']+feature['COM_COM_Field_2']+feature['SAN_COM_Field_2']+feature['TRA_COM_Field_2'])/feature['POP_IRIS_Field_2'] } })
			else :
				iris10p.dataProvider().changeAttributeValues({ feature.id() : { 8 : (feature['PAR_IRIS_Field_2']+feature['COM_IRIS_Field_2']+feature['SAN_IRIS_Field_2']+feature['TRA_IRIS_Field_2'])/feature['POP_IRIS_Field_2'] } })
			iris10p.dataProvider().changeAttributeValues({ feature.id() : { 9 : 1 } })
	
	##Exportation du tableau final et calcul de la couverture commerciale moyenne sur la zone
	QgsVectorFileWriter.writeAsVectorFormat(iris10p, r'perim.csv', "utf-8", None, "CSV")
	couv_com = somme_col('iris10p.csv', 8)/somme_col('iris10p.csv', 9)
	
	##Nettoyage
	QgsMapLayerRegistry.instance().removeMapLayers( [iris.id()] )
	QgsMapLayerRegistry.instance().removeMapLayers( [popiris.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [pariris.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [parcom.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [comiris.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [comcom.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [saniris.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [sancom.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [trairis.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [tracom.id()] )
        QgsMapLayerRegistry.instance().removeMapLayers( [iris10p.id()] )		       
			       
			       
	return couv_com
	

        
			       
