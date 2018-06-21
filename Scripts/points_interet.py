from qgis.core import *
from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer
import processing

def points_interet(POI_EPSG, Isochrone10V, param):
  
  poi = iface.addVectorLayer("POI_EPSG", "POI", "ogr")
  iso10v = iface.addVectorLayer("Isochrone10V", "isochrone10v", "ogr")
  
  poi.removeSelection()
  processing.runalg('qgis:extractbylocation', poi, iso10v, u'within', 0, ".\POIiso.shp")
  POIiso = iface.addVectorLayer(".\POIiso.shp", "POIiso", "ogr")
  
  nombre_POI = POIiso.featureCount()
  
  flag = 0
  while flag not in [1,2,3]:
    flag = raw_input('Veuillez entrer le numero correspondant a la repartition des points d\'interet, puis valider avec Entree : \n1:uniforme autour du quartier \n2:homogène autour du quartier \n3:concentrée d\'un seul côté du quartier \n')
  rep = flag
  
  flag = 0
  while flag not in [1,2,3]:
    flag = raw_input('Veuillez entrer le numero correspondant a la proximite des points d\'interet, puis valider avec Entree : \n1:la plupart des points sont proches du quartier \n2: points à distances moyennes ou hétérogènes du quartier \n3:points éloignés du quartier \n')
  pro = flag
  
  
  return param['R{0}'.format(rep)] * param['PR{0}'.format(pro)] * nombre_POI
