
def export(notes, notes_branches, ind_brut, amb_urb_brutes, nom_dossier)
	os.chdir('../')
	os.makedirs(nom_dossier)
	os.chdir('./'+nom_dossier)
	indics = notes.items()
	branches = notes_branches.items()
	amb_urb = amb_urb_brutes.items()
	with open('indicateurs.txt','w') as ind:
		for i in indics:
			ind.write(i[0] + ';' + str(i[1]) + '\n')
	with open('branches.txt','w') as br:
		for b in branches:
			br.write(b[0] + ';' + str(b[1]) + '\n')
	with open('indicateurs_bruts.txt','w') as indb:
		for i in ind_brut:
			indb.write(i[0] + ';' + str(i[1]) + '\n')
	with open('amb_urb_brutes.txt','w') as amb:
		for a in amb_urb:
			amb.write(a[0] + ';' + str(a[1]) + '\n')
		

