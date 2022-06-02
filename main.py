import pygame as pg
import time
from ball import Ball
from player import *


TABLE_COLOR = (23, 21, 38)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 720

def main():
    pg.init()
    pg.display.init()


    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    table = pg.display.set_mode(window_size)
    pg.display.set_caption("Pong Game")

    player1 = Player(0, (WINDOW_HEIGHT-PLAYER_HEIGHT)/2)
    ball = None

    run = True
    reset = True

    while run:
        if reset:
            ball = Ball(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
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

        if ball_x - ball_radius < PLAYER_WIDTH or ball_x + ball_radius > WINDOW_WIDTH:
            if not player1.collide_with_ball(ball):
                # Resetando a posição da bola
                reset = True

        if ball_y - ball_radius < 0 or ball_y + ball_radius > WINDOW_HEIGHT:
            ball.reflect_y()
        
        time.sleep(1/60) # 60 fps
        pg.display.update()

main()