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
