import random
import uuid
import time
import sys
import socket
import select
import pickle

HEADERLENGTH = 10
IP = "127.0.0.1"
PORT = 12121

def main():
    #start poker engine
    pokerEngine = Main()

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Bind to port on IP, leave IP blank to allow
    #connections from other local computers
    server_socket.bind((IP, PORT))
    server_socket.listen(20)

    sockets_list = [server_socket]

    clients = {}

    print('starting up on %s port %s' % (IP, PORT))

    # Listen for incoming connections

    while True:
        # Wait for a connection
        print('waiting for a connection')
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = recieve_message(client_socket)

                if user is False:
                    continue

                sockets_list.append(client_socket)

                clients[client_socket] = user

                player = Player(user['data'].decode('utf-8'))
                gameID = pokerEngine.addPlayerToRandomGame(player)
                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} Adding them to game {gameID}")

                client_socket.send(str(gameID).encode('utf-8'))

            else:
                message = recieve_message(notified_socket)

                ##logic to send messsage to game

                if message is False:
                    print(f"Closed connection from  {clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue

                user = clients[notified_socket]
                print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

                #sends to all but sender
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

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

'''     
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
'''

class Main:
    MAXGAMEPLAYERS = 8
    active = 0

    def __init__(self):
        self.games = []
        self.active = 1

    def getMain(self):
        return self

    def createGame(self):
        game = Game()
        self.games.append(game)

    #Returns Gameid which player was added to
    def addPlayerToRandomGame(self, player):
        #If no games currently in play then create one
        if len(self.games) == 0:
            return self.createGameAndAddPlayer(player)
        # Else check if games are full
        else:
            gamesFull = 1
            for game in self.games:
                if len(game.getPlayers()) < self.MAXGAMEPLAYERS:
                    game.addPlayer(player)
                    print('You are playing in game %d', game.getGameId())
                    gamesFull = 0
                    return game.getGameId()

            # If games full then create new game and add player
            if gamesFull == 1:
                return self.createGameAndAddPlayer(player)

    def createGameAndAddPlayer(self, player):
        game = Game()
        self.games.append(game)
        game.addPlayer(player)
        return game.gameId

    def removeGame(self, game):
        self.games.remove(game)

    def mergeGames(self):
        pass



class Deck:

    def __init__(self):
        numbers = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
        suits = ['♥','♠','♦','♣']

        self.deck = []

        for number in numbers:
            for suit in suits:
                self.deck.append((number, suit))

        random.shuffle(self.deck)

    def __str__(self):
        return str(self.deck)

    def pop(self):
        return self.deck.pop()


class Player():
    def __init__(self, name):
        self.playerid = uuid.uuid1()
        self.name = name
        self.chips = 1000
        self.hand = []
        self.game = 0


    def __str__(self):
        return str(self.name) + str(self.chips)

    def getPlayerName(self):
        return self.name

    def getGame(self):
        return self.game

    def addCardtoHand(self, card):
        self.hand.append(card)

    def resetHand(self):
        self.hand = []

    def getPlayerID(self):
        return self.playerid

    def joinGame(self):
        if self.game.gameInPlay == 1:
            print('Game currently in progress please wait...')
            while self.game.gameInPlay == 1:
                time.sleep(1)
        self.game.playGame(self)

    def takeBet(self):
        input('Do you want to [R]aise, [C]all or [F]lop?')

class Game():
    def __init__(self):
        self.players = []
        self.gameId = uuid.uuid1()
        self.gameInPlay = 0

    def addPlayer(self, player):
        self.players.append(player)
        player.game = self

    def getPlayers(self):
        return self.players

    def getGameId(self):
        return self.gameId

    def playGame(self, player):
        self.gameInPlay = 1
        hand = Hand(self)

        print('Players in this game ', self.getPlayers())

        hand.dealPlayers()
        print('player.hand', player.hand)
        self.takeBets(hand)
        hand.dealRiver()
        print('hand.table - River', hand.table)
        self.takeBets(hand)
        '''
        hand.dealTurn()
        print('hand.table - Turn', hand.table)
        self.takeBets(hand)
        hand.dealFlop()
        print('hand.table - Flop', hand.table)
        self.takeBets(hand)
        '''
        #reset players hands
        hand.reset()

        print('player.hand - after reset', player.hand)
        print('**NEW GAME**')

        self.gameInPlay = 0


    def takeBets(self, hand):
        for player in hand.game.players:
            player.takeBet()






class Hand():

    def __init__(self, game):
        self.table = []
        self.game = game
        self.deck = Deck()


    def betting(self):
        pass

    def dealPlayers(self):
        # First card
        for player in self.game.players:
            player.addCardtoHand(self.deck.pop())
        #Second card
        for player in self.game.players:
            player.addCardtoHand(self.deck.pop())

    def dealRiver(self):
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())
        self.table.append(self.deck.pop())

    def dealTurn(self):
        self.table.append(self.deck.pop())

    def dealFlop(self):
        self.table.append(self.deck.pop())

    def reset(self):
        for player in self.game.players:
            player.resetHand()

    def getWinner(self):
        pass



if __name__== "__main__":
    main()

