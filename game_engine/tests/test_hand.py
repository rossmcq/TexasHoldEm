import unittest
from unittest.mock import Mock, call

from game_engine.deck import Card
from game_engine.poker_logic import Hand
from game_engine.tests.test_config import test_deck

# command to run tests:
# python3 -m unittest game_engine/tests/test_hand.py -v


class HandTest(unittest.TestCase):
    def setUp(self):
        mock_game = Mock()
        self.mock_player_1 = Mock()
        self.mock_player_2 = Mock()
        mock_game.players: list[Mock] = [self.mock_player_1, self.mock_player_2]
        self.hand = Hand(mock_game)

    def test_hand_burn_then_deal_one_card(self):
        self.hand.deck = test_deck.copy()
        self.hand.burn_then_deal_one_card()
        self.assertEqual(self.hand.table, [Card("A", "♣")])

    def test_hand_deal_players(self):
        self.hand.deck = test_deck.copy()
        self.hand.deal_players()
        self.mock_player_1.add_card_to_hand.assert_has_calls(
            [call(Card("3", "♣")), call(Card("5", "♠"))]
        )

        self.mock_player_2.add_card_to_hand.assert_has_calls(
            [call(Card("A", "♣")), call(Card("K", "♦"))]
        )

    def test_hand_reset(self):
        self.hand.reset()
        self.mock_player_1.reset_hand.assert_called_once()
        self.mock_player_2.reset_hand.assert_called_once()


if __name__ == "__main__":
    unittest.main()
