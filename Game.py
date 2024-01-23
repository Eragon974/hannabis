while game_not_over:
    update_game()
    send_instructions_to_players()
    receive_actions_from_players()
    check_end_conditions()
    notify_end_of_game()

def update_game():
    # Update deck, suits in construction, tell which player needs to play etc.
    ...

def send_instructions_to_players():
    # Send game state information to players
    ...

def receive_actions_from_players():
    # Receive actions from players via sockets
    ...

def check_end_conditions():
    # Check if the game is over based on conditions
    ...

def notify_end_of_game():
    # Send signals to players for game win or loss
    ...
