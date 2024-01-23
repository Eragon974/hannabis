while game_not_over:
    show_game()
    receive_updates_from_game()
    play_card()
    send_info_to_player()
    show_your_info()
    send_updates_to_game()

def play_card():
    # Update information about the player's hand
    ...

def show_game():
    # Display the current state of the game, which means the others players hand via messages queues and/or suits that are constructing in the game via sockets
    ...

def send_info_to_player():
    # Send informations to others players about what they have
    ...

def show_your_info():
    #look at info that a player got in the past
    ...

def receive_updates_from_game():
    # Receive updates from the game process via sockets, like modified suits or if it is your turn to play or not
    ...

def send_updates_to_game():
    # Send updates if you have finished your turn and if you played a card or not
    ...
