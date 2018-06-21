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

#Importation des deciles
tab_deciles = csv_to_list('deciles,csv')


#Initialisation des dictionnaires
notes = {}
ind_brut = {}

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
point_i = points_interet('POI_EPSC.shp', 'Isochrone10V.shp')
ind_brut['PI'] = point_i

note_point_i = get_note(point_i, 'points interet', tab_deciles)
notes['CU03'] = note_point_i

#Traitement ambiance urbaine
amb_urb = ambiance_urbaine('ambiance_urbaine.csv', param)

note_amb_urb = get_note(amb_urb, 'ambiance urbaine', tab_deciles)
notes['CU01'] = note_amb_urb

#Ponderation et agregation
saisie = dict(csv_to_list('saisie.csv'))
notes.update(saisie)
corresp = dict(csv_to_list('correspondances.csv'))

notes_branches = agreg(notes, param, corresp)

#Exportation
export(notes, notes_branches, ind_brut, nom_dossier)
