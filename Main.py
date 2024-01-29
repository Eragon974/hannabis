from Game import Game
from Player import Player
from multiprocessing import Process
import threading
from queue import Queue

def main():
    num_players = int(input("Nombre de joueur?\n"))
    game=Game(num_players)
    #pg = Process(target=game.game_process, args=())
    queue=Queue()
    for i in range(game.num_players):
        player = Player(game, i+1, queue)
        game.players.append(player)
        #pp = threading.Thread(target=player.player_process, args=())
        #game.allsemaphore.append()
        #pp.start()
    #pg.start()
    #for player in game.allPlayers:
        #pp.join()
    while game.fuse_tokens!=0:
        for player in game.players:
            player.action()
    
if __name__ == "__main__":
    main()