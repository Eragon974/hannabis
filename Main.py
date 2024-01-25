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
        self.num_players = num_players
        info_tokens = Value('d',num_players + 3)
        fuse_tokens = Value('d',3)
        self.end_of_game = multiprocessing.Event()

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
        self.hand = self.generate_initial_hand()

    def generate_initial_hand(self):
        # Generate initial hand for the player
        return [random.randint(1, 5) for _ in range(5)]
    
    def run(self):
        while not self.game.end_of_game.is_set():
            self.update_hand_information()
            self.display_game_state()
            self.send_actions_to_game()
            self.receive_updates_from_game()

        def give_information(self, player_id):
            choice = input("Voulez-vous donner une information sur une couleur ou un chiffre ? c/n")
            while check_response:
                if choice == "c":
                    color = input("Sur quelle couleur voulez-vous donner une information ?")
                    print(f"Vous choisissez de donner une information sur la couleur : {color}")

                elif choice == "n":
                    check_number=False
                    while not check_number:
                        number = input("Sur quelle chiffre (entre 1 et 5) voulez-vous donner une information ?")
                        if number in ["1","2","3","4","5"]:
                            print(f"Vous choisissez de donner une information sur le chiffre : {number}")
                            check_number=True
                        else:
                            print("Vous devez choisir un chiffre entre 1 et 5")
                else:
                    check_response=False
                    print("Vous devez choisir entre une couleur et un chiffre")

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