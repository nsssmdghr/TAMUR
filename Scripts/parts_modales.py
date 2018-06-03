# -*- coding: cp1252 -*-
from numpy import *


def parts_modales(fichier):
    liste_trans = []
    sum_vp_nav, sum_vp_sta, sum_tc_nav, sum_tc_sta = 0,0,0,0 
    with open(fichier,'r') as f:
        flag = 0   
        for l in f:
            if flag == 1:
                att = ''
                tab = []
                for c in l:
                    if c == ',':
                        tab.append(att)
                        att = ''
                    else:        
                        att += c
                tab.append(att[:-1])
                liste_trans.append([int(tab[28]),int(tab[0] == tab[3])])
            flag = 1

            
    for b in liste_trans:
        if (b[0] in (3,4)) and (b[1] == 0):
            sum_vp_nav += 1
        elif (b[0] in (3,4)) and (b[1] == 1):
            sum_vp_sta += 1
        elif (b[0] == 5) and (b[1] == 0):
            sum_tc_nav += 1
        elif (b[0] == 5) and (b[1] == 1):
            sum_tc_sta += 1
    n = len(liste_trans)
    ratio_vp_nav = float(sum_vp_nav)/n
    ratio_vp_sta = float(sum_vp_sta)/n
    ratio_tc_nav = float(sum_tc_nav)/n
    ratio_tc_sta = float(sum_tc_sta)/n
    with open('ratios_vp_tc.csv','w') as r:
            r.write('ratio_vp_nav,ratio_vp_sta,ratio_tc_nav,ratio_tc_sta \n{0},{1},{2},{3}'.format(ratio_vp_nav,ratio_vp_sta,ratio_tc_nav,ratio_tc_sta))

    print("Traitement des parts modales termine")

