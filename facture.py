import os


def creer_fichier_facture():
    # Ouvrir le fichier en mode écriture
    with open('facture.txt', 'w') as f:
        # Écrire l'en-tête
        f.write('Référence Agence\t\tSomme à payer\n')
    print("Le fichier 'facture.txt' a été créé avec succès !")


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
                print("Agence : " + reference)
                print("Somme à payer : " + somme)
                return "Agence : " + reference + "\n" + "Somme à payer : " + somme
        # Si la référence n'a pas été trouvée
        print("Aucune facture trouvée avec la référence " + reference)
        return("Aucune facture trouvée avec la référence " + reference)


def maj_facture(ref_agence):
    print("mise à jour de la facture")
    with open('histo.txt', 'r') as fh:
        next(fh)
        s = 0
        for ligne in fh:
            ref_v, agence, trans, val, res = ligne.strip().split('\t\t')
            if ref_agence == agence:
                if trans == 'Demande' and res == 'succès':
                    with open('vols.txt', 'r') as fv:
                        next(fv)
                        for l in fv:
                            ch = l.strip().split('\t\t')
                            if int(ch[0]) == int(ref_v):
                                prix_place = ch[3]
                                s = s + (int(prix_place) * int(val))
                elif trans == 'Annulation':
                    with open('vols.txt', 'r') as fv:
                        next(fv)
                        for l in fv:
                            ch = l.strip().split('\t\t')
                            if int(ch[0]) == int(ref_v):
                                prix_place = ch[3]
                                s = s - (int(prix_place) * int(val)) + \
                                    0.1 * (int(prix_place) * int(val))
            else:
                print("Pas de transactions pour cette agence " + ref_agence)
        if s != 0:
            with open("facture.txt", "r") as f:
                lines = f.readlines()
            with open("facture.txt", "w") as f:
                for line in lines:
                    ref, somme = line.strip().split('\t\t')
                    if ref == ref_agence:
                        somme = int(somme) + s
                    f.write(f"{ref}\t\t{somme}\n")
