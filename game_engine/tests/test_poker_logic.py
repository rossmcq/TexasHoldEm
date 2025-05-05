import unittest
from unittest.mock import Mock, sentinel

from game_engine.poker_logic import PokerPlayer, PokerGame

# command to run tests:
# python3 -m unittest game_engine/tests/test_deck.py -v


class PlayerTest(unittest.TestCase):
    def test_player_initation(self):
        player = PokerPlayer("Ross", sentinel)

        self.assertEqual(player.name, "Ross")
        self.assertEqual(player.player_socket, sentinel)
        self.assertEqual(player.game, None)

        self.assertEqual(player.chips, 1000)
        self.assertEqual(player.hand, [])
        self.assertEqual(player.timeout, 0)
        self.assertEqual(player.action, "u")
        self.assertEqual(player.currentStake, 0)

    def test_player_increase_chips(self):
        player = PokerPlayer("Ross", sentinel)
        player.increase_chips(100)
        self.assertEqual(player.chips, 1100)

    def test_player_decrease_chips(self):
        player = PokerPlayer("Ross", sentinel)
        player.decrease_chips(100)
        self.assertEqual(player.chips, 900)

    def test_player_place_bet(self):
        player = PokerPlayer("Ross", sentinel)
        player.place_bet(100)
        self.assertEqual(player.chips, 900)
        self.assertEqual(player.currentStake, 100)


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
