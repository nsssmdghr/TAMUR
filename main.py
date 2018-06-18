# -*- coding: cp1252 -*-

#Importation des fonctions de traitement

from Scripts.base import *
from Scripts.parts_modales import *
from Scripts.potentiel_commercial import *
from Scripts.accessibilite import *


chemin = 'Chemin vers dossier principal'
os.chdir(chemin)


os.chdir('./Couches')

#Traitement de base

liste_csv = traitement_base_all()


#Importation du dictionnaire des parametres

param = import_param('parametres.csv')





#Traitement potentiel commercial

potentiel_commercial('POP_IRIS.csv','REV_IRIS.csv','COMMUNES.csv')


#Traitement couverture commerciale


#Traitement accessibilite

pm_vp, pm_tc = parts_modales('PARTS_MOD.csv')



#Traitement points d'interet


#Traitement ambiance urbaine


#Traitement autres indicateurs saisis


#Ponderation et agregation


#Exportation



