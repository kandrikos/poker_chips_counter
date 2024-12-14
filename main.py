from hand import Hand
from player import Player
from table import Table
from pot import Pot

# Main function in main.py should look like this
def main(test_mode=False):
    num_players = 5
    player_names = [f"Player_{i}" for i in range(num_players)]
    initial_stack = 10000
    init_big_blind = 100
    button_position = 0

    players = [Player(name, i, initial_stack) for i, name in enumerate(player_names)]
    table = Table(players, num_seats=num_players)

    # Create new pot and hand instance
    pot = Pot()
    hand = Hand(players=players, table=table, pot=pot,
                button_position=button_position, big_blind=init_big_blind)
    
    # In test mode, just play one hand
    if test_mode:
        hand.play_hand()
        return

    # Normal game mode - continue until one player remains
    while len([player for player in players if player.game_active]) > 1:
        print("\n================================ NEW HAND ================================\n")
        hand.play_hand()
        # Update button position for next hand
        button_position = (button_position + 1) % len(players)
        
        # Create new pot and hand for next round
        pot = Pot()
        hand = Hand(players=players, table=table, pot=pot,
                   button_position=button_position, big_blind=init_big_blind)

if __name__ == "__main__":
    main()