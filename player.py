import pygame as pg
from ball import Ball
from properties import *

def draw_opponent(x: int, y: int, table: pg.Surface):
    opponent_rect = pg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pg.draw.rect(table, PLAYER_COLOR, opponent_rect)

def collided_in_x(number: int, player_x: int, ball_x: int):
        if number == 1:
            return (ball_x - BALL_RADIUS) < PLAYER_WIDTH
        
        else: # if player's number equals 2
            return (ball_x + BALL_RADIUS) > player_x 

def collided_in_y(player_y: int, ball_y: int) -> bool:
    conditions = [
        (ball_y - BALL_RADIUS) < (player_y + PLAYER_HEIGHT),
        (ball_y + BALL_RADIUS) > player_y
    ]
    return all(conditions)

class Player:
    def __init__(self, number: int):
        self.number = number
        if number == 1:
            self.x = 0
        else:
            self.x = TABLE_WIDTH - PLAYER_WIDTH
        self.y = (TABLE_HEIGHT-PLAYER_HEIGHT)/2
    
    def draw(self, table: pg.surface.Surface):
        player_rect = pg.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        pg.draw.rect(table, PLAYER_COLOR, player_rect)
    
    def up(self):
        self.y = max(self.y - PLAYER_SPEED, 0)

    def down(self, window_height: int = 400):
        self.y = min(self.y + PLAYER_SPEED, window_height-PLAYER_HEIGHT)

    def player_info(self):
        return f'player-position {int(self.x)} {int(self.y)} '
