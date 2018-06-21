from base import *
from qgis.core import *
from qgis.utils import iface 
import processing


def accessibilite(Couche_TC, Communes, Emplois_Communes, Isochrone10P, Isochrone30V):
  
  ##Traitement de Emplois_communes, pour ne garder que l'information pertinente
  sup_lignes(Emlois_Communes,5)
  keep_col(Emplois_Communes,[1,39])
  print("Fichiers prets pour le traitement de l'accessibilité")

  ##importation des couches et création des appels
  TC = iface.addVectorLayer("Couche_TC", "TC", "ogr")
  iso10p = iface.addVectorLayer("Isochrone10P", "isochrone10p", "ogr")

  ##création et importation de la couche TC restreinte à l'isochrone
  TC.removeSelection()
  processing.runalg('qgis:extractbylocation', TC, iso10p, u'within', 0, "TC_isochrone10p.shp")
  TCiso10p = iface.addVectorLayer("TC_isochrone10p.shp","TCiso10p","ogr")

  ##comptage des arrêts de bus dans l'isochrone
  it = TCiso10p.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" = bus_stop' )) 
  TCiso10p.setSelectedFeatures( [ f.id() for f in it ] )
  arrets_bus = TCiso10p.selectedFeatureCount()  
  
  ##comptage des points autres qu'arrêts de bus
  it = TCiso10p.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" != bus_stop' )) 
  TCiso10p.setSelectedFeatures( [ f.id() for f in it ] )
  arrets_non_bus = TCiso10p.selectedFeatureCount()
  
  access_tc = arrets_bus + arrets_non_bus
  
  ##ajout des couches commune, emplois et isochrone en voiture 30 min
  communes = iface.addVectorLayer("Communes","COMMUNES","ogr")
  empcom = iface.addVectorLayer("Emplois_Communes","EMPCOM","ogr")
  iso30v = iface.addVectorLayer("Isochrones30V","ISO30V","ogr")
  
  ##jointure entre communes et empcom
  shpField='INSEE'
  csvField='field_1'
  joinObject = QgsVectorJoinInfo()
  joinObject.joinLayerId = empcom.id()
  joinObject.joinFieldName = csvField
  joinObject.targetFieldName = shpField
  joinObject.memoryCache = True
  communes.addJoin(joinObject)
  
  ##selection des communes dans l'isochrone
  communes.removeSelection()
  processing.runalg('qgis:extractbylocation', communes, iso30v, u'within', 0, "Communes_iso30v.shp")
  comiso30v = iface.addVectorLayer("Communes_iso30v.shp","ComIso30v","ogr")
  
  ##exportation du csv de sortie (indicateur = somme de la colonne S)
  QgsVectorFileWriter.writeAsVectorFormat(comiso30v, r'comiso30v.csv', "utf-8", None, "CSV")
  access_vp = somme_col('comiso30v.csv', 19)
  
  
  ##retourner les sorties
  return access_vp, access_tc
  
