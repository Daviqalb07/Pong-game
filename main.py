import pygame as pg
import time
import socket

from ball import Ball
from player import *
from properties import *


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    pg.init()
    pg.display.init()

    while True:
        number = int(client.recv(2048).decode("utf-8"))
        if number in [1, 2]:
            break
    window_size = (TABLE_WIDTH, TABLE_HEIGHT)
    table = pg.display.set_mode(window_size)
    pg.display.set_caption("Pong Game")

    player1 = Player(number)
    ball = None

    run = True
    reset = True

    while run:
        if reset:
            ball = Ball(TABLE_WIDTH/2, TABLE_HEIGHT/2)
            reset = False

        for event in pg.event.get():
            if event.type == pg.WINDOWCLOSE:
                run = False
        
        table.fill(TABLE_COLOR)
        ball.draw(table)
        player1.draw(table)

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player1.up()
        elif keys[pg.K_s]:
            player1.down()
        
        ball.move()
        ball_x = ball.get_x()
        ball_y = ball.get_y()
        ball_radius = ball.get_radius()

        if ball_x - ball_radius < PLAYER_WIDTH or ball_x + ball_radius > TABLE_WIDTH - PLAYER_WIDTH:
            if not player1.collide_with_ball(ball):
                # Resetando a posição da bola
                reset = True

        if ball_y - ball_radius < 0 or ball_y + ball_radius > TABLE_HEIGHT:
            ball.reflect_y()
        
        time.sleep(1/60) # 60 fps
        pg.display.update()

main()