import multiprocessing
import threading
import queue
import time
import json
import random
import signal
import threading
import socket
from multiprocessing import Process, Manager, Semaphore
from queue import Queue

class Player:
    
    def __init__(self, game, ID, queue, lock, port, hand):
        super(Player, self).__init__()
        self.ID = ID
        self.game = game
        self.def_indice()
        self.hand_Player=hand
        self.queue=queue
        self.lock=lock
        self.port=port


    def def_indice(self):
        self.hand_indice = []
        self.indice = []
        for i in range(5):
            self.hand_indice.append(self.hand_Player[i])
            self.indice.append([False,False])

    def show_my_indices(self, carte, i):
        carte = self.game.trad_1card(carte)
        if carte == "Vide":
            ligne1 = f"+-------+"
            ligne2 = f"|       |"
            ligne3 = f"|       |"
            ligne4 = f"|       |"
            ligne5 = f"+-------+"
            return [ligne1, ligne2, ligne3, ligne4, ligne5]

        largeur_carte = 7
        hauteur_carte = 5
        valeur = "-1"
        couleur = "blue"
        symbole = "J"
        if self.indice[i][0] == True and self.indice[i][1] == True:
            couleur, valeur = carte.split()
            valeur = int(valeur)
            symbole = str(valeur) if valeur <= 10 else {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(valeur, '')
        elif self.indice[i][0] == False and self.indice[i][1] == True:
            couleur, valeur = carte.split()
            valeur = int(valeur)
            symbole = str(valeur) if valeur <= 10 else {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(valeur, '')
            couleur = "?"
        elif self.indice[i][0] == True and self.indice[i][1] == False:
            couleur, valeur = carte.split()
            valeur = "?"
            symbole = "?"
        elif self.indice[i][0] == False and self.indice[i][1] == False:
            couleur, valeur = carte.split()
            valeur = "?"  
            symbole = "?"   
            couleur = "?"


        # Créer la représentation de la carte avec des caractères ASCII standard
        ligne1 = f"+-------+"
        ligne2 = f"| {symbole:^2}    |"
        ligne3 = f"|   {couleur[:1]}   |"
        ligne4 = f"|    {symbole:^2} |"
        ligne5 = f"+-------+"

        return [ligne1, ligne2, ligne3, ligne4, ligne5]

    def show_my_indice(self, cartes):
        print(f"Indice Joueur {self.ID}\n")
        for i in range(len(cartes)):
            for j in range(5):
                print(self.show_my_indices(cartes[i], i)[j]+ "  ", end="")
                print()
    
    def show_suits(self):
        print(f"Indice Joueur {self.ID}\n")
        for j in range(len(self.game.allsuits)):
            if j == 0:
                print("Pile blue\n")
            elif j == 1:
                print("Pile red\n")  
            elif j == 2:
                print("Pile Yellow\n")
            elif j == 3:
                print("Pile Green\n")  
            elif j == 4:
                print("Pile White\n")
            elif j == 5:
                print("Pile Pink\n")
            for i in range(0, len(self.game.suits_in_construction), 5):
                self.game.afficher_cartes(self.game.allsuits[j][i:i+5])
                print()

    def show_cartes(self):
        for joueur in self.game.players:
            if joueur != self:
                print(f"Joueur {joueur.ID}\n")
                for i in range(0, len(joueur.hand_Player), 5):
                    self.game.afficher_cartes(joueur.hand_Player)
                    print()

    def get_couleur_carte(self, carte):
        card = self.game.trad_1card(carte)
        couleur, valeur = card.split()
        return couleur
    
    def get_valeur_carte(self, carte):
        card = self.game.trad_1card(carte)
        couleur, valeur = card.split()
        return valeur
    
    def add_to_suits(self,suits,nb_carte):
        nb_carte=nb_carte-1
        if self.get_couleur_carte(self.hand_Player[nb_carte]) == suits:
            for i in range(5):
                if int(self.game.allsuits[self.get_suits_color_number(suits)][0]) == -1 and int(self.get_valeur_carte(self.hand_Player[nb_carte])) == 1:
                    reponse = f"{self.ID} cartes {suits} {nb_carte}"
                    self.tcp_socket.send(reponse.encode())
                    return True
                elif int(self.game.allsuits[self.get_suits_color_number(suits)][i]) == -1 and int(self.game.allsuits[self.get_suits_color_number(suits)][i]) == int(self.game.allsuits[self.get_suits_color_number(suits)][i-1])+1:
                    reponse = f"{self.ID} cartes {suits} {nb_carte}"
                    self.tcp_socket.send(reponse.encode())
                    return True
                elif i==4 and int(self.game.allsuits[self.get_suits_color_number(suits)][i]) != -1:
                    reponse = f"{self.ID} discard {suits} {nb_carte}"
                    self.tcp_socket.send(reponse.encode())
                    return False       
        elif self.get_couleur_carte(self.hand_Player[nb_carte]) != suits:
            reponse = reponse = f"{self.ID} discard {suits} {nb_carte}"
            self.tcp_socket.send(reponse.encode())
            return False

    def obtenir_choix(self,mots_autorises):
        while True:
            choix_utilisateur = str(input("Veuillez faire votre choix: ").lower())  # .lower() pour rendre l'entrée insensible à la casse
            if choix_utilisateur in mots_autorises:
                return choix_utilisateur
            else:
                print("Choix invalide")

    def choix_cartes(self):
        print("Quel cartes voulez vous envoyer? Faites votre choix en tappant le numéro de la carte\n")
        mots_autorises= [str(i) for i in range(1,6,1)]
        num_card = int(self.obtenir_choix(mots_autorises))
        print(f"Dans quelle pile voulez vous l'envoyer?\n")
        for i in range (self.game.num_players):
                print(f"{self.game.couleur[i]}")
        print("\n")
        mots_autorises = self.game.couleur
        pile = self.obtenir_choix(mots_autorises)
        print(f"Vous avez envoyé votre carte\n")
        reponse = self.add_to_suits(pile, num_card)
        if reponse == True:
            print("Vous avez réussi à poser votre carte dans la bonne pile\n")
        elif reponse == False:
            print(f"Vous avez raté. Vous perdez un fuse token. Il vous en reste {self.game.fuse_tokens}\n")
        print("Vous avez pioché une nouvelle carte")
        print("Fin de votre tour")

    def choix_info(self):
        print("Avec qui voulez communiquer? Faites votre choix en tappant le numéro du joueur :\n")
        mots_autorises = [str(i) for i in range(1, len(self.game.players)+1) if i != self.ID]
        joueur = self.obtenir_choix(mots_autorises)
        print(f"Que voulez vous dire au Joueur {joueur}?\nCouleur ou Chiffre?")
        mots_autorises = ["couleur","chiffre"]
        choix=self.obtenir_choix(mots_autorises)
        if choix == "couleur":
            print(f"Quel couleur?\n")
            for i in range (self.game.num_players):
                print(f"{self.game.couleur[i]}")
            print("\n")
            mots_autorises=self.game.couleur
            choix=self.obtenir_choix(mots_autorises)[0]
            self.send_message(f"{joueur}{choix}")
            reponse = "info"
            self.tcp_socket.send(reponse.encode())
            print(f"\nL'information a bien été envoyé\n")
        if choix=="chiffre":
            print("Quel chiffre entre 1 et 5?")
            mots_autorises = [str(i) for i in range(1,6,1)]
            choix =self.obtenir_choix(mots_autorises)
            self.send_message(f"{joueur}{choix}")
            print(f"\nL'information a bien été envoyé\n")

    def choix_indice(self):
        self.show_my_indice(self.hand_indice)
        print("Vous pouvez maintenant choisir entre 3 actions: Information, Cartes ou Suits \n")
        mots_autorises = ["information","cartes","suits"]
        choix = self.obtenir_choix(mots_autorises)
        return choix
    
    def choix_suits(self):
        self.show_suits()
        print("Vous pouvez maintenant choisir entre 3 actions: Information, Cartes ou Indice\n")
        mots_autorises = ["information","cartes","indice"]
        choix = self.obtenir_choix(mots_autorises)
        return choix

    def action(self):
        self.set_indice_and_reload()
        print(self.indice)
        print(f"Vous etes le Joueur {self.ID}\n")
        print("Voici les cartes des autres Joueurs:\n")
        self.show_cartes()
        print("Vous pouvez maintenant choisir entre 4 actions: Information, Cartes, Indice ou Suits\n")
        mots_autorises = ["information","cartes","indice","suits"]
        choix = self.obtenir_choix(mots_autorises)
        if choix == "information":
            self.choix_info()
        if choix == "cartes":
           self.choix_cartes()
        if choix == "indice":
            choix=self.choix_indice()
            if choix == "information":
                self.choix_info()
            if choix == "cartes":
                self.choix_cartes()
            if choix == "suits":
                choix = self.choix_suits()
                if choix == "information":
                    self.choix_info()
                if choix == "cartes":
                    self.choix_cartes()
        if choix == "suits":
            choix=self.choix_suits()
            if choix == "information":
                self.choix_info()
            if choix == "cartes":
                self.choix_cartes
            if choix == "indice":
                choix = self.choix_indice()
                if choix == "information":
                    self.choix_info()
                if choix == "cartes":
                    self.choix_cartes()
    
    def game_start(self) :
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(("localhost", self.port))
        while True :
            self.lock.acquire()
            self.action()

    def send_message(self,msg):
        self.queue.put(msg)   

    def get_all_msg(self):
        message = []
        while not self.queue.empty():
            message = self.queue.get()
        return message
    
    def set_indice_and_reload(self):
        copie_queue = list(self.get_all_msg())
        print(copie_queue)
        for i in range (0,len(copie_queue),2):
            ID=int(copie_queue[i])
            info=copie_queue[i+1]
            if ID == self.ID:
                if info=='1' or info=='2' or info=='3' or info=='4' or info=='5':
                    for i in range(len(self.hand_Player)):
                        if int(self.get_valeur_carte(self.hand_Player[i]))==int(info):
                            self.indice[i][1] = True
                else:
                    for i in range(len(self.hand_Player)):
                        if self.get_couleur_carte(self.hand_Player[i])[0]==info:
                            self.indice[i][0] = True
            else:
                self.queue.put(copie_queue[i])
                self.queue.put(copie_queue[i+1])