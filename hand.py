# class Hand:
#     def __init__(self, players, table, pot, button_position, big_blind):
#         self.players = players  # List of Player objects
#         self.table = table      # Table object
#         self.pot = pot          # Pot object
#         self.button_position = button_position
#         self.big_blind = big_blind
#         self.small_blind = big_blind // 2
#         self.current_bet = 0    # Initialize current bet to 0
#         self.current_street = "pre-flop"  # Always start with pre-flop
#         self.last_bet = 0  # Track the last bet made in the current street

#         self.active_players = [player for player in players if player.game_active]
#         self.initialize_table()

#     def initialize_table(self):
#         """Assign players to seats and reset their hand state."""
#         # Reset all players' hand state
#         for player in self.active_players:
#             player.hand_active = True
#             player.is_all_in = False

#         # Assign relative positions based on button
#         for i, player in enumerate(self.active_players):
#             player.rel_position = (i - self.button_position) % len(self.active_players)
#             # Debug print to verify positions
#             print(f"Debug - Player: {player.name}, Position: {player.rel_position}")

#     def get_player_by_position(self, position):
#         """Get the player with a specific relative position."""
#         for player in self.active_players:
#             if player.rel_position == position:
#                 return player
#         return None

#     def rotate_button(self):
#         """Move the button to the next active player."""
#         self.button_position = (self.button_position + 1) % len(self.active_players)

#     def post_blinds(self):
#         """Post small and big blinds."""
#         small_blind_player = self.get_player_by_position(1)
#         big_blind_player = self.get_player_by_position(2)

#         print(f"Posting blinds: Small Blind={self.small_blind}, Big Blind={self.big_blind}")
#         small_blind_player.update_stack(-self.small_blind)
#         self.pot.collect_bet(small_blind_player, self.small_blind)

#         big_blind_player.update_stack(-self.big_blind)
#         self.pot.collect_bet(big_blind_player, self.big_blind)

#     def get_available_actions(self, player):
#         """Determine available actions for a player."""
#         self.to_call = self.current_bet - self.pot.current_round_contributions.get(player, 0)

#         # Pre-flop specific logic
#         if self.current_street == "pre-flop":
#             # Special case: Big blind can check if no raises have occurred
#             if player.rel_position == 2 and self.to_call == 0:
#                 return ["check", "raise [amount]"]
            
#             # Normal pre-flop action
#             if self.to_call > 0:
#                 if player.can_bet(self.to_call):
#                     return ["call", "fold", "raise [amount]"]
#                 elif player.stack > 0:  # Can't match the bet but has chips
#                     return ["fold", "all-in"]
#                 else:  # No chips left
#                     return ["fold"]
        
#         # Post-flop streets (flop, turn, river)
#         else:
#             # If no bet has been made in this street
#             if self.last_bet == 0:
#                 if player.stack > 0:
#                     return ["check", "raise [amount]"]  # No fold option when checking is possible
#                 else:
#                     return ["check"]  # No chips left to raise
            
#             # If there's a bet to call
#             if self.to_call > 0:
#                 if player.can_bet(self.to_call):
#                     return ["call", "fold", "raise [amount]"]
#                 elif player.stack > 0:  # Can't match the bet but has chips
#                     return ["fold", "all-in"]
#                 else:  # No chips left
#                     return ["fold"]

#         # Default case when there's no bet to call
#         return ["check", "raise [amount]"] if player.stack > 0 else ["check"]

#     def prompt_player_action(self, player):
#         """Prompts the player for an action."""
#         if player.is_all_in:  # Skip players who are all-in
#             return "skip"

#         available_actions = self.get_available_actions(player)
#         print(f"Available actions: {available_actions}")

#         # Prompt player until a valid action is selected
#         action = input(f"{player.name}, choose your action: ").strip().lower()
#         while action not in available_actions and not action.startswith("raise"):
#             print(f"Invalid action. Available actions: {available_actions}")
#             action = input(f"{player.name}, choose your action: ").strip().lower()
        
#         # Process the chosen action
#         if action == "fold":
#             player.action_fold()
#         elif action == "call":
#             player.action_call(self)
#         elif action == "check":
#             player.action_check()
#         elif action == "all-in":
#             player.action_all_in(self)
#         elif action.startswith("raise"):
#             try:
#                 # Extract the raise amount
#                 _, raise_amount = action.split()
#                 raise_amount = int(raise_amount[1:-1])
#                 if raise_amount > player.stack:  # If raise amount is more than stack, go all-in
#                     player.action_all_in(self)
#                 else:
#                     player.action_raise(self, raise_amount)
#             except (ValueError, IndexError):
#                 print("Invalid raise format. Use 'raise [amount]'.")
#                 return self.prompt_player_action(player)
#         return action

#     def show_game_state(self, player):
#         """Print the current state of the game."""
#         print(f"Current Street: {self.current_street}")
#         print(f"Big Blind: {self.big_blind}")
#         print(f"Amount to Call: {self.current_bet - self.pot.current_round_contributions.get(player, 0)}")
#         print(f"Pot: {self.pot.total}")
#         print("Stacks:")
#         for p in self.players:
#             status = ""
#             if p.is_all_in:
#                 status = " (All-in)"
#             elif not p.hand_active:
#                 status = " (Folded)"
#             print(f"{p.name}: {p.stack}{status}")
#         print()

