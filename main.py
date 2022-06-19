import threading
import pygame as pg
import time
import socket
import sys

from ball import *
from player import *
from properties import *

def thread_send():
    global player, client
    while True:
        client.send(player.player_info().encode())


def thread_recv():
    global client, ball_x, ball_y, opponent_x, opponent_y

    while True:
        try:
            received = client.recv(BUFF_SIZE).decode().split(' ')

            if received[0] == 'opponent-position':
                opponent_x = int(received[1])
                opponent_y = int(received[2])

            if received[0] == 'ball':
                ball_x = int(received[1])
                ball_y = int(received[2])
            
            if received[0] == 'goal':
                print("\nGoal!")
                score = [int(received[1]), int(received[2])]
                print(f'Score: {score[0]} x {score[1]}')

        except Exception as e:
            print(e)


def set_window() -> pg.Surface:
    global ball_x, ball_y, opponent_x, opponent_y, player

    window_size = (TABLE_WIDTH, TABLE_HEIGHT)
    table = pg.display.set_mode(window_size)
    pg.display.set_caption("Pong Game")
    table.fill(TABLE_COLOR)
    pg.draw.line(table, PLAYER_COLOR, (TABLE_WIDTH/2, 0), (TABLE_WIDTH/2, TABLE_HEIGHT))

    player.draw(table)
    draw_opponent(opponent_x, opponent_y, table)
    draw_ball(ball_x, ball_y, table)
    return table


def get_player_number() -> int:
    try:
        number = int(client.recv(2048).decode())
        print(f"Welcome, Player {number}!")
        if number in [1, 2]:
            return number
        else:
            print("Maximun number of players reached!")
            sys.exit(1)
    except:
        pass

def preset_opponent_position(number: int):
    if number == 1:
        opponent_x = TABLE_WIDTH - PLAYER_WIDTH
    else:
        opponent_x = 0
    opponent_y= (TABLE_HEIGHT - PLAYER_HEIGHT)/2

    return opponent_x, opponent_y

def wait_start():
    print("Waiting all players...")
    while client.recv(2048).decode() != "start":
        pass
    print("Start!")
    time.sleep(1)

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    
    number = get_player_number()
    player = Player(number)
    opponent_x, opponent_y = preset_opponent_position(number)
    ball_x = TABLE_WIDTH/2
    ball_y = TABLE_HEIGHT/2    

    pg.init()
    pg.display.init()
    pg.font.init()


    table = set_window()
    wait_start()

    threading.Thread(target= thread_recv).start()
    threading.Thread(target= thread_send).start()

    run = True
    print('Score: 0 x 0')
    while run:
        for event in pg.event.get():
            if event.type == pg.WINDOWCLOSE:
                run = False
            else:
                pass

        if not run:
            pass

        table.fill(TABLE_COLOR)
        pg.draw.line(table, PLAYER_COLOR, (TABLE_WIDTH/2, 0), (TABLE_WIDTH/2, TABLE_HEIGHT))
        draw_ball(ball_x, ball_y, table) 
        player.draw(table)
        draw_opponent(opponent_x, opponent_y, table)

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player.up()
        elif keys[pg.K_s]:
            player.down()
        

        time.sleep(1/60) # 60 fps
        pg.display.update()