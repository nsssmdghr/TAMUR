from qgis.core import *
from qgis.utils import iface 
import processing

def points_interet(POI_EPSG, Isochrone10V):
  
  poi = iface.addVectorLayer("POI_EPSG", "POI", "ogr")
  iso10v = iface.addVectorLayer("Isochrone10V", "isochrone10v", "ogr")
  
  poi.removeSelection()
  processing.runalg('qgis:extractbylocation', poi, iso10v, u'within', 0, ".\POIiso.shp")
  POIiso = iface.addVectorLayer(".\POIiso.shp", "POIiso", "ogr")
  
  nombre_POI = POIiso.featureCount()
  return nombre_POI
