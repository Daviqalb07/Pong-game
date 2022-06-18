import threading
import pygame as pg
import time
import socket
import pickle
import sys

from ball import *
from player import *
from properties import *


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

pg.init()
pg.display.init()

window_size = (TABLE_WIDTH, TABLE_HEIGHT)
table = pg.display.set_mode(window_size)
table.fill(TABLE_COLOR)
pg.display.set_caption("Pong Game")

ball_x = TABLE_WIDTH/2
ball_y = TABLE_HEIGHT/2

opponent_x = int()
opponent_y = int()

send_collided = False
send_not_collided = False

while True:
    number = int(client.recv(2048).decode())
    print(number)
    if number in [1, 2]:
        break
    else:
        print("Máximo atingido!")
        sys.exit(1)

while client.recv(2048).decode() != "start":
    pass
time.sleep(1)
player = Player(number)


def main():
    threading.Thread(target= thread_recv).start()
    threading.Thread(target= thread_send).start()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.WINDOWCLOSE:
                run = False
            else:
                pass

        table.fill(TABLE_COLOR)       
        draw_ball(ball_x, ball_y, table) 
        player.draw(table)
        print(f'opx: {opponent_x} opx: {opponent_y}')
        draw_opponent(opponent_x, opponent_y, table)

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player.up()
        elif keys[pg.K_s]:
            player.down()
        

        time.sleep(1/60) # 60 fps
        pg.display.update()


def thread_send():
    global send_collided, send_not_collided, player, client
    while True:
        client.send(player.player_info().encode())

        if send_collided:
            client.send(f'ball-collided {1} '.encode())
            send_collided = False

        if send_not_collided:
            client.send(f'ball-collided {0} '.encode())
            send_not_collided = False


def thread_recv():
    global player, ball_x, ball_y, opponent_x, opponent_y, send_collided, send_not_collided, client

    while True:
        try:
            received = client.recv(BUFF_SIZE).decode().split(' ')

            if received[0] == 'opponent-position':
                opponent_x = int(received[1])
                opponent_y = int(received[2])

            if received[0] == 'ball':
                ball_x = int(received[1])
                ball_y = int(received[2])

                collided = [
                    player.collided_in_x(int(received[1])),
                    player.collided_in_y(int(received[2]))
                ]
                
                if all(collided):
                    send_collided = True
                elif collided[0]:
                    send_not_collided = True
        except Exception as e:
            print(e)

main()