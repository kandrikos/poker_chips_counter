from typing import List

from player import Player
from pot import Pot

class Hand:
    def __init__(self, players: List[Player], big_blind: int=20):
        self.currentStreet = 'pre-flop'
        self.activePlayers = players
        self.big_blind = big_blind
        self.pot = Pot()
        self.current_bet = 0
        self.button_position = 0  # Initialize button position to 0 (first player)
        # self.start_new_hand()

    def start_new_hand(self):
        # Reset player states
        for player in self.activePlayers:
            player.isActive = True 
            player.actions = []

        # Reset pot
        self.pot = Pot()
        self.current_bet = self.big_blind

        # Collect blinds
        for player in self.activePlayers:
            if player.position == "SB":
                player.make_action("posting SB", self.big_blind // 2, "pre-flop", self)
            elif player.position == "BB":
                player.make_action("posting BB", self.big_blind, "pre-flop", self)



    def end_hand(self):
        # Determine winner(s)
        # Distribute pot
        # Rotate the dealer button at the end of the method
        pass
    
    def is_valid_action(self, player, action_type, amount):
        # Blinds checks 
        if action_type == "posting SB":
            if player.position == "SB":
                return True
        
        if action_type == "posting BB":
            if player.position == "BB":
                return True

        # Basic checks
        if action_type not in ["fold", "check", "call", "bet", "raise"]:
            return False
        if amount < 0 or amount > player.stack:
            return False
        
        
        # Check for SB completing the blind (pre-flop only)
        if player.position == "SB" and self.currentStreet == "pre-flop":
            amount_to_call = self.big_blind - self.pot.current_round_contributions.get(player, 0)
            if action_type == "check" and amount_to_call > 0:
                return False  # Can't check if SB needs to complete
            if action_type == "call" and amount != amount_to_call:
                return False  # Call amount must match the amount needed
            
        # Check for BB completing the blind (pre-flop only)
        if player.position == "BB" and self.currentStreet == "pre-flop":
            # BB has already posted the big blind, so they can check if no one has raised
            if action_type == "check" and self.current_bet == self.big_blind:
                return True
            # If there's a raise, BB needs to call or raise further
            elif action_type == "call" and amount == self.current_bet - self.big_blind:
                return True
            elif action_type == "raise" and amount >= self.current_bet * 2:  # Minimum raise is 2x current bet
                return True
            else:
                return False

        # General betting rules
        if self.current_bet == 0:  # No bet has been made yet
            if action_type == "check":
                return True
            elif action_type == "bet" and amount > 0:
                return True
            else:
                return False
        else:  # There's a current bet
            if action_type == "fold":
                return True
            elif action_type == "call" and amount == self.current_bet:
                return True
            elif action_type == "raise" and amount >= self.current_bet * 2:  # Assuming minimum raise is 2x current bet
                return True
            else:
                return False