from vol import *
from historique import *
from facture import *
from serverLaunch import *
from multiprocessing import Process
import os

procs = []


def initialiser():
    creer_fichier_vols()
    creer_fichier_histo()
    creer_fichier_facture()


if __name__ == '__main__':

    while True:

        os.system("cls")
        response = 0
        print("********BIENVENUE DANS LA PLATEFORME DE LA COMPAGNIE AERIENNE*******")
        if(len(procs) == 1):
            print(f"********SERVEUR EN MARCHE son PID{procs[0].pid}*******")
        print("1- Consulter un vol")
        print("2- Consulter la facture d'une agence")
        print("3- Consulter l'historique des trasactions")
        print("4- Lancer le serveur")
        print("5- Réinitialiser les données")
        print("6- Exit")
        response = input()
        while int(response)not in [1, 2, 3, 4, 5, 6]:
            print("Choix invalide! Essayez de nouveau [1,2,3,4]: ")
            response = input()
        if(int(response) == 1):
            print("Veuillez saisir la référence du vol à consulter: ", end="")
            reference = input()
            consulter_vol(reference)
            print("Entrer pour continuer...", end="")
            input()
        if(int(response) == 2):
            print("Veuillez saisir la référence de l'agence: ", end="")
            ref = input()
            consulter_facture(ref)
            print("Entrer pour continuer...", end="")
            input()
        if(int(response) == 3):
            afficher_historique()
            print("Entrer pour continuer...", end="")
            input()
        if(int(response) == 4):
            if(len(procs) >= 1):
                print("Serveur en marche voulez vous l'arreter? [O/N]")
                rep = input()
                if(rep.lower() == 'o'):
                    procs[0].terminate()
                    procs.pop()
            else:
                proc = Process(target=launchServer)
                procs.append(proc)
                proc.start()
        if(int(response) == 5):
            print(
                "ACTION IRREVERSIBLE! Voulez vous vraiment effacer la base? [O/N]")
            rep = input()
            if(rep.lower() == 'o'):
                initialiser()
        if(int(response) == 6):
            break
    print("********AU REVOIR*******")
