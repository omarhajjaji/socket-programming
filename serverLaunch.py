import socket
import threading
from vol import *
from historique import *
from facture import consulter_facture
import logging

# Mutex pour assurer l'exlusion mutuelle
mutex = threading.Lock()
logging.basicConfig(filename='serveur.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
log = logging.getLogger("logger")

# Liste des actions autorisée par le serveur pour le client
actions_autorisees = ["ConsulterVol",
                      "RecevoirFacture", "Reservation", "Annulation"]
current_threads = []
msgsize = 1024

# Gestion des clients a travers les threads


class threadClients(threading.Thread):

    # Recuperer l'adresse et la socket du client connecté
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        logging.info(
            f"nouvelle connexion avec l'adresse: {clientAddress}: Thread créé")

    # Recuperer l'action autorisé pour le client connecté afin de l'excéuter
    def run(self):
        log.info(f"Connexion de : {self.clientAddress}")
        self.csocket.send(bytes("hello", 'utf-8'))
        rsp = ''
        while True:
            try:
                data = self.csocket.recv(3072)
            except socket.error as e:
                log.info("Socket déconnecté !")
                break
            rsp = data.decode()
            if rsp != "Salut":
                log.info(f"Demande du client: {rsp.split(',')[0]}")
                action = rsp.split(",")[0]
                if action in actions_autorisees:
                    TraitementServeur(self.clientAddress, rsp, self.csocket)
                elif rsp == 'exit':
                    break
                else:
                    msg = " n'est pas une action autorisée!"
                    self.csocket.send(bytes(msg, 'UTF-8'))

        log.info("Client dont l'adresse est : ",
                 self.clientAddress, " est deconnete ..")
# fin de la classe


# Notifier a chaque fois le serveur de l'action effectuer par le(s) client(s) afin
# de poursuivre le process fait par chaque client

def TraitementServeur(ip, message, csock):
    elements = message.split(",")
    # Reference de l'agence selon son adresse ip de
    ref_agence = ip[0].split(".")[3]
    log.info("Reference agence= " + ref_agence)
    if elements[0] == "ConsulterVol":
        msg = consulter_vol(elements[1])
        csock.send(bytes(msg, 'UTF-8'))
   # if elements[0] == "ConsulterHistorique": !!!!!!!!!!!!C'est exclusif à l'agence!!!!!!!!
    #    msg = afficher_historique(elements[1])
    if elements[0] == "RecevoirFacture":
        msg = consulter_facture(ref_agence)
        csock.send(bytes(msg, 'UTF-8'))
    if elements[0] == "Reservation":
        mutex.acquire()
        msg = reserver(elements[1], ref_agence, elements[2])
        mutex.release()
        csock.send(bytes(msg, 'UTF-8'))
    if elements[0] == "Annulation":
        mutex.acquire()
        msg = annuler(elements[1], ref_agence, elements[2])
        mutex.release()
        csock.send(bytes(msg, 'UTF-8'))


def launchServer():
    HOST = "192.168.1.7"
    PORT = 8084
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))

    log.info("Serveur up")
    log.info("En attente des requetes clients..")
    while True:
        # Boucle principale
        server.listen(1)
        clientsock, clientAddress = server.accept()
        # retourner le couple (socket,addresse)
        newthread = threadClients(clientAddress, clientsock)
        try:
            newthread.start()
        except e:
            log.error("Erreur du serveur: ", e)
        current_threads.append(newthread)
