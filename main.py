from player import Player
from hand import Hand

from random import randrange

class Table:
    def __init__(self, num_seats):
        self.num_seats = num_seats
        self.seating = {}  # Dictionary to map seat numbers to players

    def assign_seat(self, player, seat_number):
        if 1 <= seat_number <= self.num_seats and seat_number not in self.seating:
            self.seating[seat_number] = player
        else:
            raise ValueError("Invalid seat number or seat already taken")

    def rotate_button(self):
        """Rotates the button (dealer) position clockwise."""
        # Find the current button
        button_seat = next((seat for seat, player in self.seating.items() if player.position == "Button"), None)
        if button_seat is None:
            raise ValueError("Button not found")

        # Calculate the new button seat (clockwise rotation)
        new_button_seat = (button_seat % self.num_seats) + 1

        # Update player positions based on the new button
        for seat, player in self.seating.items():
            relative_position = (seat - new_button_seat) % self.num_seats
            if relative_position == 0:
                player.position = "Button"
            elif relative_position == 1:
                player.position = "SB"
            elif relative_position == 2:
                player.position = "BB"
            else:
                player.position = relative_position + 1  # Adjust for 1-based indexing


def play_simple_hand():
    """Plays a simplified hand of poker."""
    initial_stack = 1000
    initial_bb = 20

    players = [
        Player(name="A", rel_position=None, stack=initial_stack),
        Player(name="B", rel_position=None, stack=initial_stack),
        Player(name="C", rel_position=None, stack=initial_stack),
        Player(name="D", rel_position=None, stack=initial_stack),
        Player(name="E", rel_position=None, stack=initial_stack),
        Player(name="F", rel_position=None, stack=initial_stack)
        ]

    # assign seats to players (or ask user for players/seats)
    # seats = {
    #     f"seat_{i}": players[i] if players[i].game_active else None
    #     for i in range(6)
    # }

    seats = {
        "seat_0": players[0],    
        "seat_1": players[1],
        "seat_2": players[2],
        "seat_3": players[3],
        "seat_4": players[4],    
        "seat_5": players[5]
    }

    
    # randomly select first dealer-seat of the game and play the first hand
    first_btn_seat = randrange(len(players))
    first_btn_player = seats.get(f"seat_{first_btn_seat}")
    first_btn_player.rel_position = 0 # assign relative position to 0 for dealer player
    nums = [i for i in range(1, len(seats))]

    seats[f'seat_{(first_btn_seat + min(nums)) % len(seats)}'].rel_position = min(nums)
    nums.pop(0)
    seats[f'seat_{(first_btn_seat + min(nums)) % len(seats)}'].rel_position = min(nums)
    nums.pop(0)
    seats[f'seat_{(first_btn_seat + min(nums)) % len(seats)}'].rel_position = min(nums)
    nums.pop(0)
    seats[f'seat_{(first_btn_seat + min(nums)) % len(seats)}'].rel_position = min(nums)
    nums.pop(0)
    seats[f'seat_{(first_btn_seat + min(nums)) % len(seats)}'].rel_position = min(nums)
    nums.pop(0)



    
    for i in range(1, len(players)):
        player = seats[f'seat_{(first_btn_seat + i) % len(seats)}']
        if player != None:
            player.rel_position = i # assign relative positions to players after the dealer
        else:
            pass # TODO: handle the case where a player in None (eliminated).
                 # The way it is written now, if a player == None
                 # the next position will not be assigned to any player. 
                 # e.g. 
                 # seat_2 player.rel_position = 0 --> dealer
                 # AND seat_3 player = None:  
                 # seat_4 player will be assigned with rel_position 2 instead of 1


    first_hand = Hand(
        active_players=players, 
        btn_player=first_btn_player, 
        big_blind=initial_bb)
    
    first_hand.play_preflop()
    first_hand.play_streets()

    active_players = [pl for pl in players if pl.game_active == True] # get active players

    

    # continue with the next hands and all active players
    hand_num = 0
    while len(active_players) > 1:
        # update `seats` dict (remove non-active players)
        for key in seats.keys():
            if seats[key].game_active == False:
                seats[key] = None

        active_players_num = len([i for i in seats.keys() if seats[i] != None])
        btn_seat = f"seat_{(first_btn_seat + hand_num + 1) % active_players_num}" # button rotation
        btn_player = seats.get(btn_seat)
        hand = Hand(active_players, btn_player)

        hand.play_preflop()
        hand.play_streets()

        active_players = [pl for pl in players if pl.game_active == True] # get active players

if __name__ == "__main__":
    play_simple_hand()
