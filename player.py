import pygame as pg
from ball import Ball

PLAYER_COLOR = (217, 217, 217)
PLAYER_HEIGHT = 150
PLAYER_WIDTH = 15
PLAYER_SPEED = 5

class Player:
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, table: pg.surface.Surface):
        player_rect = pg.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        pg.draw.rect(table, PLAYER_COLOR, player_rect)
    
    def up(self):
        self.y = max(self.y - PLAYER_SPEED, 0)

    def down(self, window_height: int = 400):
        self.y = min(self.y + PLAYER_SPEED, window_height-PLAYER_HEIGHT)

    def collide_with_ball(self, ball: Ball) -> bool:
        ball_y = ball.get_y()
        ball_radius = ball.get_radius()

        if ball_y < (self.y + PLAYER_HEIGHT + ball_radius) and ball_y > (self.y - ball_radius):
            ball.reflect_x()
            return True
        else:
            return False
            