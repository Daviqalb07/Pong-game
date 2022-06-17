import pygame as pg
from random import choice
from properties import *

class Ball:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.speed_x = SPEED_X * choice((-1, 1))
        self.speed_y = SPEED_Y * choice((-1, 1))
        self.radius = BALL_RADIUS

    def draw(self, table: pg.Surface):
        ball_center = (self.x, self.y)
        pg.draw.circle(table, BALL_COLOR, ball_center, BALL_RADIUS)
    
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