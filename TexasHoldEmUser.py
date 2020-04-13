import socket
import select
import errno
import sys

HEADERLENGTH = 10
IP = "127.0.0.1"
PORT = 12121

def main():
    if input('Do you want to join a game of Texas Hold Em? [Y/N]') == 'Y':

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        #client_socket.setblocking(False)

        #Create player
        newPlayer = input('What is your name?').strip()
        if len(newPlayer) < 100:
            username = newPlayer.encode('utf-8')
        else:
            raise Exception('Username needs to be  < 100 characters')

        username_header = f"{len(username):<{HEADERLENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)


        try:

            while True:
                # receive things
                return_message = client_socket.recv(1024)
                if not len(return_message):
                    print("connection closed by server")
                    sys.exit()

                print(return_message.decode('utf-8'))

                if return_message.decode('utf-8') == 'Do you want to [R]aise, [C]all or [F]lop?':
                    while True:
                        raiseflopcall = input()
                        if raiseflopcall.lower() in ['r','c','f']:
                            raiseflopcallbytes = raiseflopcall.lower().encode('utf-8')
                            client_socket.send(username_header + raiseflopcallbytes)
                            break
                        else:
                            print('Please enter either F, R or C')



                '''
                username_length = int(username_header.decode("utf-8"))
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv((HEADERLENGTH))
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                print(f"{username} > {message}")
                '''
                #print('Your Player Profile is: ', full_data)



        except IOError as e:

            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('reading error ', str(e))
                sys.exit()

        except Exception as e:

            print('General error', str(e))

            sys.exit()

#        while(len(pokerEngine.games) > 0):
#            newPlayer.joinGame()
    else:
        print('OK Bye!')





if __name__== "__main__":
    main()