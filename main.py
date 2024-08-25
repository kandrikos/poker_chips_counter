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
        

class Seats:
    def __init__(self, players):
        self.seats = {f"seat_{i}": player for i, player in enumerate(players)}

    def get_player_at_seat(self, seat):
        return self.seats.get(seat)

    def assign_player_to_seat(self, seat, player):
        self.seats[seat] = player

    def remove_player_from_seat(self, seat):
        self.seats[seat] = None

    def get_active_players(self):
        return [player for player in self.seats.values() if player is not None]
    


def play_simple_hand():
    """Plays a simplified hand of poker."""

    ####################################################################
    ########################## RUNS ONLY ONCE ##########################

    initial_stack = 1000
    initial_bb = 20
 
    # num_players = int(input("Enter the number of players: "))
    # players = []
    # for i in range(num_players):
    #     player_name = input(f"Enter the name of the player to sit in seat_{i}: ")
    #     player = Player(player_name,  rel_position=None, stack=initial_stack)
    #     players.append(player)

    num_players = 9
    players = []
    for i  in range(num_players):
        players.append(Player(f"Player_{i}", rel_position=None, stack=initial_stack))


    seats = Seats(players)
    
    # # randomly select first dealer-seat of the game and play the first hand
    # first_btn_seat = int(input(f"Enter the number of seat to have the first dealer button (0 - {num_players}): ")) # randrange(len(players))
    # first_btn_player = seats.get_player_at_seat(f"seat_{first_btn_seat}") # seats.get(f"seat_{first_btn_seat}")
    # first_btn_player.rel_position = 0 # assign relative position to 0 for dealer player
    # nums = [i for i in range(1, len(seats.seats))]

    first_btn_seat = 4
    first_btn_player = seats.get_player_at_seat(f"seat_{first_btn_seat}")
    first_btn_player.rel_position = 0
    nums = [i for i in range(1, num_players)]


    print(f"Initial BB: {initial_bb}\n")
    print(f"Starting Stack: {initial_stack}\n")
    print(f"Players: \n{[player.name for player in players]}\n")
    print(f"First btn  player: {first_btn_player.name}\n")
    print(f"Seats: \n {seats.seats.keys()}")
    print(f"Players: \n {[v.name for v in seats.seats.values()]}")

    # assign relative positions to players after the dealer
    for i in range(1, len(players)):
        player = seats.get_player_at_seat(f'seat_{(first_btn_seat + i) % len(seats.seats)}')
        if player is not None:
            player.rel_position = min(nums)
            nums.pop(0)

    first_hand = Hand(
        active_players=players, 
        btn_player=first_btn_player, 
        big_blind=initial_bb)
    
    first_hand.play_preflop()
    first_hand.play_streets()

    
    active_players = [pl for pl in players if pl.game_active == True] # get active players
    
    
    ####################################################################
    ####################################################################


    # continue with the next hands and all active players
    hand_num = 0
    while len(active_players) > 1:
        # update `seats` dict (remove non-active players)
        for key in list(seats.seats.keys()):
            if seats.get_player_at_seat(key) is not None and not seats.get_player_at_seat(key).game_active:
                seats.remove_player_from_seat(key)

        active_players_num = len([i for i in seats.seats.values() if i is not None])
        btn_seat = f"seat_{(first_btn_seat + hand_num + 1) % active_players_num}"  # button rotation
        btn_player = seats.get_player_at_seat(btn_seat)
        hand = Hand(active_players, btn_player)

        hand.play_preflop()
        hand.play_streets()

        active_players = seats.get_active_players()  # get active players

if __name__ == "__main__":
    play_simple_hand()
