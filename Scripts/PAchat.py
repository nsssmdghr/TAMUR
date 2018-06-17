def pouvoir_achat(Geographie_IRIS, Donnees_Communes, Revenus_IRIS, Population_IRIS):
	
	#Importation des couche et création des appels
	iris = iface.addVectorLayer(".\Couches\Geographie_IRIS","IRIS","ogr")
	communes = iface.addVectorLayer(".\Couches\Donnees_Communes","COMMUNES","ogr")
	reviris = iface.addVectorLayer(".\Couches\Revenus_IRIS","REV_IRIS","ogr")
	popiris = iface.addVectorLayer(".\Couches\Population_IRIS","POP_IRIS","ogr")

	#Sélection de l'IRIS à étudier
	num = num_iris
	it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = {0}'.format(num) ))
	iris.setSelectedFeatures( [ f.id() for f in it ] )

	#Création du périmètre de 10km
	from qgis.utils import iface 
	from qgis.analysis import QgsGeometryAnalyzer 
	import processing

	QgsGeometryAnalyzer().buffer(iris, ".\Couches\Buffer.shp",10000, True, False, -1)
	buffer = iface.addVectorLayer(".\Couches\Buffer.shp","Buffer","ogr")

	#Création d'une couche restreinte au périmètre de 10km
	iris.removeSelection()

	processing.runalg('qgis:extractbylocation', iris, buffer, u'within', 0, ".\Couches\Perim.shp")
	perim = iface.addVectorLayer(".\Couches\Perim.shp","Perim","ogr")

	#Jointures des différentes bases de données à la couche géographique
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

	#Création de nouvelles colonnes (pouvoir d'achat, distance et potentiel de chaque IRIS)
	from qgis.PyQt.QtCore import QVariant
	perim.dataProvider().addAttributes([QgsField("P_Achat", QVariant.Int), QgsField("Distance", QVariant.Int),QgsField("Potentiel", QVariant.Int)])
	perim.updateFields()

	#Remplissage des nouvelles colonnes
	#Création d'un appel pour le centroïde de l'IRIS étudié
	it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = {0}'.format(num) ))
	for feature in it:
		centro = feature.geometry().centroid()

	n=friction_deplacement

	#Remplissage des colonnes pouvoir d'achat (numéro 8) et distance (numéro 9)
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

	#Remplissage de la colonne potentiel (numéro 10)
	features = perim.getFeatures()
	for feature in features:
		if not feature['COMMUNES_Field_2'] is None:
			perim.dataProvider().changeAttributeValues({ feature.id() : { 10 : feature['P_Achat']/(feature['Distance']+200)^n } })

	#Exportation des données des IRIS du périmètre dans un CSV
	QgsVectorFileWriter.writeAsVectorFormat(perim, r'.\Couches\Perim.csv', "utf-8", None, "CSV")

