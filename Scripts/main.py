# -*- coding: cp1252 -*-
import os
from string import maketrans


#Importation des fonctions de traitement
from base import *
from parts_modales import *
from importation import *



#Remplacer '.' par 'Chemin/Du/Dossier' si les fichiers ne se situent pas dans le meme dossier
chemin = '.'

#Importation des listes des fichiers .csv et .txt
liste_csv = import_csv(chemin)
liste_txt = import_txt(chemin)


#Affichage de la liste des fichiers .csv
if liste_csv == []:
        print('Erreur: aucun fichier .csv dans le dossier.')
else:
        print('Liste des fichiers .csv: ')
        print(liste_csv)


#Affichage de la liste des fichiers .txt
if liste_txt == []:
        print('Erreur: aucun fichier .txt dans le dossier.')
else:
        print('Liste des fichiers .txt: ')
        print(liste_txt)



#Traitement des fichiers .csv
for fichier in liste_csv:       
        traitement_base(fichier)
        print('Traitement de '+fichier+' terminé')
        keep_col(fichier,[0,1,3])
        

#Conversion des fichiers .txt en .csv puis traitement
for fichier in liste_txt:
        txt_to_csv(fichier)
        traitement_base(fichier)
        print('Traitement de '+fichier+' terminé')
