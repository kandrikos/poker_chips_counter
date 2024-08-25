

class Player:
    def __init__(self, name: str, rel_position, stack: int):
        self.name = name
        self.rel_position = rel_position
        self.stack = stack
        self.hand_active = True
        self.game_active = True
        self.actions = []
    
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


    def update_stack(self, amount):
        # Ensure stack doesn't go negative
        self.stack = max(0, self.stack + amount)