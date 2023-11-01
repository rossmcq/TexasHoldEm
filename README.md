# TexasHoldEm
TexasHoldEm card game simulator that runs in Terminal
Currently doing a bit of a tidy up after it not beeing looked at since 2019

# Run the game
1) To start run `TexasHoldemEngine.py` to start the game engine
2) Each player can connect to the game engine by running `TexasHoldEmUser.py` in a terminal.
3) More than one player needed to start the game. So you may need to repeat step 2 in a separate terminal.

## Limitations
1) Only can be run on 1 machine with all players sharing that machine. 

##TODO: 
1) Testing unit and E2E
2) Game Logic:

    i) Betting/Raising
    
    ii) Calculate Winning Hand (currently just highest card wins)
    
    iii) merge games if not many players

3) Logging 
4) HeaderString in messages
5) Alerting
6) User log in/retain chips
7) UI (I made a start refactoring to a microservice architechture with UI latest commits are on my gitlab https://gitlab.com/mcanal/texasholdem)
8) Typehints
9) Split into logical files
