from base import *

def ambiance_urbaine(fichier,coeffs):
	cor = {'AU0{0}'.format(x):'P31{0}'.format(x) for x in range(1,10)}
	notes = dict(csv_to_list(fichier))
	somme = 0
	denom = 0
	for clef in notes:
		somme += note[clef]*coeffs[cor[clef]]
		denom += coeffs[cor[clef]]

	return somme/denom
