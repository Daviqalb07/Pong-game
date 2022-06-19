import socket
import sys
import time
import threading

from ball import Ball
from player import *
from properties import *

# Global variables with assignment
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
players = []
ball = Ball()
reflect_ball = False

# Global variables without assignment
opponents_positions = ["", ""]
score = [0, 0]
goal = False

def main():
    server_up()
    server.listen(2)
    waiting_players()

    time.sleep(1)
    
    start_game()

    time.sleep(1)
    
    threading.Thread(target= thread_recv_player, args= [0, ]).start()
    threading.Thread(target= thread_recv_player, args= [1, ]).start()
    threading.Thread(target= thread_send).start()
    
    while True:
        ball.move()
        
        ball_y = ball.get_y()
        ball_radius = ball.get_radius()
        if (ball_y - ball_radius) < 0 or ball_y + ball_radius > TABLE_HEIGHT:
            ball.reflect_y()
       
        time.sleep(1/60)


def server_up():
    global server
    try:
        server.bind((SERVER_IP, SERVER_PORT))
        print("Server's status: ON!")
    except socket.gaierror as e:
        print(e)
        sys.exit(1)
    except socket.error as e:
        print(e)
        sys.exit(1)

def waiting_players():
    global players, server
    while len(players) < 2:
        try:
            player, _ = server.accept()

            players.append(player)
            number = f'{len(players) }'
            print(f"Player {number} connected!")
            player.send(number.encode())
        except:
            print(f"Error while connecting! Players connected: {len(players)}")


def start_game():
    global players
    for p in players:
        p.send('start'.encode())
    print("Game started!")


def thread_recv_player(number: int):
    global ball, opponents_positions, players, goal

    while True:
        try:
            received = players[number].recv(BUFF_SIZE).decode().split(' ')
            # received's infos: ['type', args]
            ## if 'type' == 'player-position' => ['type', 'player_x', 'player_y'] 

            
            if received[0] == 'player-position':
                player_x = int(received[1])
                player_y = int(received[2])
                
                opponents_positions[1-number] = f'opponent-position {player_x} {player_y} '
                collided = [
                    collided_in_x(number+1, player_x, ball.get_x()),
                    collided_in_y(player_y, ball.get_y())
                ]

                if all(collided):
                    if not reflect_ball:
                        threading.Thread(target= thread_reflect_ball).start()

                elif collided[0]:
                    score[1-number] += 1
                    goal = True
                    ball = Ball()

        except Exception as e:
            pass
        
def thread_send():
    global ball, players, opponents_positions, goal

    while True:
        ball_info = ball.ball_xy_encode()
        for i, player in enumerate(players):
            player.send(ball_info.encode())
            players[i].send(opponents_positions[i].encode())
        if goal:
            for player in players:
                player.send(score_info().encode())
            goal = False

def thread_reflect_ball():
    global ball, reflect_ball
    reflect_ball = True
    ball.reflect_x()
    time.sleep(1)
    reflect_ball = False

def score_info() -> str:
    global score
    return f'goal {score[0]} {score[1]} '
    
main()