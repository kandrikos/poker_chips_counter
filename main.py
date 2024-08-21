from player import Player
from hand import Hand

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

    players_names = ["A", "B", "C", "D", "E", "F"]

    # players = [
    #     Player("A", None, initial_stack),
    #     Player("B", None, initial_stack),
    #     Player("C", None, initial_stack),
    #     Player("D", None, initial_stack),
    #     Player("E", None, initial_stack),
    #     Player("F", None, initial_stack)
    # ]
    # assign positions to the table
    table = Table(len(players_names))

    for name in players_names:
        seat = int(input(f"Enter the seat number for player {name} (1-6): "))
        table.assign_seat(Player(name, None, initial_stack), seat)

    first_button_seat = int(input("Select the 1st dealer seat (1-6): "))

    table.seating.get(first_button_seat).position = "Button"
    try:
        table.seating.get(first_button_seat + 1).position = "SB"
    except AttributeError:
        table.seating.get(1).position = "SB"
        table.seating.get(2).position = "BB"
    
    table.seating.get(first_button_seat + 2).position = "BB"

    table.rotate_button()

    players = list(table.seating.values())
    hand = Hand(players, initial_bb)
    hand.start_new_hand()

if __name__ == "__main__":
    play_simple_hand()
