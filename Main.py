import multiprocessing
import threading
import queue
import time
import json
import random
import signal
from multiprocessing import Process, Value, Array




class Game:
    def __init__(self, num_players):
        self.num_players = Value('i', num_players)
        self.info_tokens = Value('i', num_players + 3)
        self.fuse_tokens = Value('i',3)
        self.end_of_game = multiprocessing.Event()
        self.create_cards()
        
    def Player_hand(self):
        for i in range(num_players):
            self.players = []
            self.hand_Player = Array('i', [0]*5)
            for k in range(5):
                self.hand_Player[k]=self.discard_deck[0]
                for j in range(1,len(self.discard_deck),1): 
                    self.discard_deck[j-1]=self.discard_deck[j]
                if j==(len(self.discard_deck)-1):
                        self.discard_deck[j]=-1
            self.players.append(self.hand_Player)

    def shuffle(self, Array):
        random.shuffle(Array)  

    def create_cards(self):
        self.discard_deck = Array('i', [0]*(10*self.num_players.value))
        for i in range (self.num_players.value):
            self.discard_deck[i*10]=0+i*5
            self.discard_deck[i*10+1]=0+i*5
            self.discard_deck[i*10+2]=0+i*5
            self.discard_deck[i*10+3]=1+i*5
            self.discard_deck[i*10+4]=1+i*5
            self.discard_deck[i*10+5]=2+i*5
            self.discard_deck[i*10+6]=2+i*5
            self.discard_deck[i*10+7]=3+i*5
            self.discard_deck[i*10+8]=3+i*5
            self.discard_deck[i*10+9]=4+i*5
            self.shuffle(self.discard_deck)
            

    def trad_card (self, Array):
        couleur = ["blue","red","yellow","black","white","pink"]
        card=list(Array)    
        for i in range (len(card)):
            if card[i]==-1:
                card[i] = "Vide"
            else:    
                card[i] = f"{couleur[card[i]//5]} {card[i]%5+1}"
        return card

    def start(self):
        self.shuffle(self.discard_deck)
        self.Player_hand()
    
        for _ in range(self.num_players):
            player = Player(self, self.message_queue)
            players.append(player)
            for i in range(5):
                self.hand
            player.start()

        self.play()
        for player in players:
            player.join()
        
    def play(self):
        # Game logic goes here
        pass

    def end_game(self, result):
        self.end_of_game.set()
        self.message_queue.put({"type": "end_game", "result": result})

class Player(threading.Thread):
    def __init__(self, game, message_queue):
        super(Player, self).__init__()
        self.game = game
        self.message_queue = message_queue

    def run(self):
        while not self.game.end_of_game.is_set():
            self.update_hand_information()
            self.display_game_state()
            self.send_actions_to_game()
            self.receive_updates_from_game()

    def update_hand_information(self):
        # Update information about the player's hand
        pass

    def display_game_state(self):
        # Display the current state of the game
        pass

    def send_actions_to_game(self):
        action = self.get_player_action()
        self.message_queue.put({"type": "player_action", "player_id": id(self), "action": action})

    def receive_updates_from_game(self):
        try:
            message = self.message_queue.get(timeout=1)
            if message["type"] == "end_game":
                self.game.end_game(message["result"])
        except queue.Empty:
            pass

    def get_player_action(self):
        # Get player's action, either giving information or playing a card
        # Return the action in a structured format (e.g., {"action_type": "information", "info": {...}})
        pass

if __name__ == "__main__":
    num_players = 3
    game = Game(num_players)
    cartes = game.trad_card(game.discard_deck)
    for i in cartes:
        print(i)
    
    #game_process = multiprocessing.Process(target=game.start)
    #game_process.start()

    #Wait for the game to finish
    #game_process.join()