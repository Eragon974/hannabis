import multiprocessing
import threading
import queue
import time
import json
import random
import signal
from multiprocessing import Process, Manager, Semaphore
import socket
from queue import Queue
from Player import Player

class Game:
    def __init__(self, num_players, port):
        self.num_players = num_players
        self.allsuits = []
        self.players = []
        self.allSemaphore = []
        self.allClient = []
        for i in range(self.num_players):
            self.suits_in_construction = []
            for i in range(5):
                self.suits_in_construction.append(-1)
            self.allsuits.append(self.suits_in_construction)
        self.couleur = ["blue","red","yellow","green","white"]
        self.info_tokens = num_players + 3
        self.fuse_tokens = 3
        self.port = port
        self.nb_tour = 0
        self.create_cards()
        self.shuffle()
        self.discard_deck = []

    def shuffle(self):
        random.shuffle(self.discard_deck)

    def create_cards(self):
        self.deck = []
        for i in range(self.num_players):
            self.deck.append(0+i*5)
            self.deck.append(0+i*5)
            self.deck.append(0+i*5)
            self.deck.append(1+i*5)
            self.deck.append(1+i*5)
            self.deck.append(2+i*5)
            self.deck.append(2+i*5)
            self.deck.append(3+i*5)
            self.deck.append(3+i*5)
            self.deck.append(4+i*5)
            self.shuffle()


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

    def get_suits_color_number(self,color):
        if color == "blue":
            return 0
        elif color == "red":
            return 1
        elif color == "yellow":
            return 2
        elif color == "purple":
            return 3
        elif color == "white":
            return 4
        elif color == "pink":
            return 5 
        
    def draw(self,nb,player):
        player.hand_Player[nb]=self.deck[0]
        for i in range(1,len(self.deck),1): 
            self.deck[i-1]=self.deck[i]
        if i==(len(self.deck)-1):
                self.deck[i]=-1

    def logic_buffer(self):
        message = self.buffer.split(" ")
        self.buffer=""
        if message[1]== "info":
            self.info_tokens-=1
        if message[1]== "cartes":
            self.allsuits[self.get_suits_color_number(message[3])][0] = (self.allhand[message[0]-1])[message[4]]
            self.discard_deck.append((self.allhand[message[0]-1])[message[4]])
            self.draw(message[4],self.allhand[message[0]-1])
        if message[1] == "discard":
            self.fuse_tokens-=1
            self.discard_deck.append(self.players[message[0]-1].hand_Player[message[4]])
            self.draw(message[4],self.players[message[0]-1])

    def get_socket_message(self,client_socket,lock,my_lock):
        with self.client_socket:
            while True :
                my_lock.acquire()
                data = client_socket.recv(1024).decode()
                self.buffer += data
                lock.release()

    def Player_hand(self):
        self.allhand = []
        for _ in range(5):
            hand = []
            hand.append(self.deck[0])
            for j in range(1,len(self.deck),1): 
                self.deck[j-1]=self.deck[j]
            if j==(len(self.deck)-1):
                    self.deck[j]=-1
            self.allhand.append(hand)        

    def create_players_lock(self) :
        self.Player_hand()
        queue=Queue()
        self.locks = []
        for i in range(self.num_players):
            self.locks.append(Semaphore(0))
            self.players.append(Player(self,i+1,queue,self.locks[i],self.port,self.allhand[i]))   

    def is_finished(self) :
        won = True
        lost = False
        for suite in self.suites :
            if len(suite) != 5 :
                won = False     
        if self.fuse == 0 :
            lost = True
        else :
            if 5 in self.discard_pile :
                lost = True
                
        return won,lost
    
    def start(self):
        self.create_players_lock()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.HOST, self.port))
            server_socket.listen(self.num_players)
            self.game_lock = Semaphore(0)   
            self.buffer_locks = []
            for _ in range(self.num_players) :
                self.buffer_locks.append(Semaphore(0))
            self.buffer = "" 
            allplayer_threads = []     
            for i in range(self.num_players) :
                t = threading.Thread(target=self.players[i].game_start())
                t.start()
                allplayer_threads.append(t)
            alltcp_process=[]
            for i in range(self.num_players) :
                conn, addr = server_socket.accept()
                t = Process(target=self.get_socket_message, args=(conn, self.game_lock,self.buffer_locks[i],self.port))
                t.start()
                alltcp_process.append(t)
            end,fin = self.is_finished()

            while not won and not lost :
                print("Début du tour")
                self.nb_tour += 1
                self.buffer_locks[(self.nb_tour-1)%self.num_players].release()
                self.locks[(self.nb_tour-1)%self.num_players].release()
                self.game_lock.acquire()
                self.logic_buffer()
                won,lost = self.is_finished()
            if won:
                print("Vous avez gagnez")
            else :
                print("Vous avez perdu")


if __name__ == "__main__" :
    num_players = int(input("Nombre de joueurs :\n"))
    port = int(input("Port > 6000"))
    game = Game(num_players,6000)
    game.start()


