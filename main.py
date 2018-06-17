# -*- coding: cp1252 -*-

#Importation des fonctions de traitement

from Scripts.base import *
from Scripts.parts_modales import *
from Scripts.pouvoir_achat import *

os.chdir('.\Couches')




#Traitement de base

liste_csv = traitement_base_all()


#Importation du dictionnaire des parametres

param = import_param('parametres.csv')


#Traitement parts modales

parts_modales('PARTS_MOD.csv')

#Traitement pouvoir d'achat

pouvoir_achat('POP_IRIS.csv','REV_IRIS.csv','COMMUNES.csv')
