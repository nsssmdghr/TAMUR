# -*- coding: cp1252 -*-
import os
from string import maketrans
from numpy import *
from importation import *

#Remplacement des ';' et des caracteres non pris en compte
def traitement_base(fichier):
        if not (fichier.endswith('.csv') or fichier.endswith('.txt')):
                print('Erreur: le fichier n\'est ni un .csv ni un .txt')
        else:
                source = open(fichier, 'r')
                l_0 = str(source.readline())
                if ';' in l_0:
                        nom_dest = fichier               
                        dest = open('_.csv', 'w')
                        intab1=','
                        outtab1='.'
                        intab2=';'
                        outtab2=','
                        trantab1=maketrans(intab1,outtab1)
                        trantab2=maketrans(intab2,outtab2)
                        l_0 =l_0.translate(trantab1)
                        l_0 = l_0.translate(trantab2)
                        dest.write(l_0)
                        for l in source:
                                l = l.translate(trantab1)
                                l = l.translate(trantab2)
                                dest.write(l)
                        source.close()
                        dest.close()
                        os.remove(fichier)
                        os.rename('_.csv',fichier)

#Supprimer les n premieres lignes                
def sup_lignes(fichier,n):
        if not (fichier.endswith('.csv') or fichier.endswith('.txt')):
                print('Erreur: le fichier n\'est ni un .csv ni un .txt')
        else:
                source = open(fichier, 'r')        
                nom_dest = fichier               
                dest = open('_.csv', 'w')
                i=1
                for l in source:
                        if i>n:
                                dest.write(l)
                        i+=1
                source.close()
                dest.close()
                os.remove(fichier)
                os.rename('_.csv',fichier)

#Garder uniquement les lignes comportant une certaine chaine de caracteres, en plus des n premieres
def select_lignes(fichier,chaine,n=1):
        if not (fichier.endswith('.csv') or fichier.endswith('.txt')):
                print('Erreur: le fichier n\'est ni un .csv ni un .txt')
        else:
                source = open(fichier, 'r')        
                nom_dest = fichier               
                dest = open('_.csv', 'w')
                i=1
                for l in source:
                        if chaine in l or i <= n :
                                dest.write(l)
                        i+=1
                source.close()
                dest.close()
                os.remove(fichier)
                os.rename('_.csv',fichier)


#Convertir un .txt en .csv
def txt_to_csv(fichier):
        if not fichier.endswith('.txt'):
                print('Erreur: le fichier n\'est pas un .txt')
        else:
                new_name=fichier[:-4]+'.csv'
                os.rename(fichier,new_name)



#Convertir en array
def csv_to_array(fichier):
        if not fichier.endswith('.csv'):
                print('Erreur: le fichier n\'est pas un .csv')
        else:
                with open(fichier,'r') as f:
                        tab=[]
                        for l in f:
                                att = ''
                                tab_p=[]
                                for c in l:
                                        if c == ',':
                                                tab_p.append(att)
                                                att=''
                                        else:        
                                                att += c
                                tab_p.append(att[:-1])
                                tab.append(tab_p)
                        return array(tab,dtype='|S50')


def keep_col(fichier,liste_col):
        if not fichier.endswith('.csv'):
                print('Erreur: le fichier n\'est pas un .csv')
        else:
                for i in range(len(liste_col)):
                        liste_col[i] -= 1
                with open(fichier,'r') as f:
                        with open('_.csv','w') as d:
                                for l in f:
                                        compteur = 0
                                        for c in l:
                                                if c == ',':
                                                        compteur += 1
                                                if compteur in liste_col:
                                                        d.write(c)           
                                        d.write('\n')
                os.remove(fichier)
                os.rename('_.csv',fichier)

def traitement_base_all():
        
        liste_txt = import_txt('.')
        if liste_txt == []:
                print('Aucun fichier .txt dans le dossier.')
        else:
                print('Liste des fichiers .txt: ')
                print(liste_txt)

        for fichier in liste_txt:
                txt_to_csv(fichier)
        
        liste_csv = import_csv('.')
        if liste_csv == []:
                print('Aucun fichier .csv dans le dossier.')
        else:
                print('Liste des fichiers .csv: ')
                print(liste_csv)


        for fichier in liste_csv:       
                traitement_base(fichier)
                print('Traitement de '+fichier+' terminé')

        return liste_csv

def sup_lignes_null(fichier):
	with open(fichier,'r') as f:
		with open('_.csv','w') as d:
			for l in f:
				if not (l.startswith(',') or l.endswith(',\n') or ',,' in l):
					d.write(l)
	os.remove(fichier)
	os.rename('_.csv',fichier)



def somme_col(fichier,n):
        n -= 1
        liste_col_n = []
        somme = 0 
        with open(fichier,'r') as f:
                if not fichier.endswith('.csv'):
                        print('Erreur: le fichier n\'est pas un .csv')
                else:
                        with open(fichier,'r') as f:
                                flag = 0
                                for l in f:
                                        compteur = 0
                                        val = ''
                                        if flag == 1:
                                                for c in l:
                                                        if compteur == n and c not in [',','\n']:
                                                                val += c
                                                        if c == ',':
                                                                compteur += 1
                                                somme += float(val)
                                        flag = 1
        return somme


def import_param(fichier):
        ar_param=csv_to_array(fichier)
        dic_param=dict(ar_param)
        for id in dic_param:
                dic_param[id]=float(dic_param[id])
        return dic_param
