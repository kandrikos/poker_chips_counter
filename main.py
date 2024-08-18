from player import Player
from hand import Hand

# def assign_positions(players):
#     """Assigns positions to players, including Button, SB, and BB."""
#     num_players = len(players)
#     button_position = 0  # Start with the button at position 1

#     for i in range(num_players):
#         position = (button_position + i) % num_players + 1
#         if position == 1:
#             players[i].position = "Button"
#         elif position == 2:
#             players[i].position = "SB"
#         elif position == 3:
#             players[i].position = "BB"
#         else:
#             players[i].position = position

# def play_preflop(hand):
#     """Simulates the pre-flop betting round."""
#     # Collect blinds (assuming SB and BB are already assigned)
#     for player in hand.activePlayers:
#         if player.position == "SB":
#             player.make_action("bet", hand.big_blind // 2, "pre-flop", hand)  # Small blind
#         elif player.position == "BB":
#             player.make_action("bet", hand.big_blind, "pre-flop", hand)  # Big blind

#     # Get actions from other players (you'll need to implement this part)
#     # ...

def play_flop_turn_or_river(hand, street_name):
    """Simulates the flop, turn, or river betting round."""
    hand.pot.new_betting_round()  # Reset current round contributions
    hand.current_bet = 0

    # Get actions from players (you'll need to implement this part)
    # ...

def play_simple_hand():
    """Plays a simplified hand of poker."""
    players = [
        Player("A", None, 1000),
        Player("B", None, 1000),
        Player("C", None, 1000),
        Player("D", None, 1000),
        Player("E", None, 1000),
        Player("F", None, 1000)
    ]
    # assign_positions(players)

    hand = Hand(players)
    hand.start_new_hand()  # You'll need to implement this to reset player states

    # play_preflop(hand)
    play_flop_turn_or_river(hand, "flop")
    play_flop_turn_or_river(hand, "turn")
    # No betting on the river in this simplified version

    # Determine the winner and distribute the pot (you'll need to implement this)
    # ...

if __name__ == "__main__":
    play_simple_hand()


# import unittest

# class TestPot(unittest.TestCase):
#     def test_collect_bet_updates_both_contributions(self):
#         pot = Pot()
#         player = Player("Alice", 1, 1000)
#         pot.collect_bet(player, 100)
#         self.assertEqual(pot.total, 100)
#         self.assertEqual(pot.contributions[player], 100)
#         self.assertEqual(pot.current_round_contributions[player], 100)

#     def test_new_betting_round_resets_current_round_contributions(self):
#         pot = Pot()
#         player = Player("Bob", 2, 1000)
#         pot.collect_bet(player, 50)
#         pot.new_betting_round()
#         self.assertEqual(pot.total, 50)  # Total remains unchanged
#         self.assertEqual(pot.contributions[player], 50)
#         self.assertEqual(pot.current_round_contributions, {})  # Current round contributions reset

# class TestHandAndPotIntegration(unittest.TestCase):
#     def test_new_betting_round_called_on_next_street(self):
#         players = [Player("Charlie", 1, 1000)]
#         hand = Hand(players)
#         # Mock the next_street method to track if new_betting_round is called
#         hand.next_street = lambda: hand.pot.new_betting_round() 
#         hand.next_street()
#         self.assertEqual(hand.pot.current_round_contributions, {})

# if __name__ == '__main__':
#     unittest.main()