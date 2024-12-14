# poker_gui.py
import tkinter as tk
from tkinter import ttk
from game_controller import GameController

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game")
        self.root.geometry("1200x800")
        
        # Setup UI components
        self.setup_ui()
        
        # Create game controller
        self.controller = GameController(self)
        
        # Start first hand
        self.controller.start_new_hand()

    def setup_ui(self):
        """Setup all UI components"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(sticky='nsew')
        
        # Create table frame
        self.table_frame = ttk.Frame(self.main_frame, padding="10")
        self.table_frame.grid(row=0, column=0, sticky='nsew')
        
        # Create green oval table
        self.canvas = tk.Canvas(self.table_frame, width=800, height=500, bg='darkgreen')
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.canvas.create_oval(50, 50, 750, 450, fill='green', outline='brown', width=3)
        
        # Create pot display
        self.pot_label = ttk.Label(self.table_frame, text="Pot: $0", 
                                 background='black', foreground='white')
        self.pot_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create player positions
        self.create_player_seats()
        
        # Create action buttons frame
        self.action_frame = ttk.Frame(self.main_frame, padding="10")
        self.action_frame.grid(row=1, column=0, sticky='ew')
        
        # Create action buttons
        self.create_action_buttons()
        
        # Create game info frame
        self.info_frame = ttk.Frame(self.main_frame, padding="10")
        self.info_frame.grid(row=0, column=1, sticky='ns')
        self.create_game_info()

    def create_player_seats(self):
        """Create all player seat positions"""
        # Button position (bottom)
        self.btn_seat = self.create_player_seat("Player_0 (BTN)\n$10,000", 0.5, 0.9)
        
        # SB position (bottom left)
        self.sb_seat = self.create_player_seat("Player_1 (SB)\n$9,950", 0.2, 0.75)
        
        # BB position (left)
        self.bb_seat = self.create_player_seat("Player_2 (BB)\n$9,900", 0.1, 0.5)
        
        # UTG position (top left)
        self.utg_seat = self.create_player_seat("Player_3 (UTG)\n$10,000", 0.2, 0.25)
        
        # UTG+1 position (top)
        self.utg1_seat = self.create_player_seat("Player_4 (UTG+1)\n$10,000", 0.5, 0.1)

    def create_player_seat(self, text, relx, rely):
        """Create a single player seat"""
        frame = ttk.Frame(self.table_frame)
        frame.place(relx=relx, rely=rely, anchor='center')
        
        label = ttk.Label(frame, text=text, background='black', 
                         foreground='white', padding=5)
        label.pack()
        
        return frame

    def create_action_buttons(self):
        """Create all action buttons"""
        # Create buttons
        self.fold_btn = ttk.Button(self.action_frame, text="Fold", 
                                 command=self.fold_action)
        self.fold_btn.pack(side='left', padx=5)
        
        self.check_btn = ttk.Button(self.action_frame, text="Check", 
                                  command=self.check_action)
        self.check_btn.pack(side='left', padx=5)
        
        self.call_btn = ttk.Button(self.action_frame, text="Call", 
                                 command=self.call_action)
        self.call_btn.pack(side='left', padx=5)
        
        # Create raise frame with button and entry
        raise_frame = ttk.Frame(self.action_frame)
        raise_frame.pack(side='left', padx=5)
        
        self.raise_amount = tk.StringVar(value="0")
        self.raise_entry = ttk.Entry(raise_frame, textvariable=self.raise_amount, 
                                   width=10)
        self.raise_entry.pack(side='left', padx=2)
        
        self.raise_btn = ttk.Button(raise_frame, text="Raise", 
                                  command=self.raise_action)
        self.raise_btn.pack(side='left', padx=2)

    def create_game_info(self):
        """Create game information display"""
        ttk.Label(self.info_frame, text="Game Information", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.street_label = ttk.Label(self.info_frame, text="Street: Pre-flop")
        self.street_label.pack(pady=2)
        
        self.blinds_label = ttk.Label(self.info_frame, text="Blinds: 50/100")
        self.blinds_label.pack(pady=2)
        
        self.current_bet_label = ttk.Label(self.info_frame, text="Current Bet: $0")
        self.current_bet_label.pack(pady=2)

    def update_pot(self, amount):
        """Update pot display"""
        self.pot_label.config(text=f"Pot: ${amount}")

    def update_player_seat(self, name, stack, position, active, is_current):
        """Update a player's seat information"""
        seat_text = f"{name}\n${stack}"
        if position == 0:
            seat_text += " (BTN)"
        elif position == 1:
            seat_text += " (SB)"
        elif position == 2:
            seat_text += " (BB)"
            
        # Add visual indication for current player
        background = 'yellow' if is_current else 'black'
        foreground = 'black' if is_current else 'white'
        
        # Get the appropriate seat based on position
        seat = None
        if position == 0:
            seat = self.btn_seat
        elif position == 1:
            seat = self.sb_seat
        elif position == 2:
            seat = self.bb_seat
        elif position == 3:
            seat = self.utg_seat
        elif position == 4:
            seat = self.utg1_seat

        if seat and seat.winfo_children():
            seat.winfo_children()[0].config(
                text=seat_text, 
                background=background, 
                foreground=foreground
            )

    def update_game_info(self, street, current_bet, big_blind):
        """Update game information display"""
        self.street_label.config(text=f"Street: {street}")
        self.blinds_label.config(text=f"Blinds: {big_blind//2}/{big_blind}")
        self.current_bet_label.config(text=f"Current Bet: ${current_bet}")

    def enable_valid_actions(self, valid_actions):
        """Enable only valid action buttons"""
        self.fold_btn.state(['!disabled'] if 'fold' in valid_actions else ['disabled'])
        self.check_btn.state(['!disabled'] if 'check' in valid_actions else ['disabled'])
        self.call_btn.state(['!disabled'] if 'call' in valid_actions else ['disabled'])
        self.raise_btn.state(['!disabled'] if any(a.startswith('raise') for a in valid_actions) else ['disabled'])

    def fold_action(self):
        self.controller.handle_player_action("fold")
        
    def check_action(self):
        self.controller.handle_player_action("check")
        
    def call_action(self):
        self.controller.handle_player_action("call")
        
    def raise_action(self):
        try:
            amount = int(self.raise_amount.get())
            self.controller.handle_player_action("raise", amount)
        except ValueError:
            print("Please enter a valid raise amount")

def main():
    root = tk.Tk()
    app = PokerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()