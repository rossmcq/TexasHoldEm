import random
import uuid
import time
import sys
import socket
import pickle

def main():
    HEADERSIZE = 10

    #start poker engine
    pokerEngine = Main()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 12121)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
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
        return str(self.players)

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

