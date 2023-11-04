import random
import uuid
import time
import socket
import select
from collections import deque
from typing import Optional
from _thread import start_new_thread
import logging
import os

HEADERLENGTH = 10
IP = "127.0.0.1"
PORT = 12121

log = logging.getLogger(__name__)
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "DEBUG"),
    format="%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

numbers = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
suits = ("♥", "♠", "♦", "♣")


def main():
    # start poker engine
    pokerEngine = Main()

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to port on IP, leave IP blank to allow
    # connections from other local computers
    server_socket.bind((IP, PORT))
    server_socket.listen(20)

    sockets_list = [server_socket]

    clients = {}

    print("starting up on %s port %s" % (IP, PORT))

    # Listen for incoming connections

    while True:
        # Wait for a connection
        print("waiting for a connection")
        read_sockets, _, exception_sockets = select.select(
            sockets_list, [], sockets_list
        )

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = recieve_message(client_socket)

                if user is False:
                    continue

                sockets_list.append(client_socket)

                clients[client_socket] = user

                player = Player(user["data"].decode("utf-8"), client_socket)
                gameID = pokerEngine.add_player_to_random_game(player)
                print(
                    f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} Adding them to game on thread {gameID}"
                )

            else:
                message = recieve_message(notified_socket)

                if message is False:
                    print(
                        f"Closed connection from  {clients[notified_socket]['data'].decode('utf-8')}"
                    )
                    sockets_list.remove(notified_socket)
                    pokerEngine.remove_player(notified_socket)
                    del clients[notified_socket]
                    continue

                user = clients[notified_socket]
                print(
                    f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}"
                )

                for game in pokerEngine.games:
                    for player in game.players:
                        if player.player_socket == notified_socket:
                            player.action = message["data"].decode("utf-8")

                """
                #sends to all but sender
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                """

            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]


def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8"))
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except Exception as e:
        print("General Error: ", e)
        return False


"""     
        try:
            print('connection from', client_address)

            # Receive the name and create player and return player object back
            while True:
                data = connection.recv(16)
                print('received "%s"' % data)
                if data:
                    print('creating player "%s"' % data.decode('utf-8'))
                    player = Player(data.decode('utf-8'))
                    gameID = pokerEngine.addPlayerToRandomGame(player)
                    gameMsg = pickle.dumps(gameID)
                    gameMsg = bytes(f"{len(gameMsg):<{HEADERSIZE}}",'utf-8') + gameMsg
                    connection.sendall(gameMsg)
                    print(f'{player} is joining {gameID}')
                    player.joinGame()
                    break
                else:
                    print('no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()
"""


class Main:
    MAXGAMEPLAYERS = 8
    active = 0

    def __init__(self):
        self.games = []
        self.active = 1

    # Returns Gameid which player was added to
    def add_player_to_random_game(self, player):
        # If no games currently in play then create one
        if len(self.games) == 0:
            return start_new_thread(self.create_game_and_add_player, (player,))
        # Else check if games are full
        else:
            gamesFull = 1
            for game in self.games:
                if len(game.get_players()) < self.MAXGAMEPLAYERS:
                    game.add_player(player)
                    print("You are playing in game %d", game.get_game_id())
                    gamesFull = 0
                    return game.get_game_id()

            # If games full then create new game and add player
            if gamesFull == 1:
                return start_new_thread(self.create_game_and_add_player, (player,))

    def create_game_and_add_player(self, player):
        game = Game()
        self.games.append(game)
        game.add_player(player)
        game.play_game()

    def remove_player(self, socket_remove):
        for game in self.games:
            for player in game.players:
                if player.player_socket == socket_remove:
                    game.remove_player(player)

    def remove_game(self, game):
        self.games.remove(game)

    # TODO: Merge games if there's > 2 games with not many numbers
    def merge_games(self):
        pass


class Card:
    def __init__(self, number, suit):
        if number in numbers and suit in suits:
            self.number = number
            self.suit = suit
            self.rank = numbers.index(number)
            self.card = (number, suit)
        elif number == "-1" and suit == "-1":
            # Dummy card
            self.rank = -1
        else:
            raise Exception("Card not a standard playing card!")

    def __str__(self):
        return str(self.card)

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank


class Deck:
    def __init__(self):
        self.deck = []

        for number in numbers:
            for suit in suits:
                self.deck.append(Card(number, suit))

        random.shuffle(self.deck)

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def pop(self):
        return self.deck.pop()


class Player:
    def __init__(self, name, player_socket):
        self.playerid = uuid.uuid1()
        self.player_socket: socket.socket = player_socket
        self.name = name
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
            time.sleep(1)
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


class Game:
    def __init__(self):
        self.players: list[Player] = []
        self.gameId = uuid.uuid1()
        self.gameInPlay: bool = False
        self.buttonPlayerIndex = 0
        self.activePlayers: list[Player] = []
        self.currentPot = 0
        self.started = 0
        self.handNumber = 0
        self.blind_amount = 20
        self.minimumStake = self.blind_amount

    def add_player(self, player):
        self.players.append(player)
        player.game = self
        player.player_socket.send(
            str("GAMEID: " + str(self.gameId)).encode("utf-8"))

        if self.gameInPlay == 1:
            player.player_socket.send(
                str("Game In Play please wait until next round starts!").encode("utf-8")
            )

    def remove_player(self, player):
        self.players.remove(player)
        self.send_msg_to_all_players(f"{player} left the table!")

    def get_players(self):
        return self.players

    def get_active_players(self):
        return self.activePlayers

    def get_game_id(self):
        return self.gameId

    def send_msg_to_all_players(self, msg):
        [player.send_msg_to_player(msg + "\n") for player in self.players]

    def player_fold(self, player):
        self.activePlayers.remove(player)
        self.send_msg_to_all_players(f"{player} folded")
        self.is_hand_won()

    def player_call(self, player):
        self.add_chips_to_pot(player, self.minimumStake - player.currentStake)
        self.send_msg_to_all_players(f"{player} called")

    # def player_raise(self, player, amount):
    #     self.send_msg_to_all_players(f"{player} raised {amount}")

    def take_blinds(self):
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
                time.sleep(4)

            while len(self.players) >= 2:
                self.send_msg_to_all_players(
                    f"Searching for players pending to join game...")
                time.sleep(3)
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
        self.table = []
        self.game: Game = game
        self.deck = Deck()

    def deal_players(self):
        # First card
        for player in self.game.players:
            player.add_card_to_hand(self.deck.pop())
        # Second card
        for player in self.game.players:
            player.add_card_to_hand(self.deck.pop())

    def deal_river(self):
        self.deck.pop()
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())

    def deal_turn(self):
        self.deck.pop()
        self.table.append(self.deck.pop())

    def deal_flop(self):
        self.deck.pop()
        self.table.append(self.deck.pop())

    def reset(self):
        [player.reset_hand() for player in self.game.players]


if __name__ == "__main__":
    main()
