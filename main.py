from player import Player
from hand import Hand
from table import Table


def start_game():

    ####################################################################
    ########################## RUNS ONLY ONCE ##########################

    initial_stack = 10000
    initial_bb = 100

    num_players = 5
    players = []
    for i  in range(num_players):
        players.append(Player(f"Player_{i}", rel_position=None, stack=initial_stack))


    table = Table(players)

    first_btn_seat = 0
    first_btn_player = table.get_player_at_seat(f"seat_{first_btn_seat}")
    first_btn_player.rel_position = 0
    nums = [i for i in range(1, num_players)]

    print("=" * 40)
    print(f"Starting Stack: {initial_stack}")
    print(f"Initial BB: {initial_bb}")
    print("=" * 40)
    for s, p in table.seats.items():
        print(f"{s} --> {p.name}")
    print("=" * 40)
    print(f"First button  player: {first_btn_player.name}")

    # assign relative positions to players after the dealer
    for i in range(1, len(players)):
        player = table.get_player_at_seat(f'seat_{(first_btn_seat + i) % len(table.seats)}')
        if player is not None:
            player.rel_position = min(nums)
            nums.pop(0)

    first_hand = Hand(
        players=players, 
        btn_player=first_btn_player, 
        big_blind=initial_bb)
    
    first_hand.play_hand(test_actions=["no_raise"])

    ####################################################################
    ####################################################################

    active_players = [p for p in players if p.game_active] 
    while len(active_players) > 1:
        hand = Hand(
            players=active_players, 
            btn_player=first_btn_player, 
            big_blind=initial_bb)
        
        hand.play_hand()
        active_players = [p for p in players if p.game_active]


    



    # # continue with the next hands and all active players
    # hand_num = 0
    # while len(active_players) > 1:
    #     # update `seats` dict (remove non-active players)
    #     for key in list(table.seats.keys()):
    #         if table.get_player_at_seat(key) is not None and not table.get_player_at_seat(key).game_active:
    #             table.remove_player_from_seat(key)

    #     active_players_num = len([i for i in table.seats.values() if i is not None])
    #     btn_seat = f"seat_{(first_btn_seat + hand_num + 1) % active_players_num}"  # button rotation
    #     btn_player = table.get_player_at_seat(btn_seat)
    #     hand = Hand(active_players, btn_player)

    #     hand.play_preflop()
    #     hand.play_streets()

    #     active_players = table.get_active_players()  # get active players

if __name__ == "__main__":
    start_game()
