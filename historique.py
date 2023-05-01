import os
from facture import maj_facture


def creer_fichier_histo():
    # Ouvrir le fichier en mode écriture
    with open('histo.txt', 'w') as f:
        # Écrire l'en-tête
        f.write('RéférenceVol\t\tAgence\t\tTransaction\t\tValeur\t\tRésultat\n')
    print("Le fichier 'histo.txt' a été créé avec succès !")


# Fonction pour afficher l'historique des transactions
def afficher_historique():
    # Ouvrir le fichier en mode lecture
    with open('histo.txt', 'r') as f:
        # Lire le contenu du fichier ligne par ligne
        for ligne in f:
            # Diviser la ligne en champs selon le caractère de tabulation
            champs = ligne.strip().split('\t\t\t')
            # Afficher les champs séparés par des tabulations
            print('\t\t\t'.join(champs))


# Fonction pour mettre à jour l'historique des transactions
def maj_historique(reference_vol, agence, transaction, valeur, resultat):

    # Ouvrir le fichier en mode ajout (append)
    with open('histo.txt', 'a') as f:
        # Écrire une nouvelle ligne avec les informations de la transaction
        f.write(
            f"{reference_vol}\t\t\t{agence}\t\t{transaction}\t\t\t{valeur}\t\t{resultat}\n")

# Fonction pour effectuer une réservation


def reserver(reference_vol, agence, nombre_places):
    # Ouvrir le fichier des vols en mode lecture
    with open('vols.txt', 'r') as f:
        # Lire le contenu du fichier ligne par ligne
        for ligne in f:
            # Diviser la ligne en champs selon le caractère de tabulation
            champs = ligne.strip().split('\t\t')
            # Vérifier si la référence du vol correspond
            if champs[0] == reference_vol:
                # Récupérer le nombre de places disponibles
                places_dispo = int(champs[2])
                # Vérifier si le nombre de places demandées est inférieur ou égal au nombre de places disponibles
                if int(nombre_places) <= places_dispo:
                   # Mettre à jour le nombre de places disponibles dans le fichier vols.txt
                    nouvelles_places_dispo = places_dispo - int(nombre_places)
                    nouvelle_ligne = f"{champs[0]}\t\t{champs[1]}\t\t{nouvelles_places_dispo}\t\t{champs[3]}\n"
                    contenu = ''
                    # Ouvrir le fichier en mode lecture/écriture
                    with open('vols.txt', 'r+') as f_vols:
                        # Lire le contenu du fichier ligne par ligne
                        for ligne_vols in f_vols:
                            # Remplacer la ligne correspondante par la nouvelle ligne mise à jour
                            if ligne_vols.startswith(reference_vol):
                                contenu += nouvelle_ligne
                            else:
                                contenu += ligne_vols
                        # Rembobiner le curseur du fichier au début
                        f_vols.seek(0)
                        # Écrire le contenu mis à jour dans le fichier
                        f_vols.write(contenu)
                        # Tronquer le fichier après la dernière ligne écrite
                        f_vols.truncate()

                    # Mettre à jour l'historique des transactions avec succès
                    maj_historique(reference_vol, agence,
                                   'Demande', nombre_places, 'succès')
                    maj_facture(agence)
                    return "MAJ fait, résultat succées"
                else:
                    # Mettre à jour l'historique des transactions avec échec
                    maj_historique(reference_vol, agence,
                                   'Demande', nombre_places, 'impossible')
                    return "MAJ fait, résultat impossible"
            # Si la référence du vol n'est pas trouvée,
    return "Pas de vol avec cette référence"

# Fonction pour effectuer une annulation


def annuler(reference_vol, agence, nombre_places):
    # verifier le nbre de places reservé par l'agence
    with open('histo.txt', 'r') as fh:
        next(fh)
        places = 0
        for ligne in fh:
            ref_v, ref_agence, trans, val, res = ligne.strip().split('\t\t')
            if(ref_v == reference_vol and agence == ref_agence and res == 'succès'):
                if trans == 'Annulation':
                    places -= int(val)
                if trans == 'Demande':
                    places += int(val)
        if(places < int(nombre_places) or int(nombre_places) == 0):
            return "Annulation impossible: nbre de places ne correspond pas"
    with open('vols.txt', 'r') as f:
        # Lire le contenu du fichier ligne par ligne
        for ligne in f:
            # Diviser la ligne en champs selon le caractère de tabulation
            champs = ligne.strip().split('\t\t')
            # Vérifier si la référence du vol correspond
            if champs[0] == reference_vol:
                places_dispo = int(champs[2])
                nouvelles_places_dispo = places_dispo + int(nombre_places)
                nouvelle_ligne = f"{champs[0]}\t\t{champs[1]}\t\t{nouvelles_places_dispo}\t\t{champs[3]}\n"
                contenu = ''
                # Ouvrir le fichier en mode lecture/écriture
                with open('vols.txt', 'r+') as f_vols:
                   # Lire le contenu du fichier ligne par ligne
                    for ligne_vols in f_vols:
                        # Remplacer la ligne correspondante par la nouvelle ligne mise à jour
                        if ligne_vols.startswith(reference_vol):
                            contenu += nouvelle_ligne
                        else:
                            contenu += ligne_vols
                    # Rembobiner le curseur du fichier au début
                    f_vols.seek(0)
                    # Écrire le contenu mis à jour dans le fichier
                    f_vols.write(contenu)
                    # Tronquer le fichier après la dernière ligne écrite
                    f_vols.truncate()

                # Mettre à jour l'historique des transactions avec succès
                maj_historique(reference_vol, agence, 'Annulation',
                               nombre_places, 'succès')
                return "MAJ faite, résultat succées"
   # Si la référence du vol n'est pas trouvée,
    return "Pas de vol avec cette référence"
