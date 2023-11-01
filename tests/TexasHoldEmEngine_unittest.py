import unittest
from unittest.mock import Mock

import TexasHoldEmEngine

# command to run tests:
# python -m unittest tests/TexasHoldEmEngine_unittest.py -v


class DeckTest(unittest.TestCase):
    def test_deck_contains_52_cards(self):
        deck = TexasHoldEmEngine.Deck()

        self.assertEqual(len(deck), 52)
