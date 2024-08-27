from typing import List

from player import Player
from pot import Pot

class Hand:
    def __init__(self, active_players: List[Player], btn_player: Player, big_blind: int=20):
        self.currentStreet = 'pre-flop'
        self.active_players = active_players
        self.btn_player = btn_player
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.pot = Pot()
        self.current_bet = 0
        self.button_position = 0  # Initialize button position to 0 (first player)
        # self.start_new_hand()

    def bets_called(self):
        # Method to check if a raise/bet has been called or folded. 
        # If returns `True` the action in this betting round is over.
        current_contributions = self.pot.current_round_contributions.items()
        amounts = [contribution for player, contribution in current_contributions if player.hand_active]
        return len(set(amounts)) == 1
        


    def start_betting_round(self, street):
        for player in self.active_players:
            player.hand_active = True
            player.actions = []
        
        self.pot = Pot()
        if street == 'pre-flop':

            # Post blinds
            # small blind
            player_sb = next((player for player in self.active_players if player.rel_position == 1), None)
            self.current_bet = self.small_blind
            player_sb.post_blind(self)

            # big blind                                
            player_bb = next((player for player in self.active_players if player.rel_position == 2), None)
            self.current_bet = self.big_blind
            player_bb.post_blind(self)
                       
            # Continue the action with the next players
            current_player_position = 3    # Position on the left of BB
            while not self.bets_called():
                current_player = next((player for player in self.active_players if player.rel_position == current_player_position), None)

                # skip the player(s) that folded
                if not current_player.hand_active:
                    current_player_position = (current_player_position + 1) % len(self.active_players)
                    continue  # Skip to the next player in the loop

                player_contribution = self.pot.current_round_contributions.get(current_player, 0)
                if player_contribution < self.current_bet:
                    available_actions = ['fold', 'call', 'raise']
                else:
                    available_actions = ['fold', 'check', 'raise']
                
                print("=" * 40)
                print(f"Pot: {self.pot.total}")
                print(f"Amount to call: {self.current_bet - self.pot.current_round_contributions.get(current_player, 0)}")
                # print("=" * 40)

                print("*" * 50)
                action = input(f"Player {current_player.name}, choose action {available_actions}: ")
                print("*" * 50)
                if action == 'fold':
                    current_player.action_fold()
                elif action == 'call':
                    current_player.action_call(self)
                elif action == 'raise':
                    current_player.action_raise(self)
                elif action == 'check':
                    current_player.action_check()
                else:
                    print("Invalid action. Try again.")
                    continue  # Retry the action for the current player

                player_contribution = self.pot.current_round_contributions.get(current_player, 0)

                # If the  bet/raise has been called or folded, exit loop


                # Update player's position for the next iteration
                current_player_position = (current_player_position + 1) % len(self.active_players)

            # Initialize the highest bet
            self.current_bet = max(self.pot.current_round_contributions.values(), default=0)
            print("Proceeding to the next betting round")

            # # Start action with the player left of the BB
            # current_player_position = 3  # Position after the BB
            
            # while True:
            #     all_matched = True  # Flag to check if all players have matched the highest bet

            #     # Loop through the active players
            #     for i in range(len(self.active_players)):
            #         current_player = next((player for player in self.active_players if player.rel_position == current_player_position), None)
            #         if not current_player or not current_player.hand_active:
            #             current_player_position = (current_player_position + 1) % len(self.active_players)
            #             continue

            #         player_contribution = self.pot.current_round_contributions.get(current_player, 0)
            #         available_actions = ['fold', 'call', 'raise']

            #         if player_contribution < self.current_bet:
            #             available_actions = ['fold', 'call', 'raise']
            #         else:
            #             available_actions = ['fold', 'check', 'raise']

            #         action = input(f"Player {current_player.name}, choose action {available_actions}: ").strip().lower()

            #         if action == 'fold':
            #             current_player.fold()
            #         elif action == 'call':
            #             call_amount = self.current_bet - player_contribution
            #             current_player.make_action("call", call_amount, street, self)
            #         elif action == 'raise':
            #             raise_amount = int(input("Enter raise amount: "))
            #             current_player.make_action("raise", raise_amount, street, self)
            #             self.current_bet = max(self.current_bet, self.pot.current_round_contributions[current_player])
            #         elif action == 'check':
            #             current_player.make_action("check", 0, street, self)
            #         else:
            #             print("Invalid action. Try again.")
            #             continue  # Retry the action for the current player

            #         # Update player contribution after the action
            #         player_contribution = self.pot.current_round_contributions.get(current_player, 0)
            #         if player_contribution < self.current_bet and current_player.hand_active:
            #             all_matched = False

            #         current_player_position = (current_player_position + 1) % len(self.active_players)
            #         print(f"Total pot: {self.pot.total}")

            #     # Exit condition: all active players have matched the highest bet or folded
            #     if all_matched:
            #         break

        

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