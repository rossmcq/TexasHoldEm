'''from TexasHoldEm import Hand
from TexasHoldEm import Game
from TexasHoldEm import Player
from TexasHoldEm import Main'''
import socket
import sys
import pickle

def main():
    if input('Do you want to join a game of Texas Hold Em? [Y/N]') == 'Y':
        HEADERSIZE = 10

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 12121)
        print('connecting to %s port %s' % server_address)
        sock.connect(server_address)

        #Create player
        newPlayer = input('What is your name?')

        try:

            # Send data
            message = 'This is the message.  It will be repeated.'
            print('sending Player name "%s"' % newPlayer)
            sock.sendall(newPlayer.encode('utf-8'))

            while True:
                full_data = b''
                new_data = True

                while True:
                    data = sock.recv(16)
                    if new_data:
                        print('received "%s"' % data)
                        print(f'new message length: {data[:HEADERSIZE]}')
                        datalen = int(data[:HEADERSIZE])
                        new_data = False

                    full_data += data

                    if len(full_data) - HEADERSIZE == datalen:
                        print('Full object recieved')
                        print(full_data[HEADERSIZE:])

                        d = pickle.loads(full_data[HEADERSIZE:])
                        print('You are playing in game ', d)

                        new_data = True
                        full_data = b''

                    print('Your Player Profile is: ', full_data)

        finally:
            print('closing socket')
            sock.close()

#        while(len(pokerEngine.games) > 0):
#            newPlayer.joinGame()
    else:
        print('OK Bye!')





if __name__== "__main__":
    main()