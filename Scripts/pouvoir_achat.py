# -*- coding: cp1252 -*-

from numpy import *
from base import *






def pouvoir_achat(fichier_pop,fichier_rev,fichier_com):
	sup_lignes(fichier_com,5)
	sup_lignes(fichier_pop,5)
	sup_lignes(fichier_rev,5)
	keep_col(fichier_pop,[1,13,30])
	keep_col(fichier_rev,[1,7])
	keep_col(fichier_com,[1,5,7])
	sup_lignes_null(fichier_pop)
	sup_lignes_null(fichier_com)
	sup_lignes_null(fichier_rev)
	print("Fichiers prets pour le traitement du pouvoir d'achat")


