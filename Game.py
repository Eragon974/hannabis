import multiprocessing
import threading
import queue
import time
import json
import random
import signal
from multiprocessing import Process, Manager,Semaphore
import socket
from queue import Queue
from Player import Player

class Game:
    def __init__(self, num_players, port):
        self.num_players = num_players
        self.allsuits = []
        self.players = []
        self.allSemaphore = []
        self.endpile=[False]*num_players
        for i in range(self.num_players):
            self.suits_in_construction = []
            for i in range(5):
                self.suits_in_construction.append(-1)
            self.allsuits.append(self.suits_in_construction)
        self.couleur = ["blue","red","yellow","green","white"]
        self.info_tokens = num_players + 3
        self.fuse_tokens = 3
        self.tokens=[self.info_tokens, self.fuse_tokens]
        self.port = port
        self.nb_tour = 0
        self.HOST = 'localhost'
        self.create_cards()
        self.discard_deck = []
        self.Player_hand()
        
    def shuffle(self):
        random.shuffle(self.deck)

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
        placed=False
        if message[1]== "info":
            self.tokens[0]-=1
        if message[1] == "cartes":
            i=int(message[0])
            j=int(message[3])
            k=0
            while placed == False:
                if self.allsuits[self.get_suits_color_number(message[2])][k]== -1:
                    self.allsuits[self.get_suits_color_number(message[2])][k] = (self.allhand[i-1])[j]
                    placed=True
                k+=1
            self.discard_deck.append((self.allhand[i-1])[j])
            self.draw(j,self.players[i-1])
        if message[1] == "discard":
            i=int(message[0])
            j=int(message[3])
            self.tokens[1]-=1
            self.discard_deck.append(self.players[i-1].hand_Player[j])
            self.draw(j,self.players[i-1])

    def get_socket_message(self,client_socket,lock,my_lock):
        with client_socket:
            while True :
                my_lock.acquire()
                data = client_socket.recv(1024).decode()
                self.buffer = data
                time.sleep(3)
                lock.release()

    def Player_hand(self):
        self.allhand = []
        for _ in range (self.num_players):
            hand = []
            for _ in range(5):
                hand.append(self.deck[0])
                for j in range(1,len(self.deck),1): 
                    self.deck[j-1]=self.deck[j]
                    if j==(len(self.deck)-1):
                        self.deck[j]=-1
            self.allhand.append(hand)        

    def create_players_lock(self) :
        queue=Queue()
        self.locks = []
        for i in range(self.num_players):
            self.locks.append(Semaphore(0))
            self.players.append(Player(i+1,queue,self.locks[i],self.port,self.allhand[i],self.allsuits,self.players,self.couleur,self.tokens))   

    def is_finished(self) :
        end = False
        won = False  
        for i in range(len(self.allsuits)):
            if 4+i*5 in self.allsuits[i]:
                self.endpile[i]==True
        if all(self.endpile):
            won=True
            end=True
        elif self.tokens[1] < 1:
            end = True
        else :
            for i in range(5):
                if 4+i*5 in self.discard_deck:
                    end=True
            
        return end,won
    
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
                t = threading.Thread(target=self.players[i].game_start)
                t.start()
                allplayer_threads.append(t)    
            alltcp_process=[]
            for i in range(self.num_players) :
                conn, addr = server_socket.accept()
                t = threading.Thread(target=self.get_socket_message, args=(conn,self.game_lock,self.buffer_locks[i]))
                t.start()
                alltcp_process.append(t)
            end,won = self.is_finished()

            while end == False :
                #print("\033c")
                print("Début du tour")
                self.nb_tour += 1
                self.buffer_locks[(self.nb_tour-1)%self.num_players].release()
                self.locks[(self.nb_tour-1)%self.num_players].release()
                self.game_lock.acquire()
                self.logic_buffer()
                end, won = self.is_finished()
            if won:
                print("Vous avez gagnez")
            else :
                print("Vous avez perdu")

if __name__ == "__main__" :
    num_players = int(input("Nombre de joueurs :\n"))
    port = int(input("Port > 6000\n"))
    game = Game(num_players,port)
    game.start()