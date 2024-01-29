import multiprocessing
import threading
import queue
import time
import json
import random
import signal
from multiprocessing import Process, Value, Array
import socket
from queue import Queue
from Player import Player

class Game:

    def __init__(self, num_players):
        self.num_players = num_players
        self.allsuits = []
        self.players = []
        self.allsemaphore = []
        for i in range(self.num_players):
            self.suits_in_construction = []
            for i in range(5):
                self.suits_in_construction.append(-1)
            self.allsuits.append(self.suits_in_construction)
        self.couleur = ["blue","red","yellow","green","white"]
        self.info_tokens = num_players + 3
        self.fuse_tokens = 3
        self.create_cards()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.discard_deck)

    def create_cards(self):
        self.discard_deck = []
        for i in range(self.num_players):
            self.discard_deck.append(0+i*5)
            self.discard_deck.append(0+i*5)
            self.discard_deck.append(0+i*5)
            self.discard_deck.append(1+i*5)
            self.discard_deck.append(1+i*5)
            self.discard_deck.append(2+i*5)
            self.discard_deck.append(2+i*5)
            self.discard_deck.append(3+i*5)
            self.discard_deck.append(3+i*5)
            self.discard_deck.append(4+i*5)
            self.shuffle()
    
    def show_deck(self):
        for i in range(0, len(self.discard_deck)):
            self.afficher_carte(self.discard_deck)
            print()

    def trad_1card(self, carte):
        if carte==-1:
            carte = "Vide"
        else:    
            carte = f"{self.couleur[carte//5]} {carte%5+1}"
        return carte
    
    def trad_card (self, cards):
        for card in cards:
            if card==-1:
                card = "Vide"
            else:    
                card = f"{self.couleur[card//5]} {card%5+1}"
        return card

    def afficher_carte(self,carte):
        carte = self.trad_1card(carte)
        if carte == "Vide":
            ligne1 = f"+-------+"
            ligne2 = f"|       |"
            ligne3 = f"|       |"
            ligne4 = f"|       |"
            ligne5 = f"+-------+"
            return [ligne1, ligne2, ligne3, ligne4, ligne5]

        largeur_carte = 7
        hauteur_carte = 5

        couleur, valeur = carte.split()
        valeur = int(valeur)

        symbole = str(valeur)

        # Créer la représentation de la carte avec des caractères ASCII standard
        ligne1 = f"+-------+"
        ligne2 = f"| {symbole:^2}    |"
        ligne3 = f"|   {couleur[:1]}   |"
        ligne4 = f"|    {symbole:^2} |"
        ligne5 = f"+-------+"

        return [ligne1, ligne2, ligne3, ligne4, ligne5]

    def afficher_cartes(self,cartes):
        for i in range(5):
            for carte in cartes:
                print(self.afficher_carte(carte)[i] + "  ", end="")
            print()

    def game_process(self):
        for i in range(self.num_players.value):
            player = Player(self, i+1)
            self.players.append(player)
        self.play()

    def handle_player(self,ID):
        while True:
            # Attendre un message du joueur
            self.msg = self.player_socket.recv(1024).decode()
            if not self.msg:
                break
            print(f"Joueur {ID} a envoyé: {self.msg}")

