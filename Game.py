while game_not_over:
    send_instructions_to_players()
    receive_actions_from_players()
    check_end_conditions()
    notify_end_of_game()
    modify_suits()

def send_infos_to_players():
    # Send game state information to players, like who needs to play, if an action is possible or not
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

def modify_suits():
    ...

def modify_player_crads():
    ...