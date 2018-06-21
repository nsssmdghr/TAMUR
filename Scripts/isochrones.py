from qgis.core import *
from qgis.utils import iface


def isochrones(GEO_COM):
  
  geo = iface.addVectorLayer("GEO_COM","GEO","ogr")
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 10 min à pieds, puis taper 1 et valider avec Entree.")
  
  iso10p = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso10p, "Isochrone10P.shp", "utf-8", iso10p.crs(), "ESRI Shapefile")
  QgsMapLayerRegistry.instance().removeMapLayers( [iso10p.id()] )
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 10 min en voiture, puis taper 1 et valider avec Entree.")
  
  iso10v = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso10p, "Isochrone10V.shp", "utf-8", iso10v.crs(), "ESRI Shapefile")
  QgsMapLayerRegistry.instance().removeMapLayers( [iso10v.id()] )
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 30 min en voiture, puis taper 1 et valider avec Entree.")
  
  iso30v = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso30v, "Isochrone30V.shp", "utf-8", iso30v.crs(), "ESRI Shapefile")
  QgsMapLayerRegistry.instance().removeMapLayers( [iso30v.id()] )
  
  print("Les isochrones ont bien été créées")
