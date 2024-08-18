class Pot:
    def __init__(self):
        self.total = 0
        self.contributions = {}  # Total contributions across all rounds
        self.current_round_contributions = {}  # Contributions in the current betting round

    def collect_bet(self, player, amount):
        self.total += amount
        self.contributions[player] = self.contributions.get(player, 0) + amount
        self.current_round_contributions[player] = self.current_round_contributions.get(player, 0) + amount

    def new_betting_round(self):
        # Reset contributions for the new betting round
        self.current_round_contributions = {}
    
    def distribute_to_winner(self, winner):
        winner.update_stack(self.total)
        self.total = 0
        self.contributions = {}
