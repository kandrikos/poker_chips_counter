from typing import List

from player import Player
from pot import Pot

class Hand:
    def __init__(self, players: List[Player], btn_player: Player, big_blind: int=20):
        self.currentStreet = 'pre-flop'
        self.players = players
        self.btn_player = btn_player
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.active_players = [player for player in players if player.game_active]
        self.pot = Pot()
        self.pot.current_round_contributions = {player : 0 for player in self.active_players}
        self.current_bet = 0
        self.button_position = 0  # Initialize button position to 0 (first player)
        self.posting_blinds = True
        # self.start_new_hand()

    def _bets_called(self):
        # Method to check if a raise/bet has been called or folded. 
        # If returns `True` the action in this betting round is over.
            
        current_contributions = self.pot.current_round_contributions.items()
        amounts = [contribution for player, contribution in current_contributions if player.hand_active]
        return len(set(amounts)) == 1
        
    def _initiate_round(self, street):
        

        if street == "PRE-FLOP":
            # Post small blind
            player_sb = next((player for player in self.active_players if player.rel_position == 1), None)
            self.current_bet = self.small_blind
            player_sb.post_blind(self)

            # Post big blind                                
            player_bb = next((player for player in self.active_players if player.rel_position == 2), None)
            self.current_bet = self.big_blind
            player_bb.post_blind(self)

            self.current_player_position = 3
            self.posting_blinds = False   # No blinds in the next street
        else:
            self.current_player_position = 1

    def _action_round(self):
        

        while not self._bets_called() or not self.posting_blinds:
            # TODO:
            #
            # In preflop round, if all players call (or fold) the BB has the options: ['check', 'raise']
            #
            #
            current_player = next((player for player in self.active_players if player.rel_position == self.current_player_position), None)

            # skip the player(s) that folded
            if not current_player.hand_active:
                self.current_player_position = (self.current_player_position + 1) % len(self.active_players)
                continue  # Skip to the next player in the loop

            player_contribution = self.pot.current_round_contributions.get(current_player, 0)
            if player_contribution < self.current_bet:
                available_actions = ['fold', 'call', 'raise']
            else:
                available_actions = ['fold', 'check', 'raise']
            
            print("=" * 40)
            print(f"Pot: {self.pot.total}")
            print(f"Amount to call: {self.current_bet - self.pot.current_round_contributions.get(current_player, 0)}")

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

            # Update player's position for the next iteration
            self.current_player_position = (self.current_player_position + 1) % len(self.active_players)

            # Initialize the highest bet
            self.current_bet = max(self.pot.current_round_contributions.values(), default=0)
        print("Proceeding to the next betting round")


    def start_hand(self):
        streets = ["PRE-FLOP", "FLOP", "TURN", "RIVER"]
        for street in streets:    
            for player in self.active_players: # TODO: WRONG! Do not set players `hand_active` in each street  
                player.hand_active = True
                player.actions = []
            
            print(f"%%%%%%%%%%%%%%%%%%%%% {street} %%%%%%%%%%%%%%%%%%%%%")
            self._initiate_round(street)
            self._action_round()
    
    def end_hand(self):
        # Determine winner(s)
        winner = str(input(f"Enter winner: ({' / '.join([f'{p}' for p in self.active_players if p.hand_active])})"))
        winner_player = next((player for player in self.active_players if player.name == winner), None)

        # Distribute pot
        winner_player.stack += self.pot.total

        # Rotate the dealer button
        for player in self.active_players:
            player.rel_position += 1
            
    def play_hand(self):
        self.start_hand()
        self.end_hand()
    
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