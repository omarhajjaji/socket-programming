import logging

logger = logging.getLogger("logger")


def creer_fichier_facture():

    # Ouvrir le fichier en mode écriture
    with open('facture.txt', 'w') as f:
        # Écrire l'en-tête
        f.write('Référence Agence\t\tSomme à payer\n')
    logger.info("Le fichier 'facture.txt' a été créé avec succès !")


def consulter_facture(reference):
    with open('facture.txt', 'r') as f:
        # Passer la première ligne (l'en-tête)
        next(f)
        # Parcourir les lignes du fichier
        for ligne in f:
            # Extraire les champs de la ligne
            reference_agence, somme = ligne.strip().split('\t\t')
            # Vérifier si la référence correspond
            if reference_agence == reference:
                # Afficher les informations de la facture
                logger.info("Agence : " + reference)
                logger.info("Somme à payer : " + somme)
                return "Agence : " + reference + "\n" + "Somme à payer : " + somme
        # Si la référence n'a pas été trouvée
        logger.info("Aucune facture trouvée avec la référence " + reference)
        return("Aucune facture trouvée avec la référence " + reference)


def maj_facture(ref_agence):
    logger.debug("mise à jour de la facture")
    with open('histo.txt', 'r') as fh:
        next(fh)
        s = 0
        for ligne in fh:
            ref_v, agence, trans, val, res = ligne.strip().split('\t\t')
            if ref_agence == agence:
                logger.debug('facture: Agence existe')
                if trans == 'Demande' and res == 'succès':
                    logger.debug('facture: Vol existe (demande)')
                    with open('vols.txt', 'r') as fv:
                        next(fv)
                        for l in fv:
                            ch = l.strip().split('\t\t')
                            if int(ch[0]) == int(ref_v):

                                prix_place = ch[3]
                                s = s + (int(prix_place) * int(val))
                elif trans == 'Annulation':
                    logger.debug('facture: Vol existe (annulation)')
                    with open('vols.txt', 'r') as fv:
                        next(fv)
                        for l in fv:
                            ch = l.strip().split('\t\t')
                            if int(ch[0]) == int(ref_v):
                                prix_place = ch[3]
                                s = s - (int(prix_place) * int(val)) + \
                                    0.1 * (int(prix_place) * int(val))
            else:
                logger.info(
                    "Pas de transactions pour cette agence " + ref_agence)
        if s != 0:
            logger.debug("S=", s)
            isUpdated = False
            nouvelle_ligne = f"{ref_agence}\t\t{s}\n"
            contenu = ''
            # Ouvrir le fichier en mode lecture/écriture
            with open('facture.txt', 'r+') as f_facture:
                # Lire le contenu du fichier ligne par ligne
                for ligne_facture in f_facture:
                    # Remplacer la ligne correspondante par la nouvelle ligne mise à jour

                    if ligne_facture.startswith(ref_agence):
                        contenu += nouvelle_ligne
                        isUpdated = True
                    else:
                        contenu += ligne_facture
                # Rembobiner le curseur du fichier au début
                f_facture.seek(0)
                # Écrire le contenu mis à jour dans le fichier
                f_facture.write(contenu)
                # Si pas de mise à jour => nouvelle facture
                if (not(isUpdated)):
                    f_facture.write(nouvelle_ligne)
                # Tronquer le fichier après la dernière ligne écrite
                f_facture.truncate()
                # Si aucune facture ne correspond (nouvelle facture)
            logger.info("Facture mise à jour")
