def accessibilite(Couche_TC):

  ##Demander à l'utilisateur de suivre le mode d'emploi pour créer les isochrones
  flag = 0
  while flag != 1:
    flag = raw_input("Veuillez suivre la section 'Isochrones' du mode d'emploi, puis taper 1 et valider avec Entree.")

  ##importation des couches et création des appels
  isochrone = iface.addVectorLayer("Couche_TC", "TC", "ogr")
  TC = iface.addVectorLayer(".\Isochrone.shp", "isochrone", "ogr")

  ##création et importation de la couche TC restreinte à l'isochrone
  import processing
  isochrone.removeSelection()
  processing.runalg('qgis:extractbylocation', TC, isochrone, u'within', 0, "TC dans isochrone.shp")
  TCiso = iface.addVectorLayer(".\TC dans isochrone.shp","TCiso","ogr")

  ##comptage des arrêts de bus dans l'isochrone
  it = TCiso.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" = bus_stop' )) 
  TCiso.setSelectedFeatures( [ f.id() for f in it ] )
  TCiso.selectedFeatureCount()

  ##Demander à l'utilisateur d'entrer manuellement le compte dans le tableaur résultat (?)
  flag = 0
  while flag != 1:
    nb_arrets_bus = raw_input("Veuillez entrer le nombre d'arrets de bus presents dans l'isochrone, puis valider avec Entree.")
    try:
        int(nb_arrets_bus)  
        flag = 1
        nb_arrets_bus = int(nb_arrets_bus)
    except ValueError:
        flag = 0
    
  
  ##comptage des points autres qu'arrêts de bus
  it = TCiso.getFeatures(QgsFeatureRequest().setFilterExpression ( u'"fclass" != bus_stop' )) 
  TCiso.setSelectedFeatures( [ f.id() for f in it ] )
  TCiso.selectedFeatureCount()

  ##Demander à l'utilisateur d'entrer manuellement le compte dans le tableau résultat (?)
  flag = 0
  while flag != 1:
    nb_autres_points = raw_input("Veuillez entrer le nombre de points n'etant pas des arrets de bus presents dans l'isochrone, puis valider avec Entree.")
    try:
        int(nb_autres_points)  
        flag = 1
        nb_autres_points = int(nb_autres_points)
    except ValueError:
        flag = 0
