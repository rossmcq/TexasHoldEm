# TexasHoldEm
TexasHoldEm card game simulator
Needs some work and tidying up, 

# Run the game
1) To start run TexasHoldem.py to start the game engine
2) Users connect to the game engine by running TexasHoldEmUser.py

## Limitations
1) Only can be run on 1 machine with all players sharing that machine. 

##TODO: 
1) HeaderString in messages
2) Game Logic:

    i) Betting/Raising
    
    ii) Calculate Winning Hand (currently just highest card wins)
    
    iii) merge games if not many players

3) Logging
4) Testing
5) Alerting
6) User log in/retain chips
7) UI (I made a start refactoring to a microservice architechture with UI latest commits are on my gitlab https://gitlab.com/mcanal/texasholdem)
8) Typehints
