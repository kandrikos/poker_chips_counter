# game_controller.py
from hand import Hand
from player import Player
from table import Table
from pot import Pot

class GameController:
    def __init__(self, gui=None):
        self.gui = gui
        self.init_game()

    def init_game(self):
        # Initialize game components
        self.num_players = 5
        self.player_names = [f"Player_{i}" for i in range(self.num_players)]
        self.initial_stack = 10000
        self.big_blind = 100
        self.button_position = 0

        # Create players
        self.players = [Player(name, i, self.initial_stack) for i, name in enumerate(self.player_names)]
        self.table = Table(self.players, num_seats=self.num_players)
        self.pot = Pot()
        
        # Create first hand
        self.current_hand = Hand(self.players, self.table, self.pot, 
                               self.button_position, self.big_blind)
        
        # Additional state tracking
        self.current_player = None
        self.current_player_options = []
        self.last_raiser = None
        self.betting_round_start_position = 3  # UTG for preflop
        self.actions_this_round = []  # Track actions in current betting round
        self.active_players_count = len([p for p in self.players if p.hand_active and not p.is_all_in])
        
        if self.gui:
            self.update_gui()

    def start_new_hand(self):
        self.pot = Pot()
        self.current_hand = Hand(self.players, self.table, self.pot,
                               self.button_position, self.big_blind)
        
        # Reset state tracking
        self.last_raiser = None
        self.betting_round_start_position = 3  # UTG for preflop
        self.actions_this_round = []
        self.active_players_count = len([p for p in self.players if p.game_active and not p.is_all_in])
        
        # Post blinds and start the hand
        self.current_hand.post_blinds()
        self.current_hand.current_bet = self.big_blind
        
        if self.gui:
            self.update_gui()
            
        # Start with UTG position
        self.handle_next_action(self.betting_round_start_position)

    def handle_next_action(self, position):
        """Handle the next player action"""
        # Find next active player
        found_player = False
        current_position = position
        
        while not found_player:
            self.current_player = self.current_hand.get_player_by_position(current_position)
            if not self.current_player:
                self.move_to_next_street()
                return
                
            if self.current_player.hand_active and not self.current_player.is_all_in:
                found_player = True
            else:
                current_position = (current_position + 1) % len(self.players)
                if current_position == position:  # We've gone full circle
                    self.move_to_next_street()
                    return

        if self.last_raiser and self.current_player == self.last_raiser:
            self.move_to_next_street()
            return

        self.current_player_options = self.current_hand.get_available_actions(self.current_player)
        
        if self.gui:
            self.update_gui()
            self.gui.enable_valid_actions(self.current_player_options)

    def handle_player_action(self, action, raise_amount=None):
        """Process a player action from the GUI"""
        if not self.current_player:
            return

        # Record the action
        self.actions_this_round.append(action)
        print(f"Action recorded: {action} by {self.current_player.name}")  # Debug print

        # Process the action
        if action == "fold":
            self.current_player.action_fold()
            self.active_players_count -= 1
        elif action == "check":
            self.current_player.action_check()
        elif action == "call":
            self.current_player.action_call(self.current_hand)
        elif action == "raise":
            self.current_player.action_raise(self.current_hand, raise_amount)
            self.last_raiser = self.current_player
        elif action == "all-in":
            self.current_player.action_all_in(self.current_hand)
            self.active_players_count -= 1
            if self.current_player.stack > self.current_hand.current_bet:
                self.last_raiser = self.current_player

        # Update GUI after action
        if self.gui:
            self.update_gui()

        # Check if betting round is complete
        if self.is_betting_round_complete():
            print("Betting round complete, moving to next street")  # Debug print
            self.move_to_next_street()
        else:
            # Move to next player
            next_position = (self.current_player.rel_position + 1) % len(self.players)
            self.handle_next_action(next_position)

    def is_betting_round_complete(self):
        """Check if the current betting round is complete"""
        # If there's a raise, we need everyone to act after it
        if self.last_raiser:
            last_raise_index = 0
            for i, action in enumerate(self.actions_this_round):
                if action.startswith('raise'):
                    last_raise_index = i
            
            # Count how many players acted after the last raise
            actions_after_raise = len(self.actions_this_round) - last_raise_index - 1
            return actions_after_raise >= self.active_players_count - 1
        
        # If no raise, everyone needs to act once
        return len(self.actions_this_round) >= self.active_players_count

    def start_new_street(self, street):
        """Start a new betting round for the next street"""
        print(f"Starting new street: {street}")  # Debug print
        self.current_hand.current_street = street
        self.current_hand.pot.new_betting_round()
        self.current_hand.current_bet = 0
        self.current_hand.last_bet = 0
        self.last_raiser = None
        self.betting_round_start_position = 1  # Start with first active player after button
        self.actions_this_round = []  # Reset actions for new street
        self.active_players_count = len([p for p in self.players if p.hand_active and not p.is_all_in])
        
        if self.gui:
            self.update_gui()
        
        self.handle_next_action(self.betting_round_start_position)

    def move_to_next_street(self):
        """Progress to the next street or end the hand"""
        current_street = self.current_hand.current_street
        
        if current_street == "pre-flop":
            self.start_new_street("flop")
        elif current_street == "flop":
            self.start_new_street("turn")
        elif current_street == "turn":
            self.start_new_street("river")
        elif current_street == "river":
            self.end_hand()

    def end_hand(self):
        """Handle end of hand and pot distribution"""
        print("Hand complete - implement winner selection")
        
        # Rotate button and start new hand
        self.button_position = (self.button_position + 1) % len(self.players)
        self.start_new_hand()

    def update_gui(self):
        """Update all GUI elements with current game state"""
        if not self.gui:
            return

        # Update pot
        self.gui.update_pot(self.pot.total)
        
        # Update player information
        for player in self.players:
            self.gui.update_player_seat(
                player.name,
                player.stack,
                player.rel_position,
                player.hand_active,
                player == self.current_player
            )
        
        # Update game information
        self.gui.update_game_info(
            street=self.current_hand.current_street,
            current_bet=self.current_hand.current_bet,
            big_blind=self.big_blind
        )