#     def play_betting_round(self, starting_position):
#         """Handles a betting round."""
#         num_players = len(self.active_players)
#         current_index = next(
#             (i for i, player in enumerate(self.active_players) if player.rel_position == starting_position),
#             0,
#         )

#         last_raiser = None  # Track the last player to raise
#         while True:
#             all_actions = []
#             for i in range(num_players):
#                 player = self.active_players[(current_index + i) % num_players]
#                 if player.hand_active and not player.is_all_in:  # Skip players who folded or are all-in
#                     # Stop the round if the action returns to the last raiser
#                     if last_raiser and player == last_raiser:
#                         return

#                     self.show_game_state(player)
#                     action = self.prompt_player_action(player)
#                     all_actions.append(action)

#                     if action.startswith("raise"):
#                         # Update the last bet and track the raiser
#                         _, raise_amount = action.split()
#                         self.last_bet = int(raise_amount[1:-1])
#                         self.current_bet = self.last_bet
#                         last_raiser = player
#                         current_index = (current_index + i + 1) % num_players
#                         break  # Stop to reset action for the next loop

#             # End the round if no raises occurred
#             if not any("raise" in action for action in all_actions):
#                 return

#     def play_hand(self):
#         """Plays a single hand of poker."""
#         self.post_blinds()
#         self.current_bet = self.big_blind  # Set initial bet to big blind
#         self.last_bet = self.big_blind    # Set initial last bet to big blind
#         self.play_betting_round(starting_position=3)  # Start with UTG (pos 3)

#         for street in ["flop", "turn", "river"]:
#             self.current_street = street
#             print(f"---------------- Dealing {street} ----------------")
#             self.pot.new_betting_round()
#             self.current_bet = 0  # Reset current bet for new street
#             self.last_bet = 0     # Reset last bet for new street
#             self.play_betting_round(starting_position=1)  # Start with first active player after button

#         self.distribute_pot()
#         self.cleanup_hand()

#     def distribute_pot(self):
#         """Distribute the pot to winners."""
#         print("Distributing the pots...")
#         winners = []
#         for i, pot in enumerate(self.pot.pots):
#             print(f"\nPot {i + 1} amount: {pot['amount']}")
#             print(f"Eligible players: {[p.name for p in pot['eligible_players']]}")
#             winner_name = input(f"Enter the name of the winner for pot {i + 1}: ").strip()
#             winner = next(player for player in self.players if player.name == winner_name)
#             winners.append(winner)
        
#         self.pot.distribute_to_winner(winners)

#     def cleanup_hand(self):
#         """Clean up after the hand and prepare for the next one."""
#         # We don't rotate button here anymore as it's handled in main
#         self.active_players = [player for player in self.players if player.game_active]
#         self.current_bet = 0
#         self.current_street = "pre-flop"
#         self.last_bet = 0

