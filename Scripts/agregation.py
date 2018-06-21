def agreg(notes, param, corresp):
	notes_branches = {CP:0, PA:0, CU:0, CF:0, NA:0, CE:0, CM:0}
	somme_pond = {CP:0, PA:0, CU:0, CF:0, NA:0, CE:0, CM:0}
		for id_entree in notes:
  			notes_branches[id_entree[:2]] += notes[id_entree] * param[corresp[id_entree]]
  			somme_pond[id_entree[:2]] += param[corresp[id_entree]]
		for id in notes_branches:
 			notes_branches[id] /= somme_pond[id]
 	return notes_branches