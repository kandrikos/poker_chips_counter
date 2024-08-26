class Table:
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