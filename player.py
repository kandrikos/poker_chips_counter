class Player:
    def __init__(self, name: str, rel_position, stack: int):
        self.name = name
        self.rel_position = rel_position
        self.stack = stack
        self.hand_active = True
        self.game_active = True
        self.actions = []

    # def get_game_active_players(self):
    #     active_players = [p for p in ]
    
    def post_blind(self, hand):
        self.update_stack(-hand.current_bet)
        hand.pot.collect_bet(self, hand.current_bet)
    
    def action_call(self, hand):
        call_amount = hand.current_bet - hand.pot.current_round_contributions.get(self, 0)
        self.update_stack(-call_amount)
        hand.pot.collect_bet(self, call_amount)

    def action_raise(self, hand):
        raise_amount = int(input("Enter raise amount: "))
        self.update_stack(-raise_amount)
        hand.pot.collect_bet(self, raise_amount)
        hand.current_bet = raise_amount  # Update current_bet

    def action_check(self):
        pass

    def action_fold(self):
        self.hand_active = False

    def update_stack(self, amount):
        # Ensure stack doesn't go negative
        self.stack = max(0, self.stack + amount)

    def make_action(self, action_type, amount, street, hand):
        # if not hand.is_valid_action(self, action_type, amount):
        #     raise ValueError("Invalid action")

        action = {"type": action_type, "amount": amount, "street": street}
        self.actions.append(action)

        if action_type in ["posting SB", "posting BB"]:
            self.update_stack(-amount)
            hand.pot.collect_bet(self, amount)
            
        if action_type == "fold":
            self.hand_active = False
        elif action_type == "check":
            pass  # No change to stack or pot
        elif action_type == "call":
            call_amount = hand.current_bet - hand.pot.current_round_contributions.get(self, 0) 
            self.update_stack(-call_amount)
            hand.pot.collect_bet(self, call_amount)
        elif action_type in ["bet", "raise"]:
            self.update_stack(-amount)
            hand.pot.collect_bet(self, amount)
            hand.current_bet = amount  # Update current_bet


    