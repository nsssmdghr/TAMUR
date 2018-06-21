import os

#Fonction d'importation de la liste des fichiers .csv du dossier dans lequel se situe le script
def import_csv(chemin):
        f=os.listdir(chemin)
        fp=[]
        for fichier in  f:
                if fichier.endswith('.csv'):
                        fp.append(fichier) 
        return fp

#Fonction d'importation de la liste des fichiers .txt
def import_txt(chemin):
        f=os.listdir(chemin)
        fp=[]
        for fichier in  f:
                if fichier.endswith('.txt'):
                        fp.append(fichier) 
        return fp

#Importation du contenu d'un csv servant a stocker 1 chaine de caracteres
def get_nom(fichier):
        nom = ''
        with open(fichier, 'r') as f:
                nom = f.readline()
        return nom

