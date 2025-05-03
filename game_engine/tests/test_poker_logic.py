import unittest
from unittest.mock import Mock

from ..poker_logic import PokerPlayer, PokerGame

# command to run tests:
# python3 -m unittest game_engine/tests/test_deck.py -v


class PlayerTest(unittest.TestCase):
    def test_player_initation(self):
        player = PokerPlayer("Ross", Mock())

        self.assertEqual(player.chips, 1000)
        self.assertEqual(player.hand, [])
        self.assertEqual(player.game, None)
        self.assertEqual(player.timeout, 0)
        self.assertEqual(player.action, "u")
        self.assertEqual(player.currentStake, 0)


class PokerGameTest(unittest.TestCase):
    def test_game_initation(self):
        game_1 = PokerGame()

        self.assertEqual(game_1.players, [])
        self.assertEqual(game_1.gameInPlay, False)
        self.assertEqual(game_1.buttonPlayerIndex, 0)
        self.assertEqual(game_1.activePlayers, [])
        self.assertEqual(game_1.currentPot, 0)
        self.assertEqual(game_1.started, 0)
        self.assertEqual(game_1.handNumber, 0)
        self.assertEqual(game_1.blind_amount, 20)
        self.assertEqual(game_1.minimumStake, 20)


if __name__ == "__main__":
    unittest.main()
