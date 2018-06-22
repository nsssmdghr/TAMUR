def get_note(valeur, nom_indic, tab_deciles):
	if nom_indic == 'accessibilite tc':
		row = 0
	elif nom_indic == 'accessibilite vp':
		row = 1
	elif nom_indic == 'couverture commerciale':
		row = 2
	elif nom_indic == 'points interet':
		row = 3
	elif nom_indic == 'potentiel commercial':
		row = 4
	deciles = tab_deciles[row]
	i = 0
	note = 0
	while valeur >= deciles[i]:
		note += 1
		i += 1

	return note
