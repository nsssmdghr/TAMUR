# -*- coding: cp1252 -*-

#Importation des fonctions de traitement

from Scripts.base import *
from Scripts.importation import *
from Scripts.parts_modales import *
from Scripts.accessibilite import *
from Scripts.ambiance_urbaine import *
from Scripts.deciles import *
from Scripts.points_interet import *
from Scripts.agregation import *
from Scripts.export import *
from Scripts.couverture_commerciale import *
from qgis.core import *
from qgis.utils import iface 
from qgis.analysis import QgsGeometryAnalyzer 
from qgis.PyQt.QtCore import QVariant
import processing

#Definition du chemin vers le dossier principal, a modifier manuellement
chemin = 'Chemin vers dossier principal'
os.chdir(chemin)
os.chdir('.\Couches')


#Traitement de base
liste_csv = traitement_base_all()


#Importation du dictionnaire des parametres
param = import_param('parametres.csv')

#Importation du nom du dossier en cours de traitement
nom_dossier = get_nom('nom_dossier.csv')

#Importation du numero de l'IRIS
num_iris = get_nom('num_iris.csv')

#Importation des deciles
tab_deciles = csv_to_list('deciles,csv')


#Initialisation des dictionnaires
notes = {}
ind_brut = {}

#Traitement potentiel commercial

sup_lignes(Donnees_Communes,5)
sup_lignes(Population_IRIS,5)
sup_lignes(Revenus_IRIS,5)
keep_col( Population_IRIS,[1,13,30])
keep_col(Revenus_IRIS,[1,7])
keep_col(Donnees_Communes,[1,5,7])
sup_lignes_null(Population_IRIS)
sup_lignes_null(Donnees_Communes)
sup_lignes_null(Revenus_IRIS)
print("Fichiers prets pour le traitement du pouvoir d'achat")


#Importation des couche et creation des appels
iris = iface.addVectorLayer("IRIS.shp","IRIS","ogr")
communes = iface.addVectorLayer("COMMUNES.csv","COMMUNES","ogr")
reviris = iface.addVectorLayer("REV_IRIS.csv","REV_IRIS","ogr")
popiris = iface.addVectorLayer("POP_IRIS.csv","POP_IRIS","ogr")

#Selection de l'IRIS a etudier
num = num_iris
it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = ' + num) ))
iris.setSelectedFeatures( [ f.id() for f in it ] )

#Creation du perimètre de 10km
QgsGeometryAnalyzer().buffer(iris, "Buffer.shp",10000, True, False, -1)
buffer = iface.addVectorLayer("Buffer.shp","Buffer","ogr")

#Creation d'une couche restreinte au perimètre de 10km
iris.removeSelection()

processing.runalg('qgis:extractbylocation', iris, buffer, u'within', 0, "Perim.shp")
perim = iface.addVectorLayer("Perim.shp","Perim","ogr")

#Jointures des differentes bases de donnees à la couche geographique
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

#Creation de nouvelles colonnes (pouvoir d'achat, distance et potentiel de chaque IRIS)
perim.dataProvider().addAttributes([QgsField("P_Achat", QVariant.Int), QgsField("Distance", QVariant.Int),QgsField("Potentiel", QVariant.Int)])
perim.updateFields()

#Remplissage des nouvelles colonnes
#Creation d'un appel pour le centroïde de l'IRIS etudie
it = iris.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"DCOMIRIS" = {0}'.format(num) ))
for feature in it:
  centro = feature.geometry().centroid()

n=param['n']

#Remplissage des colonnes pouvoir d'achat (numero 8) et distance (numero 9)
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

#Remplissage de la colonne potentiel (numero 10)
features = perim.getFeatures()
for feature in features:
  if not feature['COMMUNES_Field_2'] is None:
    perim.dataProvider().changeAttributeValues({ feature.id() : { 10 : feature['P_Achat']/(feature['Distance']+200)^n } })

#Exportation des donnees des IRIS du perimètre dans un CSV, calcule et renvoi du resultat final (somme de la colonne K)
QgsVectorFileWriter.writeAsVectorFormat(perim, r'perim.csv', "utf-8", None, "CSV")
pot_com = somme_col('perim.csv', 11)

QgsMapLayerRegistry.instance().removeMapLayers( [iris.id()] )
QgsMapLayerRegistry.instance().removeMapLayers( [communes.id()] )
QgsMapLayerRegistry.instance().removeMapLayers( [reviris.id()] )
QgsMapLayerRegistry.instance().removeMapLayers( [popiris.id()] )
QgsMapLayerRegistry.instance().removeMapLayers( [buffer.id()] )
QgsMapLayerRegistry.instance().removeMapLayers( [perim.id()] )

ind_brut['PC'] = pot_com

note_pot_com = get_note(pot_com, 'potentiel commercial', tab_deciles)
notes['CM05'] = note_pot_com 

#Traitement couverture commerciale
couv_com = couverture_commerciale('IRIS.shp', 'POP_IRIS_bis.csv', 'PAR_IRIS.csv', 'PAR_COM.csv', 'COM_IRIS.csv', 'COM_COM.csv', 'SAN_IRIS.csv', 'SAN_COM.csv', 'TRA_IRIS.csv', 'TRA_COM.csv', 'Isochrone10P.shp')
ind_brut['CC'] = couv_com

note_couv_com = get_note(couv_com, 'couverture commerciale', tab_deciles)
notes['CM03'] = note_couv_com


#Traitement accessibilite
pm_vp, pm_tc = parts_modales('PARTS_MOD.csv')
access_vp, access_tc = accessibilite('Couche_TC.shp', 'COMMUNES_OSM.shp', 'Emp_Com.csv', 'Isochrone10P.shp', 'Isochrone30V.shp')
ind_brut['AVP'] = access_vp
ind_brut['ATC'] = access_tc


note_access_vp = get_note(access_vp, 'accessibilite vp', tab_deciles)
note_access_tc = get_note(access_tc, 'accessibilite tc', tab_deciles)

note_access = note_access_vp * param['P322'] + note_access_tc * param['P321'] 
note_access /= param['P321'] + param['P322']
notes['CU02'] = note_access


#Traitement points d'interet
point_i = points_interet('POI_EPSC.shp', 'Isochrone10V.shp', param)
ind_brut['PI'] = point_i

note_point_i = get_note(point_i, 'points interet', tab_deciles)
notes['CU03'] = note_point_i

#Traitement ambiance urbaine
amb_urb_brutes = dict(csv_to_list('ambiance_urbaine.csv'))
amb_urb = ambiance_urbaine('ambiance_urbaine.csv', param)

notes_amb_urb = get_note(amb_urb, 'ambiance urbaine', tab_deciles)
notes['CU01'] = note_amb_urb

#Ponderation et agregation
saisie = dict(csv_to_list('saisie.csv'))
moyennes = dict(csv_to_list('moyennes.csv'))
moyennes['CU02'] = 5
moyennes['CU03'] = 5
moyennes['CM05'] = 5
                
notes.update(saisie)
corresp = dict(csv_to_list('correspondances.csv'))

normalisation(notes)
notes_branches = agreg(notes, param, corresp)


#Exportation
export(notes, notes_branches, ind_brut, amb_urb_brutes, nom_dossier)