# hand.py
class Hand:
    def __init__(self, players, table, pot, button_position, big_blind):
        self.players = players
        self.table = table
        self.pot = pot
        self.button_position = button_position
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.current_bet = 0
        self.current_street = "pre-flop"
        self.last_bet = 0

        # Only consider players with chips as active
        self.active_players = [p for p in players if p.game_active and p.stack > 0]
        self.initialize_table()

    def initialize_table(self):
        """Assign players to seats and reset their hand state."""
        # Reset all players' hand state and positions
        for player in self.active_players:
            player.hand_active = True
            player.rel_position = None
            player.is_all_in = False

        # Assign positions relative to button
        for i in range(len(self.active_players)):
            pos = (i + self.button_position) % len(self.active_players)
            player = self.active_players[i]
            player.rel_position = pos
            print(f"Debug - Player: {player.name}, Position: {pos}")

    def get_player_by_position(self, position):
        """Get the player with a specific relative position."""
        for player in self.active_players:
            if player.rel_position == position:
                return player
        return None

    def post_blinds(self):
        """Post small and big blinds."""
        small_blind_player = self.get_player_by_position(1)
        big_blind_player = self.get_player_by_position(2)

        print(f"Posting blinds: Small Blind={self.small_blind}, Big Blind={self.big_blind}")
        small_blind_player.update_stack(-self.small_blind)
        self.pot.collect_bet(small_blind_player, self.small_blind)

        big_blind_player.update_stack(-self.big_blind)
        self.pot.collect_bet(big_blind_player, self.big_blind)

    def get_available_actions(self, player):
        """Determine available actions for a player."""
        # Skip players with no chips
        if player.stack == 0:
            return []

        self.to_call = self.current_bet - self.pot.current_round_contributions.get(player, 0)

        # Pre-flop specific logic
        if self.current_street == "pre-flop":
            # Special case: Big blind can check if no raises have occurred
            if player.rel_position == 2 and self.to_call == 0:
                return ["check", "raise [amount]"]
            
            # Normal pre-flop action
            if self.to_call > 0:
                if player.can_bet(self.to_call):
                    return ["call", "fold", "raise [amount]"]
                elif player.stack > 0:  # Can't match the bet but has chips
                    return ["fold", "all-in"]
                else:  # No chips left
                    return ["fold"]
        
        # Post-flop streets (flop, turn, river)
        else:
            # If no bet has been made in this street
            if self.last_bet == 0:
                if player.stack > 0:
                    return ["check", "raise [amount]"]  # No fold option when checking is possible
                else:
                    return ["check"]  # No chips left to raise
            
            # If there's a bet to call
            if self.to_call > 0:
                if player.can_bet(self.to_call):
                    return ["call", "fold", "raise [amount]"]
                elif player.stack > 0:  # Can't match the bet but has chips
                    return ["fold", "all-in"]
                else:  # No chips left
                    return ["fold"]

        # Default case when there's no bet to call
        return ["check", "raise [amount]"] if player.stack > 0 else ["check"]

    def prompt_player_action(self, player):
        """Prompts the player for an action."""
        if player.is_all_in or player.stack == 0:  # Skip players who are all-in or have no chips
            return "skip"

        available_actions = self.get_available_actions(player)
        print(f"Available actions: {available_actions}")

        action = input(f"{player.name}, choose your action: ").strip().lower()
        while action not in available_actions and not action.startswith("raise"):
            print(f"Invalid action. Available actions: {available_actions}")
            action = input(f"{player.name}, choose your action: ").strip().lower()
        
        if action == "fold":
            player.action_fold()
        elif action == "call":
            player.action_call(self)
        elif action == "check":
            player.action_check()
        elif action == "all-in":
            player.action_all_in(self)
        elif action.startswith("raise"):
            try:
                _, raise_amount = action.split()
                raise_amount = int(raise_amount[1:-1])
                if raise_amount > player.stack:
                    player.action_all_in(self)
                else:
                    player.action_raise(self, raise_amount)
            except (ValueError, IndexError):
                print("Invalid raise format. Use 'raise [amount]'")
                return self.prompt_player_action(player)
        return action

    def show_game_state(self, player):
        """Print the current state of the game."""
        print(f"Current Street: {self.current_street}")
        print(f"Big Blind: {self.big_blind}")
        print(f"Amount to Call: {self.current_bet - self.pot.current_round_contributions.get(player, 0)}")
        print(f"Pot: {self.pot.total}")
        print("Stacks:")
        for p in self.players:
            status = ""
            if not p.hand_active:
                status = " (Folded)"
            elif p.is_all_in:
                status = " (All-in)"
            print(f"{p.name}: {p.stack}{status}")
        print()

    def play_betting_round(self, starting_position):
        """Handles a betting round."""
        num_players = len(self.active_players)
        current_index = next(
            (i for i, player in enumerate(self.active_players) if player.rel_position == starting_position),
            0,
        )

        last_raiser = None
        while True:
            all_actions = []
            for i in range(num_players):
                player = self.active_players[(current_index + i) % num_players]
                if player.hand_active and not player.is_all_in:
                    if last_raiser and player == last_raiser:
                        return

                    self.show_game_state(player)
                    action = self.prompt_player_action(player)
                    all_actions.append(action)

                    if action.startswith("raise"):
                        _, raise_amount = action.split()
                        self.last_bet = int(raise_amount[1:-1])
                        self.current_bet = self.last_bet
                        last_raiser = player
                        current_index = (current_index + i + 1) % num_players
                        break

            if not any("raise" in action for action in all_actions):
                return

    def play_hand(self):
        """Plays a single hand of poker."""
        self.post_blinds()
        self.current_bet = self.big_blind
        self.last_bet = self.big_blind
        self.play_betting_round(starting_position=3)

        for street in ["flop", "turn", "river"]:
            print(f"---------------- Dealing {street} ----------------")
            self.current_street = street
            self.pot.new_betting_round()
            self.current_bet = 0
            self.last_bet = 0
            self.play_betting_round(starting_position=1)

        self.distribute_pot()
        self.cleanup_hand()

    def distribute_pot(self):
        """Distribute the pot to winners."""
        print("Distributing the pots...")
        winners = []
        for i, pot in enumerate(self.pot.pots):
            print(f"\nPot {i + 1} amount: {pot['amount']}")
            eligible_players = self.pot.get_eligible_players()
            print(f"Eligible players: {eligible_players}")
            
            while True:
                winner_name = input(f"Enter the name of the winner for pot {i + 1}: ").strip()
                if winner_name in eligible_players:
                    winner = next(player for player in self.players if player.name == winner_name)
                    winners.append(winner)
                    break
                else:
                    print(f"Invalid winner. Must be one of: {eligible_players}")
        
        self.pot.distribute_to_winner(winners)

    def cleanup_hand(self):
        """Clean up after the hand and prepare for the next one."""
        self.button_position = (self.button_position + 1) % len(self.active_players)
        self.active_players = [p for p in self.players if p.game_active and p.stack > 0]
        self.current_bet = 0
        self.current_street = "pre-flop"
        self.last_bet = 0