from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from _thread import start_new_thread
import logging
import os

# Custom libraries
from game_engine.poker_logic import Game, Player

HEADERLENGTH = 10
IP = "127.0.0.1"
PORT = 12121

log = logging.getLogger(__name__)
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "DEBUG"),
    format="%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # start poker engine
    pokerEngine = Main()

    # Create a TCP/IP socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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
        read_sockets, _, exception_sockets = select(sockets_list, [], sockets_list)

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
                    f"Accepted new connection from {client_address[0]}:{client_address[1]} "
                    f"username:{user['data'].decode('utf-8')} Adding them to game on thread {gameID}"
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
                    f"Received message from {user['data'].decode('utf-8')}"
                    f": {message['data'].decode('utf-8')}"
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


def recieve_message(client_socket: socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8"))
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except Exception as e:
        print("General Error: ", e)
        return False


class Main:
    MAXGAMEPLAYERS = 8
    active: bool = False

    def __init__(self):
        self.games: list[Game] = []
        self.active: bool = True

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


if __name__ == "__main__":
    main()
