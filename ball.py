from properties import *

import pygame as pg
from random import choice

def draw_ball(center_x: int, center_y: int, table: pg.Surface):
    center = (center_x, center_y)
    pg.draw.circle(table, BALL_COLOR, center, BALL_RADIUS)

class Ball:
    def __init__(self, x: int = TABLE_WIDTH/2, y: int = TABLE_HEIGHT/2):
        self.x = x
        self.y = y
        self.speed_x = SPEED_X * choice((-1, 1))
        self.speed_y = SPEED_Y * choice((-1, 1))
        self.radius = BALL_RADIUS
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_radius(self):
        return self.radius

    def reflect_x(self):
        self.speed_x *= -1

    def reflect_y(self):
        self.speed_y *= -1
    
    def ball_xy_encode(self) -> str:
        return f'ball {int(self.x)} {int(self.y)} '
    

