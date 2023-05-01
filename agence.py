# les importations
import os
import socket
def clear(): return os.system('cls')


# Les actions autorisées par le serveur pour chaque agence
# La consultation des vols
def consulterVol(agence):
    clear()
    print("Veuillez saisir la référence du vol à consulter: ", end="")
    ref = input()
    agence.sendall(bytes("ConsulterVol,{}".format(ref), 'UTF-8'))

# La consultation des transactions (historique)


def consulterTransaction(agence):
    clear()
    print("Veuillez saisir la référence du vol pour consulter transaction :")
    ref = input()
    agence.sendall(bytes("ConsulterHistorique,{}".format(ref), 'UTF-8'))

# La consultation des factures


def consulterFacture(agence):
    clear()
    agence.sendall(bytes("RecevoirFacture", 'UTF-8'))


# une des actions effectue par l'agence : transaction qui présente la demande et l'annulation des places du vol en faisant les mise-a-jour necessaires
def transactionVol():
    clear()
    print("1- Réserver places ")
    print("2- Annuler places")
    print("3- quitter")
    rsp = input()
    while(int(rsp) not in [1, 2, 3]):
        print("Choix invalide! Essayez de nouveau [1,2,3]: ")
        rsp = input()
    msg = ""
    if int(rsp) == 1:
        print("Saisir la référence du vol: ")
        ref = input()
        print("Saisir le nombre de places: ")
        nb_places = input()
        msg = "Reservation,{},{}".format(ref, nb_places)
        agence.sendall(bytes(msg, 'UTF-8'))

    if int(rsp) == 2:
        print("Saisir la référence du vol: ")
        ref = input()
        print("Saisir le nombre de places: ")
        nb_places = input()
        msg = "Annulation,{},{}".format(ref, nb_places)
        agence.sendall(bytes(msg, 'UTF-8'))

    if int(rsp) == 3:
        actionAgence(agence)


# actions effectuees pour une agence

def actionAgence(agence):
    clear()
    response = 0
    print("1- Consulter un vol")
    print("3- Consulter la facture à payer")
    print("4- Realiser une trasaction")
    print("choix d'action :", end="")
    response = input()
    while int(response)not in [1, 2, 3, 4]:
        print("Choix invalide! Essayez de nouveau [1,2,3,4]: ")
        response = input()
    if(int(response) == 1):
        consulterVol(agence)
    if(int(response) == 3):
        consulterFacture(agence)
    if(int(response) == 4):
        transactionVol()


# le type du socket : SOCK_STREAM pour le protocole TCP
# le type du socket : SOCK_DGRAM pour le protocole UDP
SERVER = "127.0.0.1"
PORT = 8084
agence = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agence.connect((SERVER, PORT))
agence.sendall(bytes("Salut", 'UTF-8'))
in_data = agence.recv(30720)
while True:

    actionAgence(agence)
    in_data = agence.recv(5072)
    if(in_data.decode() != "Salut"):
        clear()
        print("Serveur a retourné :", in_data.decode())
        input("Press Enter to continue...")

    if(in_data.decode() == "exit"):

        break
agence.close()
