import random

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
        self.name = name
        self.chips = 1000
        self.hand = []


    def addCardtoHand(self, card):
        self.hand.append(card)


class Game():
    def __init__(self):
        self.players = []


    def addPlayer(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

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





