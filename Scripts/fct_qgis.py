from qgis.core import *


def add_shp_layer(layer_path,layer_name):
	layer = iface.addVectorLayer(layer_path,layer_name,"ogr")

	if not layer.isValid():
		print("Erreur: couche non chargée")

def add_csv_layer(layer_path,layer_name):
	layer = iface.addVectorLayer(layer_path,layer_name,"delimitedtext")

	if not layer.isValid():
		print("Erreur: couche non chargée")

def select_by_field_value(layer_name,field_name,value):
	layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(layer)
    it = layer.getFeatures(QgsFeatureRequest().setFilterExpression (u'{0} = {1}'.format(field_name,value))) #mettre simplement le code en chiffres
    layer.setSelectedFeatures( [ f.id() for f in it ] )

