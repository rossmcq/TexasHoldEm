# TexasHoldEm
TexasHoldEm card game simulator that runs in Terminal
Currently doing a bit of a tidy up after it not beeing looked at since 2019

## Run the game
1) To start run `python3 game_engine/game_lobby.py` to start the game engine
2) Each player can connect to the game engine by running `python3 game_engine/user.py` in a terminal.
3) More than one player needed to start the game. So you may need to repeat step 2 in a separate terminal.

## Limitations
1) Only can be run on 1 machine with all players sharing that machine. 

## TODO: 
1) Add more unit tests 
2) Add E2E tests 
3) Game Logic:

    i) Betting/Raising
    
    ii) Calculate Winning Hand (currently just highest card wins)
    
    iii) Merge games if possible

4) Logging 
5) HeaderString in all messages
6) User log in/retain chips
7) UI (I made a start refactoring to a microservice architechture with UI latest commits are on my gitlab https://gitlab.com/mcanal/texasholdem)
