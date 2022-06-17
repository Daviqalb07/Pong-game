import socket
from properties import *

players = []

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(e)

    try:
        server.bind((SERVER_IP, SERVER_PORT))
        print("Server's status: ON!")
    except socket.gaierror as e:
        print(e)
    except socket.error as e:
        print(e)

    server.listen(2)

    while True:
        player, _ = server.accept()
        players.append(player)
        player.send(str(len(players)).encode('utf-8'))

main()