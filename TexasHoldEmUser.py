import socket
import select
import errno
import sys
import logging
import os
from random import shuffle

HEADERLENGTH = 10
IP = "127.0.0.1"
PORT = 12121

log = logging.getLogger(__name__)
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "DEBUG"),
    format="%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
default_names: list[str] = ["Dave", "Scott", "Juan", "Sara", "Tracey", "Tim", "Ross"]


def main():
    if input("Do you want to join a game of Texas Hold Em? [Y/n]") in ("Y", "y", ""):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        # client_socket.setblocking(False)

        # Create player
        newPlayer = input("What is your name? ").strip()
        if newPlayer == "":
            shuffle(default_names)
            newPlayer = default_names.pop()

        if len(newPlayer) < 100:
            username = newPlayer.encode("utf-8")
        else:
            raise Exception("Username needs to be  < 100 characters")

        username_header = f"{len(username):<{HEADERLENGTH}}".encode("utf-8")
        client_socket.send(username_header + username)

        try:
            while True:
                # receive things
                return_message = client_socket.recv(1024)
                if not len(return_message):
                    print("connection closed by server")
                    sys.exit()

                decode_return_message = return_message.decode("utf-8").strip()

                print(decode_return_message)

                if decode_return_message == "Do you want to [C]all or [F]old?":
                    raiseflopcall = input(": ")
                    if raiseflopcall.lower() in ["c", "f"]:
                        raiseflopcallbytes = raiseflopcall.lower().encode("utf-8")
                        client_socket.send(username_header + raiseflopcallbytes)
                    else:
                        print("Please enter either F or C")
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("reading error ", str(e))
                sys.exit()

        except Exception as e:
            print("General error", str(e))

            sys.exit()
    else:
        print("OK Bye!")


if __name__ == "__main__":
    main()
