import os


def creer_fichier_vols():
    # Ouvrir le fichier en mode écriture
    with open('vols.txt', 'w') as f:
        # Écrire l'en-tête
        f.write('RéférenceVol\tDestination\tNombre Places\tPrix Place\n')
        # Écrire les données des vols
        f.write('1000\t\tParis\t\t20\t\t500\n')
        f.write('2000\t\tMedina\t\t10\t\t2500\n')
        f.write('3000\t\tMontréal\t\t40\t\t3500\n')
        f.write('4000\t\tDubai\t\t15\t\t3000\n')
        f.write('5000\t\tMaroc\t\t30\t\t2500\n')
    print("Le fichier 'vols.txt' a été créé avec succès !")


def consulter_vol(reference):
    with open('vols.txt', 'r') as f:
        # Passer la première ligne (l'en-tête)
        next(f)
        # Parcourir les lignes du fichier
        for ligne in f:
            # Extraire les champs de la ligne
            reference_vol, destination, nb_places, prix_place = ligne.strip().split('\t\t')
            # Vérifier si la référence correspond
            if reference_vol == reference:
                # Afficher les informations du vol
                print("Vol : " + reference)
                print("Destination : " + destination)
                print("Nombre de places disponibles : " + nb_places)
                print("Prix d'une place : " + prix_place)
                return"Vol : " + reference + "\n"+"Destination : " + destination+"\n"+"Nombre de places disponibles : " + nb_places+"\n"+"Prix d'une place : " + prix_place+"\n"
        # Si la référence n'a pas été trouvée
        print("Aucun vol trouvé avec la référence " + reference)
        return "Aucun vol trouvé avec la référence " + reference
