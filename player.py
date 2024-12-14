class Player:
    def __init__(self, name: str, rel_position, stack: int):
        self.name = name
        self.rel_position = rel_position 
        self.stack = stack
        self.hand_active = True  # is set to False if the player folds in a hand
        self.game_active = True  # is set to False if the player is eliminated
        self.actions = []
        self.is_all_in = False  # New flag to track all-in status

    def post_blind(self, hand):
        """Posts blind bet."""
        if self.can_bet(hand.current_bet):
            self.update_stack(-hand.current_bet)
            hand.pot.collect_bet(self, hand.current_bet)
    
    def action_call(self, hand):
        """Matches the current bet."""
        call_amount = hand.current_bet - hand.pot.current_round_contributions.get(self, 0)
        if self.can_bet(call_amount):
            self.update_stack(-call_amount)
            hand.pot.collect_bet(self, call_amount)
            self.actions.append(f"call {call_amount}")

    def action_raise(self, hand, raise_amount: int):
        """
        Raises the bet to a specified total amount.
        raise_amount represents the total commitment, not an additional amount.
        """
        # Calculate how much more the player needs to add
        already_contributed = hand.pot.current_round_contributions.get(self, 0)
        additional_amount = raise_amount - already_contributed

        if self.can_bet(additional_amount):
            self.update_stack(-additional_amount)
            hand.pot.collect_bet(self, additional_amount)
            hand.current_bet = raise_amount  # Set the new bet level for other players
            self.actions.append(f"raise {raise_amount}")

    def action_all_in(self, hand):
        """Goes all-in with remaining stack."""
        all_in_amount = self.stack
        self.update_stack(-all_in_amount)
        hand.pot.collect_bet(self, all_in_amount)
        self.is_all_in = True
        self.actions.append(f"all-in {all_in_amount}")
        # Create side pot if necessary
        if all_in_amount < hand.current_bet:
            hand.pot.create_side_pot(all_in_amount)

    def action_check(self):
        """Checks if no bet is required."""
        self.actions.append("check")

    def action_fold(self):
        """Folds the hand."""
        self.hand_active = False
        self.actions.append("fold")

    def update_stack(self, amount: int):
        """Updates the player's stack."""
        self.stack = max(0, self.stack + amount)  # ensure stack doesn't go negative

    def can_bet(self, amount: int) -> bool:
        """Returns True if the player has enough chips."""
        return self.stack >= amount

    def is_active(self) -> bool:
        """Checks if the player is active in the hand."""
        return self.hand_active and self.game_active

    def __str__(self):
        return f"Player(name={self.name}, rel_position={self.rel_position}, stack={self.stack}, hand_active={self.hand_active}, game_active={self.game_active}, actions={self.actions})"
    
    def __repr__(self):
        return self.__str__()