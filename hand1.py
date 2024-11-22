# from player import Player
# from table import Table
# from pot import Pot

# from tests import test_cases


# class Hand:
#     def __init__(self, players: List[Player], btn_player: Player, big_blind: int=20):
#         # self.current_street = 'PRE-FLOP'
#         self.players = players
#         self.btn_player = btn_player
#         self.big_blind = big_blind
#         self.small_blind = big_blind // 2
#         self.active_players = [player for player in players if player.game_active]
#         self.pot = Pot()
#         self.pot.current_round_contributions = {player : 0 for player in self.active_players}
#         self.current_bet = 0
#         self.button_position = 0  # Initialize button position to 0 (first player)
#         self.posting_blinds = True
#         # self.start_new_hand()

#     def _bets_called(self):
#         # Method to check if a raise/bet has been called or folded.
#         # If returns `True` the action in this betting round is over.           
#         current_contributions = self.pot.current_round_contributions.items()
#         amounts = [contribution for player, contribution in current_contributions if player.hand_active]
#         return len(set(amounts)) == 1
        
#     def _initiate_round(self, street):
#         if street == "PRE-FLOP":
#             # Post small blind
#             self.player_sb = next((player for player in self.active_players if player.rel_position == 1), None)
#             self.current_bet = self.small_blind
#             self.player_sb.post_blind(self)

#             # Post big blind                                
#             self.player_bb = next((player for player in self.active_players if player.rel_position == 2), None)
#             self.current_bet = self.big_blind
#             self.player_bb.post_blind(self)

#             self.current_player_position = 3
#             self.posting_blinds = False   # No blinds in the next street
#         else:
#             self.current_player_position = 1

#     def special_cases(self):
#         # Case 1: Pre-flop round, no raise exists and the last player to act (BB) has the option `check`

#         # Case 2: 
#         pass


#     def _action_round(self, street_actions=None):
        
#         actions_taken = 0
#         total_active_players = len([p for p in self.active_players if p.hand_active])

#         while actions_taken < total_active_players or not self._bets_called():

#             # raise_exist = False
#             # # TODO:
#             # #
#             # # In preflop round, if all players call (or fold) the BB has the options: ['check', 'raise']
#             # #
#             # #
#             current_player = next((player for player in self.active_players if player.rel_position == self.current_player_position), None)

#             # skip the player(s) that folded
#             if not current_player.hand_active:
#                 self.current_player_position = (self.current_player_position + 1) % len(self.active_players)
#                 continue  # Skip to the next player in the loop

#             player_contribution = self.pot.current_round_contributions.get(current_player, 0)
#             if player_contribution < self.current_bet:
#                 available_actions = ['fold', 'call', 'raise']
#             else:
#                 available_actions = ['check', 'raise']
            
#             print("=" * 40)
#             print(f"Pot: {self.pot.total}")
#             print(f"Amount to call: {self.current_bet - self.pot.current_round_contributions.get(current_player, 0)}")

#             print("*" * 50)
#             # Fetch the action from test case if available
#             action = (street_actions.get(current_player.name, []).pop(0) 
#                   if street_actions and current_player.name in street_actions 
#                   else input(f"Player {current_player.name}, choose action {available_actions}: "))
            
            
#             print("*" * 50)
#             if action == 'fold':
#                 current_player.action_fold()
#             elif action == 'call':
#                 current_player.action_call(self)
#             elif action == 'raise':
#                 current_player.action_raise(self)
#                 actions_taken = 0 # Reset actions count if there's a raise
#             elif action == 'check':
#                 current_player.action_check()
#             else:
#                 print("Invalid action. Try again.")
#                 continue  # Retry the action for the current player

#             # Count action and move to next player
#             actions_taken += 1
#             self.current_player_position = (self.current_player_position + 1) % len(self.active_players)

#             if actions_taken >= total_active_players and self._bets_called():
#                 break  # End round after all active players act and bets are matched
#         print("Proceeding to the next betting round")

