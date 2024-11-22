from player import Player

class Table:
    def __init__(self, players: list[Player], num_seats: int = 9):
        self.seats = {f"seat_{i}": None for i in range(num_seats)}
        for i, player in enumerate(players[:num_seats]):
            self.seats[f"seat_{i}"] = player

    def get_player_at_seat(self, seat: str):
        return self.seats.get(seat)

    def assign_player_to_seat(self, seat: str, player: Player):
        if seat in self.seats:
            self.seats[seat] = player

    def remove_player_from_seat(self, seat: str):
        if seat in self.seats:
            self.seats[seat] = None

    def get_active_players(self):
        """Returns a list of active players."""
        return [player for player in self.seats.values() if player and player.is_active()]
    
    def __str__(self):
        return f"Table(seats={self.seats}"
    
    def __repr__(self):
        return self.__str__()