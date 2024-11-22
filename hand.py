class Hand:
    def __init__(self, players, table, pot, button_position, big_blind):
        self.players = players  # List of Player objects
        self.table = table      # Table object
        self.pot = pot          # Pot object
        self.button_position = button_position
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.current_bet = big_blind  # Current bet amount for this hand
        self.current_street = "pre-flop"  # Current street (pre-flop, flop, turn, river)

        self.active_players = [player for player in players if player.game_active]
        self.initialize_table()

    def initialize_table(self):
        """Assign players to seats and reset their hand state."""
        for i, player in enumerate(self.active_players):
            player.rel_position = (self.button_position + i) % len(self.active_players)
            player.hand_active = True

    def rotate_button(self):
        """Move the button to the next active player."""
        self.button_position = (self.button_position + 1) % len(self.active_players)

    def post_blinds(self):
        """Post small and big blinds."""
        small_blind_player = self.get_player_by_position(1)
        big_blind_player = self.get_player_by_position(2)

        print(f"Posting blinds: Small Blind={self.small_blind}, Big Blind={self.big_blind}")
        small_blind_player.update_stack(-self.small_blind)
        self.pot.collect_bet(small_blind_player, self.small_blind)

        big_blind_player.update_stack(-self.big_blind)
        self.pot.collect_bet(big_blind_player, self.big_blind)

    def get_player_by_position(self, position):
        """Get the player with a specific relative position."""
        for player in self.active_players:
            if player.rel_position == position:
                return player
        return None

    def play_betting_round(self, starting_position):
        """Handles a betting round."""
        num_players = len(self.active_players)
        current_index = next(
            (i for i, player in enumerate(self.active_players) if player.rel_position == starting_position),
            0,
        )

        last_raiser = None  # Track the last player to raise
        while True:
            all_actions = []
            for i in range(num_players):
                player = self.active_players[(current_index + i) % num_players]
                if player.hand_active:  # Skip players who folded
                    # Stop the round if the action returns to the last raiser
                    if last_raiser and player == last_raiser:
                        return

                    self.show_game_state(player)
                    action = self.prompt_player_action(player)
                    all_actions.append(action)

                    if action.startswith("raise"):
                        # Update the current bet and track the raiser
                        last_raiser = player
                        current_index = (current_index + i + 1) % num_players
                        break  # Stop to reset action for the next loop

            # End the round if no raises occurred
            if not any("raise" in action for action in all_actions):
                return



    def prompt_player_action(self, player):
        """Prompts the player for an action."""
        available_actions = self.get_available_actions(player)
        print(f"Available actions: {available_actions}")

        # Prompt player until a valid action is selected
        action = input(f"{player.name}, choose your action: ").strip().lower()
        while action not in available_actions and not action.startswith("raise"):
            print(f"Invalid action. Available actions: {available_actions}")
            action = input(f"{player.name}, choose your action: ").strip().lower()
        
        # Process the chosen action
        if action == "fold":
            player.action_fold()
        elif action == "call":
            player.action_call(self)
        elif action == "check":
            player.action_check()
        elif action.startswith("raise"):
            try:
                # Extract the raise amount
                _, raise_amount = action.split()
                raise_amount = int(raise_amount[1:-1])
                player.action_raise(self, raise_amount)
            except (ValueError, IndexError):
                print("Invalid raise format. Use 'raise [amount]'.")
                return self.prompt_player_action(player)  # Retry prompt on invalid raise
        return action


    def get_available_actions(self, player):
        """Determine available actions for a player."""
        self.to_call = self.current_bet - self.pot.current_round_contributions.get(player, 0)

        # Special case: Big blind can check if no raises have occurred when action returns
        if (
            self.current_street == "pre-flop"
            and player.rel_position == 2  # Big blind position
            and self.to_call == 0
        ):
            return ["check", f"raise [amount]"]

        if self.to_call == 0:
            # No bet to call: "check", "fold", or "raise" are available
            return ["check", "fold", f"raise [amount]"]

        # If there is a bet to call
        if player.can_bet(self.to_call):
            return ["call", "fold", f"raise [amount]"]
        else:
            # Player cannot afford to call
            return ["fold"]


    def show_game_state(self, player):
        """Print the current state of the game."""
        print(f"Current Street: {self.current_street}")
        print(f"Big Blind: {self.big_blind}")
        print(f"Amount to Call: {self.to_call}")
        print(f"Pot: {self.pot.total}")
        print("Stacks:")
        for p in self.players:
            print(f"{p.name}: {p.stack}")
        print()

    def distribute_pot(self):
        """Distribute the pot to the winner."""
        print("Distributing the pot...")
        winner_name = input("Enter the name of the winner: ").strip()
        winner = next(player for player in self.players if player.name == winner_name)
        self.pot.distribute_to_winner(winner)

    def play_hand(self):
        """Plays a single hand of poker."""
        self.post_blinds()
        self.play_betting_round(starting_position=3)

        for street in ["flop", "turn", "river"]:
            self.current_street = street
            print(f"Dealing {street}...")
            self.pot.new_betting_round()
            self.play_betting_round(starting_position=1)
            self.to_call = 0

        self.distribute_pot()
        self.cleanup_hand()

    def cleanup_hand(self):
        """Clean up after the hand and prepare for the next one."""
        self.rotate_button()
        self.active_players = [player for player in self.players if player.game_active]
