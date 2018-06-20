# -*- coding: cp1252 -*-

#Importation des fonctions de traitement

from Scripts.base import *
from Scripts.parts_modales import *
from Scripts.potentiel_commercial import *
from Scripts.accessibilite import *
from Scripts.ambiance_urbaine import *
from Scripts.deciles import *
from Scripts.points_interet import *

chemin = 'Chemin vers dossier principal'
os.chdir(chemin)


os.chdir('./Couches')

#Traitement de base

liste_csv = traitement_base_all()


#Importation du dictionnaire des parametres

param = import_param('parametres.csv')

#Importation des deciles

tab_deciles = csv_to_list('deciles,csv')



#Traitement potentiel commercial

potentiel_commercial('POP_IRIS.csv','REV_IRIS.csv','COMMUNES.csv')

note_pot_com = get_note(pot_com, 'potentiel commercial', tab_deciles)

#Traitement couverture commerciale

note_couv_com = get_note(couv_com, 'couverture commerciale', tab_deciles)

#Traitement accessibilite

pm_vp, pm_tc = parts_modales('PARTS_MOD.csv')

note_access_vp = get_note(access_vp, 'accessibilite vp', tab_deciles)
note_access_tc = get_note(access_tc, 'accessibilite tc', tab_deciles)


#Traitement points d'interet

note_point_i = get_note(point_i, 'points interet', tab_deciles)

#Traitement ambiance urbaine

amb_urb = ambiance_urbaine('ambiance_urbaine.csv', param)

note_amb_urb = get_note(amb_urb, 'ambiance urbaine', tab_deciles)


#Traitement autres indicateurs saisis


#Ponderation et agregation


#Exportation



