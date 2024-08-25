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


    def start_betting_round(self, street):
        
        for player in self.active_players:
            player.hand_active = True
            player.actions = []
        
        self.pot = Pot()
        if street == 'pre-flop':
            bet_exists = True   # big blind exists
            # first_bet = self.big_blind

            # Post blinds
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

            # Continue the action with the next players
            # next_player_position = 3    # Position on the left of BB
            # while bet_exists:
            #     if next_player_position != 2:
            #         availiable_actions = ['fold', 'call', 'raise']
            #     next_player = next((player for player in self.active_players if player.rel_position == next_player_position), None)
            #     action = input(f"Player {next_player.name}, choose action {availiable_actions}: ")
            #     next_player.make_action(action)

            # Initialize the highest bet
            self.current_bet = max(self.pot.current_round_contributions.values(), default=0)

            # Start action with the player left of the BB
            next_player_position = 3  # Position after the BB
            
            while True:
                all_matched = True  # Flag to check if all players have matched the highest bet

                # Loop through the active players
                for i in range(len(self.active_players)):
                    next_player = next((player for player in self.active_players if player.rel_position == next_player_position), None)
                    if not next_player or not next_player.hand_active:
                        next_player_position = (next_player_position + 1) % len(self.active_players)
                        continue

                    player_contribution = self.pot.current_round_contributions.get(next_player, 0)
                    available_actions = ['fold', 'call', 'raise']

                    if player_contribution < self.current_bet:
                        available_actions = ['fold', 'call', 'raise']
                    else:
                        available_actions = ['fold', 'check', 'raise']

                    action = input(f"Player {next_player.name}, choose action {available_actions}: ").strip().lower()

                    if action == 'fold':
                        next_player.fold()
                    elif action == 'call':
                        call_amount = self.current_bet - player_contribution
                        next_player.make_action("call", call_amount, street, self)
                    elif action == 'raise':
                        raise_amount = int(input("Enter raise amount: "))
                        next_player.make_action("raise", raise_amount, street, self)
                        self.current_bet = max(self.current_bet, self.pot.current_round_contributions[next_player])
                    elif action == 'check':
                        next_player.make_action("check", 0, street, self)
                    else:
                        print("Invalid action. Try again.")
                        continue  # Retry the action for the current player

                    # Update player contribution after the action
                    player_contribution = self.pot.current_round_contributions.get(next_player, 0)
                    if player_contribution < self.current_bet and next_player.hand_active:
                        all_matched = False

                    next_player_position = (next_player_position + 1) % len(self.active_players)
                    print(f"Total pot: {self.pot.total}")

                # Exit condition: all active players have matched the highest bet or folded
                if all_matched:
                    break

        

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