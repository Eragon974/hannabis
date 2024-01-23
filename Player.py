while game_not_over:
    update_hand_info()
    show_game_state()
    send_card_to_game()
    receive_updates_from_game()
    send_info_to_player()

def update_hand_info(player_card[], i):
    # Update information about the player's hand
    ...

def show_game_state():
    # Display the current state of the game
    ...

def send_card_to_game():
    # Send actions to the game process via sockets
    ...

def receive_updates_from_game():
    # Receive updates from the game process via sockets
    ...

def send_info_to_player():
    # Send informations to others players via messages queues
    ...
