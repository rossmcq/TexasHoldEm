import unittest
from unittest.mock import Mock, call

from TexasHoldEmEngine import Card, Deck, Hand

# command to run tests:
# python -m unittest tests/TexasHoldEmEngine_unittest.py -v

test_deck: Deck = [
    Card("A", "♥"),
    Card("3", "♥"),
    Card("4", "♥"),
    Card("8", "♦"),
    Card("6", "♥"),
    Card("7", "♥"),
    Card("8", "♥"),
    Card("9", "♥"),
    Card("10", "♥"),
    Card("J", "♥"),
    Card("Q", "♥"),
    Card("A", "♠"),
    Card("A", "♦"),
    Card("3", "♠"),
    Card("2", "♣"),
    Card("4", "♠"),
    Card("3", "♦"),
    Card("6", "♠"),
    Card("7", "♠"),
    Card("9", "♠"),
    Card("8", "♠"),
    Card("10", "♠"),
    Card("J", "♠"),
    Card("Q", "♠"),
    Card("4", "♣"),
    Card("5", "♣"),
    Card("6", "♣"),
    Card("K", "♣"),
    Card("7", "♣"),
    Card("9", "♣"),
    Card("10", "♣"),
    Card("J", "♣"),
    Card("Q", "♣"),
    Card("K", "♠"),
    Card("2", "♥"),
    Card("2", "♦"),
    Card("4", "♦"),
    Card("8", "♣"),
    Card("5", "♦"),
    Card("6", "♦"),
    Card("K", "♥"),
    Card("7", "♦"),
    Card("10", "♦"),
    Card("9", "♦"),
    Card("2", "♠"),
    Card("5", "♥"),
    Card("J", "♦"),
    Card("Q", "♦"),
    Card("K", "♦"),
    Card("5", "♠"),
    Card("A", "♣"),
    Card("3", "♣"),
]


class DeckTest(unittest.TestCase):
    def test_deck_contains_52_cards(self):
        deck = Deck()

        self.assertEqual(len(deck), 52)


class CardTest(unittest.TestCase):
    def test_card_initation(self):
        ace_of_diamonds = Card("A", "♦")

        self.assertEqual(ace_of_diamonds.number, "A")
        self.assertEqual(ace_of_diamonds.suit, "♦")
        self.assertEqual(ace_of_diamonds.rank, 12)


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
