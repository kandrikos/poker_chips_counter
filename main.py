# from player import Player
# from hand import Hand
# from table import Table


# def start_game():

#     ####################################################################
#     ########################## RUNS ONLY ONCE ##########################

#     initial_stack = 10000
#     initial_bb = 100

#     num_players = 5
#     players = []
#     for i  in range(num_players):
#         players.append(Player(f"Player_{i}", rel_position=None, stack=initial_stack))


#     table = Table(players)

#     first_btn_seat = 0
#     first_btn_player = table.get_player_at_seat(f"seat_{first_btn_seat}")
#     first_btn_player.rel_position = 0
#     nums = [i for i in range(1, num_players)]

#     print("=" * 40)
#     print(f"Starting Stack: {initial_stack}")
#     print(f"Initial BB: {initial_bb}")
#     print("=" * 40)
#     for s, p in table.seats.items():
#         print(f"{s} --> {p.name}")
#     print("=" * 40)
#     print(f"First button  player: {first_btn_player.name}")

#     # assign relative positions to players after the dealer
#     for i in range(1, len(players)):
#         player = table.get_player_at_seat(f'seat_{(first_btn_seat + i) % len(table.seats)}')
#         if player is not None:
#             player.rel_position = min(nums)
#             nums.pop(0)

#     first_hand = Hand(
#         players=players, 
#         btn_player=first_btn_player, 
#         big_blind=initial_bb)
    
#     first_hand.play_hand(test_actions=["no_raise"])

#     ####################################################################
#     ####################################################################

#     active_players = [p for p in players if p.game_active] 
#     while len(active_players) > 1:
#         hand = Hand(
#             players=active_players, 
#             btn_player=first_btn_player, 
#             big_blind=initial_bb)
        
#         hand.play_hand()
#         active_players = [p for p in players if p.game_active]

# if __name__ == "__main__":
#     start_game()

from hand import Hand
from player import Player
from table import Table
from pot import Pot

def main():
    num_players = 5
    player_names = [f"Player_{i}" for i in range(num_players)]
    initial_stack = 10000
    init_big_blind = 100
    init_btn_position = 0

    players = [Player(name, i, initial_stack) for i, name in enumerate(player_names)]
    table = Table(players, num_seats=num_players)
    pot = Pot()

    hand = Hand(players=players, table=table, pot=pot, 
                button_position=init_btn_position, big_blind=init_big_blind)

    while len([player for player in players if player.game_active]) > 1:
        print("\n--- Starting New Hand ---\n")
        hand.play_hand()

if __name__ == "__main__":
    main()

