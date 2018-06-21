from qgis.core import *
from qgis.utils import iface 
from qgis.core import QgsVectorFileWriter


def isochrones(GEO_COM):
  
  geo = iface.addVectorLayer("GEO_COM","GEO","ogr")
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 10 min à pieds, puis taper 1 et valider avec Entree.")
  
  iso10p = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso10p, "Isochrone10P.shp", "utf-8", iso.crs(), "ESRI Shapefile")
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 10 min en voiture, puis taper 1 et valider avec Entree.")
  
  iso10v = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso10p, "Isochrone10V.shp", "utf-8", iso.crs(), "ESRI Shapefile")
  
  flag = 0
    while flag != 1:
      flag = raw_input("Veuillez suivre le mode d'emploi pour créer une isochrone de 30 min en voiture, puis taper 1 et valider avec Entree.")
  
  iso10p = iface.activeLayer()
  QgsVectorFileWriter.writeAsVectorFormat(iso30v, "Isochrone30V.shp", "utf-8", iso.crs(), "ESRI Shapefile")
  
  print("Les isochrones ont bien été créées")
