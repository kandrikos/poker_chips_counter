from player import Player

class Pot:
    def __init__(self):
        self.total = 0
        self.contributions = {}  # Total contributions across all rounds
        self.current_round_contributions = {}  # Contributions in the current betting round
        self.side_pots = []  # List of side pots for all-in scenarios

    def collect_bet(self, player: Player, amount: int):
        """
        Adds the amount to: 
        - pot
        - player's contributions in the current betting round
        - player's contributions in the current hand 
        """
        self.total += amount
        self.contributions[player] = self.contributions.get(player, 0) + amount
        self.current_round_contributions[player] = self.current_round_contributions.get(player, 0) + amount

    def new_betting_round(self):
        # Reset contributions for the new betting round
        self.current_round_contributions = {}

    def create_side_pot(self, all_in_amount: int):
        """Creates a side pot for all-in contributions."""
        side_pot_total = sum(min(all_in_amount, self.contributions[player]) for player in self.contributions)
        self.side_pots.append(side_pot_total)
        self.total -= side_pot_total
    
    def distribute_to_winner(self, winner: Player):
        winner.update_stack(self.total)
        self.total = 0
        self.contributions = {}
        self.side_pots = []

    def __str__(self):
        return f"Pot(total={self.total}, contributions={self.contributions}, current_round_contributions={self.current_round_contributions}"
    
    def __repr__(self):
        return self.__str__()
