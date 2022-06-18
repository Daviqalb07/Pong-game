import socket
import pickle
import time
import threading

from ball import Ball
from properties import *

players = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = ""
player1_position = ""
player2_position = ""

ball = Ball()
def main():
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
        number = f'{len(players) }'
        print(f"Player {number} connected!")
        player.send(number.encode())

        if len(players) == 2:
            break

    time.sleep(1)
    for p in players:
        p.send(str('start').encode())
    print("Game started!")

    time.sleep(1)
    threading.Thread(target= thread_recv).start()
    threading.Thread(target= thread_send).start()
    while True:
        ball.move()
        
        ball_y = ball.get_y()
        ball_radius = ball.get_radius()
        if (ball_y - ball_radius) < 0 or ball_y + ball_radius > TABLE_HEIGHT:
            ball.reflect_y()
       
        time.sleep(1/60)


def thread_send():
    global ball, players, player1_position, player2_position

    while True:
        ball_info = ball.ball_xy_encode()
        for player in players:
            player.send(ball_info.encode())
        
        players[0].send(player2_position.encode())
        players[1].send(player1_position.encode())


def thread_recv():
    global ball, player1_position, player2_position, server, msg

    while True:
        try:
            for player in players:
                received = player.recv(BUFF_SIZE).decode().split(' ')

                if received[0] == 'ball-collided':
                    # ball collided with a player => reflect ball in x-axis
                    if bool(received[1]): 
                        ball.reflect_x()
                    # ball passed by a player => reset ball position
                    else:
                        ball = Ball()

                
                elif received[0] == 'player-position':
                    
                    if int(received[1]) == 1:
                        player1_position = f'opponent-position {received[2]} {received[3]} '

                    elif int(received[1]) == 2:
                        player2_position = f'opponent-position {received[2]} {received[3]} '

        except Exception as e:
            pass
        




main()