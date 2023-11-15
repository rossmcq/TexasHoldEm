import unittest

from game_engine.deck import Card, Deck

# command to run tests:
# python3 -m unittest game_engine/tests/test_deck.py -v


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


if __name__ == "__main__":
    unittest.main()
