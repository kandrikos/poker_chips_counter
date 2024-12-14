# class Pot:
#     def __init__(self):
#         self.total = 0
#         self.contributions = {}  # Total contributions across all rounds
#         self.current_round_contributions = {}  # Contributions in the current betting round
#         self.pots = [{"amount": 0, "eligible_players": set()}]  # List of pots (main pot and side pots)

#     def collect_bet(self, player, amount: int):
#         """Adds the amount to pot and tracks contributions"""
#         self.total += amount
#         self.contributions[player] = self.contributions.get(player, 0) + amount
#         self.current_round_contributions[player] = self.current_round_contributions.get(player, 0) + amount
        
#         # Add player to eligible players for main pot
#         self.pots[0]["eligible_players"].add(player)
#         self.pots[0]["amount"] += amount

#     def create_side_pot(self, all_in_amount: int):
#         """Creates a side pot when a player goes all-in"""
#         current_pot = self.pots[-1]  # Get the last pot
#         new_pot_amount = 0
#         new_pot_players = set()

#         # Calculate excess chips that go to the side pot
#         for player, contribution in self.contributions.items():
#             if contribution > all_in_amount and player in current_pot["eligible_players"]:
#                 excess = min(contribution - all_in_amount, self.current_round_contributions.get(player, 0))
#                 if excess > 0:
#                     new_pot_amount += excess
#                     new_pot_players.add(player)
#                     current_pot["amount"] -= excess

#         # Create new side pot if there are excess chips
#         if new_pot_amount > 0:
#             self.pots.append({
#                 "amount": new_pot_amount,
#                 "eligible_players": new_pot_players
#             })

#     def new_betting_round(self):
#         """Reset contributions for the new betting round"""
#         self.current_round_contributions = {}

#     def distribute_to_winner(self, winners_by_pot):
#         """
#         Distribute pots to winners. 
#         winners_by_pot should be a list of winners, one for each pot
#         """
#         for i, winner in enumerate(winners_by_pot):
#             if i < len(self.pots):
#                 pot = self.pots[i]
#                 if winner in pot["eligible_players"]:
#                     winner.update_stack(pot["amount"])

#         # Reset everything after distribution
#         self.total = 0
#         self.contributions = {}
#         self.pots = [{"amount": 0, "eligible_players": set()}]

#     def __str__(self):
#         return f"Pot(total={self.total}, contributions={self.contributions}, current_round_contributions={self.current_round_contributions}, pots={self.pots})"
    
#     def __repr__(self):
#         return self.__str__()

# pot.py
class Pot:
    def __init__(self):
        self.total = 0
        self.contributions = {}  # Total contributions across all rounds
        self.current_round_contributions = {}  # Contributions in the current betting round
        self.pots = [{"amount": 0, "eligible_players": set()}]  # List of pots (main pot and side pots)

    def collect_bet(self, player, amount: int):
        """Adds the amount to pot and tracks contributions"""
        self.total += amount
        self.contributions[player] = self.contributions.get(player, 0) + amount
        self.current_round_contributions[player] = self.current_round_contributions.get(player, 0) + amount
        
        # Only add to eligible players if the player hasn't folded
        if player.hand_active:
            self.pots[0]["eligible_players"].add(player)
        self.pots[0]["amount"] += amount

    def create_side_pot(self, all_in_amount: int):
        """Creates a side pot when a player goes all-in"""
        current_pot = self.pots[-1]  # Get the last pot
        new_pot_amount = 0
        new_pot_players = set()

        # Calculate excess chips that go to the side pot
        for player, contribution in self.contributions.items():
            if contribution > all_in_amount and player in current_pot["eligible_players"]:
                excess = min(contribution - all_in_amount, self.current_round_contributions.get(player, 0))
                if excess > 0:
                    new_pot_amount += excess
                    new_pot_players.add(player)
                    current_pot["amount"] -= excess

        # Create new side pot if there are excess chips
        if new_pot_amount > 0:
            self.pots.append({
                "amount": new_pot_amount,
                "eligible_players": new_pot_players
            })

    def new_betting_round(self):
        """Reset contributions for the new betting round"""
        self.current_round_contributions = {}

    def get_eligible_players(self):
        """Returns list of player names who are eligible to win the pot"""
        return [p.name for p in self.pots[0]["eligible_players"] if p.hand_active]

    def distribute_to_winner(self, winners_by_pot):
        """Distribute pots to winners."""
        for i, winner in enumerate(winners_by_pot):
            if i < len(self.pots):
                pot = self.pots[i]
                if winner in pot["eligible_players"]:
                    winner.update_stack(pot["amount"])

        # Reset everything after distribution
        self.total = 0
        self.contributions = {}
        self.pots = [{"amount": 0, "eligible_players": set()}]

    def __str__(self):
        return f"Pot(total={self.total}, contributions={self.contributions}, current_round_contributions={self.current_round_contributions}, pots={self.pots})"
    
    def __repr__(self):
        return self.__str__()