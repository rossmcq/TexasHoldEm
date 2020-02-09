import random
import uuid

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

    def createGameAndAddPlayer(self, player):
        game = Game()
        self.games.append(game)
        game.addPlayer(player)
        print('You are playing in game %d', game.gameId)

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



class Game():
    def __init__(self):
        self.players = []
        self.gameId = uuid.uuid1()

    def addPlayer(self, player):
        self.players.append(player)
        player.game = self

    def getPlayers(self):
        return str(self.players)

    def getGameId(self):
        return self.gameId



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


'''
game1 = Game()

player1 = Player('Ross')
player2 = Player('Tom')
game1.addPlayer(player1)
game1.addPlayer(player2)

hand1 = Hand(game1)
print(hand1.deck)
hand1.dealPlayers()
hand1.dealRiver()


print('player1.hand', player1.hand)
print('player2.hand', player2.hand)
print('hand1.table', hand1.table)
print('hand1.deck', hand1.deck)
'''




