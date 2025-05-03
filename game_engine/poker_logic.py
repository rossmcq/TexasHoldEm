# Standard
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional
from uuid import uuid4, UUID
from time import sleep
from socket import socket

# Custom
from game_engine.deck import Deck, Card


class Player:
    def __init__(self, name, player_socket):
        self.playerid: UUID = uuid4()
        self.player_socket: socket = player_socket
        self.name: str = name


class PokerPlayer(Player):
    def __init__(self, name, player_socket):
        super().__init__(name, player_socket)
        self.chips = 1000
        self.hand = []
        self.game: Optional[Game] = None
        self.timeout = 0
        self.action = "u"
        self.currentStake = 0

    def __str__(self):
        return f"{self.name} {str(self.chips)}"

    def get_player_name(self):
        return self.name

    def get_game(self):
        return self.game

    # TODO: Header String in messages
    def send_msg_to_player(self, msg: str):
        try:
            self.player_socket.send(msg.encode("utf-8"))
        except ConnectionResetError as e:
            print("Player disconnected still pending remove")
            print(e)

    def add_card_to_hand(self, card):
        self.hand.append(card)
        self.send_msg_to_player(str(card))

    def reset_hand(self):
        self.hand = []
        self.currentStake = 0

    def take_bet(self):
        self.send_msg_to_player("Do you want to [C]all or [F]old?")
        self.action = "u"
        self.timeout = 20

        while self.timeout > 0 and self.action == "u":
            sleep(1)
            self.timeout -= 1

        if self.timeout == 0:
            print(f"{self.name} timed out!")
            self.fold()
        elif self.action.lower() == "f":
            self.fold()
        elif self.action.lower() in ("c", ""):
            self.call()
        # elif self.action.lower() == 'r':
        #     self.raise_hand()
        # elif self.action is int:
        #     self.raise_hand(self.action)
        else:
            raise Exception("Unhandled player action!")

    def fold(self):
        if self.game:
            self.game.player_fold(self)
        self.currentStake = 0

    def call(self):
        if self.game:
            self.game.player_call(self)

    # # TODO: Raise hand logic
    # def raise_hand(self, chips):
    #     self.chips -= chips
    #     self.game.player_raise(self, chips)


class Game(ABC):
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.gameId: UUID = uuid4()
        self.gameInPlay: bool = False

    @abstractmethod
    def add_player(self, player: Player) -> None:
        pass

    @abstractmethod
    def remove_player(self, player: Player) -> None:
        pass

    @abstractmethod
    def send_msg_to_all_players(self, msg: str) -> None:
        pass

    # Make property?
    def game_id(self) -> UUID:
        return self.gameId

    def get_players(self) -> list[Player]:
        return self.players


class PokerGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.buttonPlayerIndex = 0
        self.activePlayers: list[Player] = []
        self.currentPot = 0
        self.started = 0
        self.handNumber = 0
        self.blind_amount = 20
        self.minimumStake = self.blind_amount

    def add_player(self, player: Player) -> None:
        self.players.append(player)
        player.game = self
        player.player_socket.send(str("GAMEID: " + str(self.gameId)).encode("utf-8"))

        if self.gameInPlay == 1:
            player.player_socket.send(
                str("Game In Play please wait until next round starts!").encode("utf-8")
            )

    def remove_player(self, player) -> None:
        self.players.remove(player)
        self.activePlayers.remove(player)
        self.send_msg_to_all_players(f"{player} left the table!")
        self.is_hand_won()

    def get_active_players(self) -> list[Player]:
        return self.activePlayers

    def send_msg_to_all_players(self, msg) -> None:
        [player.send_msg_to_player(msg + "\n") for player in self.players]

    def player_fold(self, player) -> None:
        self.activePlayers.remove(player)
        self.send_msg_to_all_players(f"{player} folded")
        self.is_hand_won()

    def player_call(self, player) -> None:
        self.add_chips_to_pot(player, self.minimumStake - player.currentStake)
        self.send_msg_to_all_players(f"{player} called")

    # def player_raise(self, player, amount):
    #     self.send_msg_to_all_players(f"{player} raised {amount}")

    def take_blinds(self) -> None:
        self.add_chips_to_pot(
            self.players[(self.buttonPlayerIndex + 1) % len(self.players)],
            int(self.blind_amount * 0.5),
        )

        self.add_chips_to_pot(
            self.players[(self.buttonPlayerIndex + 2) % len(self.players)],
            self.blind_amount,
        )

    def add_chips_to_pot(self, player, amount):
        player.chips -= amount
        player.currentStake += amount
        self.currentPot += amount

    def play_game(self):
        while True:
            while len(self.players) < 2:
                self.send_msg_to_all_players(
                    f"You are the only player in the game, waiting for others to join..."
                )
                sleep(4)

            while len(self.players) >= 2:
                self.send_msg_to_all_players(
                    f"Searching for players pending to join game..."
                )
                sleep(3)
                self.handNumber += 1
                self.send_msg_to_all_players(f"Hand number {self.handNumber}")
                self.gameInPlay = True

                self.take_blinds()

                # Rotate players
                self.activePlayers = deque(self.players)
                self.activePlayers.rotate(-(1 + self.buttonPlayerIndex))
                hand = Hand(self)

                # Tell players whose in this round
                game_players = ""
                for player in self.get_players():
                    if (
                        player
                        == self.get_players()[
                            (self.buttonPlayerIndex + 1) % len(self.get_players())
                        ]
                    ):
                        game_players += str(player) + " SMALL BLIND\n"
                    elif (
                        player
                        == self.get_players()[
                            (self.buttonPlayerIndex + 2) % len(self.get_players())
                        ]
                    ):
                        game_players += str(player) + " BIG BLIND\n"
                    elif player == self.get_players()[self.buttonPlayerIndex]:
                        game_players += str(player) + " BUTTON\n"

                self.send_msg_to_all_players(game_players)

                hand.deal_players()

                self.take_bets()

                if self.gameInPlay:
                    hand.deal_river()
                    self.send_msg_to_all_players(
                        f"River - {[(card.number, card.suit) for card in hand.table]}"
                    )
                    self.take_bets()

                if self.gameInPlay:
                    hand.deal_turn()
                    self.send_msg_to_all_players(
                        f"Turn - {[(card.number, card.suit) for card in hand.table]}"
                    )
                    self.take_bets()

                if self.gameInPlay:
                    hand.deal_flop()
                    self.send_msg_to_all_players(
                        f"Flop - {[(card.number, card.suit) for card in hand.table]}"
                    )
                    self.take_bets()

                    hand_winner = self.calc_hand_winner()
                    self.hand_winner(hand_winner)
                    self.gameInPlay = False

                # reset players hands
                hand.reset()

                # move button player on
                if len(self.get_players()) > 0:
                    self.buttonPlayerIndex = (self.buttonPlayerIndex + 1) % len(
                        self.get_players()
                    )

                # print('player.hand - after reset', player.hand)
                print("**END OF HAND**")

    def is_hand_won(self):
        if len(self.activePlayers) == 1:
            self.hand_winner([self.activePlayers[0]])
            self.gameInPlay = False

    def take_bets(self):
        self.send_msg_to_all_players("POT: " + str(self.currentPot))
        for player in self.activePlayers.copy():
            if self.gameInPlay:
                player.take_bet()

    # TODO: Calculate hand winner correctly
    def calc_hand_winner(self):
        # For now set player with the highest card to be winner
        highest_card = Card("-1", "-1")
        winning_player = []
        for player in self.players:
            for card in player.hand:
                if card > highest_card:
                    highest_card = card
                    winning_player = [player]
                elif card == highest_card:
                    winning_player.append(player)
        return winning_player

    def hand_winner(self, hand_winner):
        if len(hand_winner) == 1:
            hand_winner[0].chips += self.currentPot
            self.send_msg_to_all_players(f"Winner is {str(hand_winner[0])}")
        elif len(hand_winner) > 1:
            for player in hand_winner:
                player.chips += int(self.currentPot / len(hand_winner))
            self.send_msg_to_all_players(
                f"Split pot {[str(player) for player in hand_winner]}"
            )

        self.currentPot = 0
        self.minimumStake = self.blind_amount


# Dealer Class
class Hand:
    def __init__(self, game):
        self.table: list[Card] = []
        self.game: Game = game
        self.deck: Deck = Deck()

    def deal_players(self):
        # First card
        for player in self.game.players:
            player.add_card_to_hand(self.deck.pop())
        # Second card
        for player in self.game.players:
            player.add_card_to_hand(self.deck.pop())

    def deal_river(self):
        self.burn_card()
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())

    def deal_turn(self):
        self.burn_then_deal_one_card()

    def deal_flop(self):
        self.burn_then_deal_one_card()

    def burn_then_deal_one_card(self):
        self.burn_card()
        self.table.append(self.deck.pop())

    def burn_card(self):
        self.deck.pop()

    def reset(self):
        [player.reset_hand() for player in self.game.players]
