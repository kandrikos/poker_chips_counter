from typing import List

from player import Player
from pot import Pot

class Hand:
    def __init__(self, active_players: List[Player], btn_player: Player, big_blind: int=20):
        self.currentStreet = 'pre-flop'
        self.active_players = active_players
        self.btn_player = btn_player
        self.big_blind = big_blind
        self.pot = Pot()
        self.current_bet = 0
        self.button_position = 0  # Initialize button position to 0 (first player)
        # self.start_new_hand()

    def play_preflop(self):
        # Reset player states
        for player in self.active_players:
            player.hand_active = True 
            player.actions = []

        # Reset pot
        self.pot = Pot()
        self.current_bet = self.big_blind

        # Collect blinds
        player_sb = next((player for player in self.active_players if player.rel_position == 1), None)
        if player_sb.stack <= self.big_blind // 2:
            player_sb.make_action("posting SB", player_sb.stack, "pre-flop", self)
        else:
            player_sb.make_action("posting SB", self.big_blind // 2, "pre-flop", self)
        
        player_bb = next((player for player in self.active_players if player.rel_position == 2), None)
        if player_bb.stack <= self.big_blind:
            player_bb.make_action("posting BB", player_bb.stack, "pre-flop", self)
        else:
            player_bb.make_action("posting BB", self.big_blind, "pre-flop", self)

        
        # Ask for action to the next player
        # Possible action: [fold, call, raise]
        next_player_position = 3  # Position of the next player after BB
        next_player = next((player for player in self.active_players if player.rel_position == next_player_position), None)
        if next_player:
            # Handle action for the next player
            action = input(f"Player {next_player.name}, choose action (fold, call, raise): ")
            while action not in ['fold', 'call', 'raise']:
                print("Invalid action. Please choose from fold, call, raise.")
                action = input(f"Player {next_player.name}, choose action (fold, call, raise): ")
            
            # Perform action based on player's choice
            if action == 'fold':
                next_player.make_action("fold", 0, "pre-flop", self)
            elif action == 'call':
                call_amount = self.current_bet - next_player.current_bet
                next_player.make_action("call", call_amount, "pre-flop", self)
            elif action == 'raise':
                raise_amount = int(input(f"Enter the raise amount for Player {next_player.name}: "))
                next_player.make_action("raise", raise_amount, "pre-flop", self)




    
    # def play_preflop(self):
    #     for player in self.activePlayers:
    #         if 
        
    #     pass




    def play_streets(self):
        pass



    def end_hand(self):
        # Determine winner(s)
        # Distribute pot
        # Rotate the dealer button at the end of the method
        pass
    
    def is_valid_action(self, player, action_type, amount):
        # Blinds checks 
        if action_type == "posting SB":
            if player.rel_position == 1:
                return True
        
        if action_type == "posting BB":
            if player.rel_position == 2:
                return True

        # Basic checks
        if action_type not in ["fold", "check", "call", "bet", "raise"]:
            return False
        if amount < 0 or amount > player.stack:
            return False
        
        
        # Check for SB completing the blind (pre-flop only)
        if player.rel_position == 1 and self.currentStreet == "pre-flop":
            amount_to_call = self.big_blind - self.pot.current_round_contributions.get(player, 0)
            if action_type == "check" and amount_to_call > 0:
                return False  # Can't check if SB needs to complete
            if action_type == "call" and amount != amount_to_call:
                return False  # Call amount must match the amount needed
            
        # Check for BB completing the blind (pre-flop only)
        if player.rel_position == 2 and self.currentStreet == "pre-flop":
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