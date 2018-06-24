# -*- coding: cp1252 -*-

#Importation des fonctions de traitement

from Scripts.base import *
from Scripts.importation import *
from Scripts.parts_modales import *
from Scripts.potentiel_commercial import *
from Scripts.accessibilite import *
from Scripts.ambiance_urbaine import *
from Scripts.deciles import *
from Scripts.points_interet import *
from Scripts.agregation import *
from Scripts.export import *
from Scripts.couverture_commerciale import *

#Definition du chemin vers le dossier principal, a modifier manuellement
chemin = 'Chemin vers dossier principal'
os.chdir(chemin)
os.chdir('./Couches')


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

#Préparation des isochrones
geo = iface.addVectorLayer('COMMUNES_OSM.shp',"GEO","ogr")
  
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


#Traitement potentiel commercial
pot_com = potentiel_commercial('IRIS.shp', 'COMMUNES.csv', 'REV_IRIS.csv', 'POP_IRIS.csv', num_iris, param['n'])
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
