##Demander à l'utilisateur de suivre le mode d'emploi pour créer les isochrones


##importation des couches et création des appels
isochrone = iface.addVectorLayer("gis_osm_transport_free_1.shp", "TC", "ogr")
TC = iface.addVectorLayer("Isochrone.shp", "isochrone", "ogr")

##création et importation de la couche TC restreinte à l'isochrone
import processing
isochrone.removeSelection()
processing.runalg('qgis:extractbylocation', TC, isochrone, u'within', 0, "TC dans isochrone.shp")
TCiso = iface.addVectorLayer("TC dans isochrone.shp","TCiso","ogr")

##comptage des arrêts de bus dans l'isochrone
it = TCiso.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" = bus_stop' )) 
TCiso.setSelectedFeatures( [ f.id() for f in it ] )
TCiso.selectedFeatureCount()

##Demander à l'utilisateur d'entrer manuellement le compte dans le tableaur résultat (?)

##comptage des points autres qu'arrêts de bus
it = TCiso.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" != bus_stop' )) 
TCiso.setSelectedFeatures( [ f.id() for f in it ] )
TCiso.selectedFeatureCount()

##Demander à l'utilisateur d'entrer manuellement le compte dans le tableaur résultat (?)