#     def start_hand(self, test_actions=None):
#         streets = ["PRE-FLOP", "FLOP", "TURN", "RIVER"]
#         for street in streets:    
#             # for player in self.active_players: # TODO: WRONG! Do not set players `hand_active` in each street  
#             #     player.hand_active = True
#             #     player.actions = []
#             self.current_street = street
#             print(f"%%%%%%%%%%%%%%%%%%%%% {self.current_street} %%%%%%%%%%%%%%%%%%%%%")
#             self._initiate_round(self.current_street)
#             self._action_round(test_actions.get(street) if test_actions else None)
    
#     def end_hand(self):
#         # Determine winner(s)
#         winner = str(input(f"Enter winner: ({' / '.join([f'{p}' for p in self.active_players if p.hand_active])})"))
#         winner_player = next((player for player in self.active_players if player.name == winner), None)

#         # Distribute pot
#         winner_player.stack += self.pot.total

#         # Rotate the dealer button
#         for player in self.active_players:
#             player.rel_position -= 1
            
#     def play_hand(self, test_actions=None):
#         self.start_hand()
#         self.end_hand()
    
# from player import Player
from table import Table
from pot import Pot

class Hand:
    def __init__(self, players, initial_stack: int, big_blind: int, button_position: int):
        self.players = players
        self.table = Table(players)
        self.pot = Pot()
        self.button_position = button_position
        self.big_blind = big_blind
        self.current_bet = 0  # Tracks the current bet amount in this hand

        # Assign relative positions to players
        self.assign_positions()

    def assign_positions(self):
        """Assigns relative positions to players based on button position."""
        num_players = len(self.players)
        for i, player in enumerate(self.players):
            player.rel_position = (i - self.button_position) % num_players

    def post_blinds(self):
        """Posts the small and big blinds."""
        small_blind_player = self.get_player_by_position(1)
        big_blind_player = self.get_player_by_position(2)

        # Post blinds
        small_blind_player.post_blind(self)
        self.current_bet = self.big_blind
        big_blind_player.post_blind(self)

    def get_player_by_position(self, position):
        """Returns the player with the given relative position."""
        for player in self.players:
            if player.rel_position == position:
                return player
        return None

    def betting_round(self, starting_position):
        """Handles a single betting round."""
        active_players = [p for p in self.players if p.is_active()]
        num_active = len(active_players)

        i = starting_position  # Start with the given position
        action_complete = False
        last_raise_position = None  # Tracks the position of the last raise

        while not action_complete:
            player = self.get_player_by_position(i)
            if player and player.is_active():
                action = input(f"{player.name} (stack: {player.stack}), action [call, raise, fold]: ").strip().lower()

                if action == "call":
                    player.action_call(self)
                elif action == "raise":
                    raise_amount = int(input("Enter raise amount: "))
                    player.action_raise(self, raise_amount)
                    last_raise_position = i
                elif action == "fold":
                    player.action_fold()

            # Move to the next player
            i = (i + 1) % num_active

            # End betting round if all players have acted, and no further raises are pending
            if i == starting_position and last_raise_position is None:
                action_complete = True
            elif i == last_raise_position:
                action_complete = True

    def play_hand(self):
        """Plays a single hand from start to finish."""
        # Pre-flop
        print("Starting pre-flop...")
        self.post_blinds()
        self.betting_round(3)

        # Flop
        print("Dealing the flop...")
        self.betting_round(1)

        # Turn
        print("Dealing the turn...")
        self.betting_round(1)

        # River
        print("Dealing the river...")
        self.betting_round(1)

        # Determine winner
        winner_name = input("Enter the name of the winning player: ").strip()
        winner = next(p for p in self.players if p.name == winner_name)
        self.pot.distribute_to_winner(winner)

    def prepare_next_hand(self):
        """Prepares the table for the next hand."""
        # Remove eliminated players
        self.players = [p for p in self.players if p.is_active()]
        self.table = Table(self.players)

        # Move the button clockwise
        num_players = len(self.players)
        self.button_position = (self.button_position + 1) % num_players

        # Reassign positions
        self.assign_positions()

    def __str__(self):
        return f"Hand(button_position={self.button_position}, current_bet={self.current_bet}, pot={self.pot})"
