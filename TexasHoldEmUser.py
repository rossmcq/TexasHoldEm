from TexasHoldEm import Hand
from TexasHoldEm import Game
from TexasHoldEm import Player
from TexasHoldEm import Main

def main():
    if input('Do you want to join a game of Texas Hold Em? [Y/N]') == 'Y':
        #Create player
        newPlayer = Player(input('What is your name?'))

        if Main.active == 0:
            main = Main()
        else:
            main = Main.getMain()

        #If Game not exists then create game
        if len(main.games) == 0:
            main.createGameAndAddPlayer(newPlayer)
        #Else check if games are full
        else:
            gamesFull = 1
            for game in main.games:
                if game.getPlayers < main.MAXGAMEPLAYERS:
                    game.addPlayer(newPlayer)
                    print('You are playing in game %d', game.getGameId())
                    gamesFull = 0
                    break

            #If games full then create new game and add player
            if gamesFull == 1:
                newGame = main.createGameAndAddPlayer(newPlayer)

        while(len(main.games) > 0):
            playGame(newPlayer)

    else:
        print('OK Bye!')


#TODO: Move below logic to Hand method.
def playGame(player):
    game = player.getGame()
    hand = Hand(game)

    print('Players in this game ', game.getPlayers())

    hand.dealPlayers()
    print('player.hand', player.hand)
    takeBets(hand, player)
    hand.dealRiver()
    print('hand.table - River', hand.table)
    takeBets(hand, player)
    hand.dealTurn()
    print('hand.table - Turn', hand.table)
    takeBets(hand, player)
    hand.dealFlop()
    print('hand.table - Flop', hand.table)
    takeBets(hand, player)
    hand.reset()

    print('player.hand - after reset', player.hand)
    print('hand.table', hand.table)
    print('hand.deck', hand.deck)

def takeBets(hand, playerCurrent):
    for player in hand.game.players:
        if player.getPlayerID() == playerCurrent.getPlayerID():
            requestAction(player)

#TODO only request for the player that joined on this logic
def requestAction(player):
    input('Do you want to [R]aise, [C]all or [F]lop?')



if __name__== "__main__":
    main()