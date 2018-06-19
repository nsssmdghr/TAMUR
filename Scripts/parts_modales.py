# -*- coding: cp1252 -*-

def parts_modales(fichier):
    liste_trans = []
    sum_vp, sum_tc = 0,0
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
                liste_trans.append(int(tab[28]))
            flag = 1

            
    for b in liste_trans:
        if (b in (3,4)):
            sum_vp += 1
        elif (b == 5):
            sum_tc += 1
            
    n = len(liste_trans)
    ratio_vp = float(sum_vp)/n
    ratio_tc = float(sum_tc)/n

    print("Traitement des parts modales termine")
    
    return ratio_vp,ratio_tc
