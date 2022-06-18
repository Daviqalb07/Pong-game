import pygame as pg
from ball import Ball
from properties import *

def draw_opponent(x: int, y: int, table: pg.Surface):
    opponent_rect = pg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pg.draw.rect(table, PLAYER_COLOR, opponent_rect)

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
        return f'player-position {self.number} {int(self.x)} {int(self.y)} '
    
    def collided_in_x(self, ball_x):
        if self.number == 1:
            return (ball_x - BALL_RADIUS) < PLAYER_WIDTH
        
        else: # if player's number equals 2
            return (ball_x + BALL_RADIUS) > self.x
    
    def collided_in_y(self, ball_y) -> bool:
        conditions = [
            (ball_y - BALL_RADIUS) < (self.y + PLAYER_HEIGHT),
            (ball_y + BALL_RADIUS) > self.y
        ]
        return all(conditions)
        
    def collided_with_ball(self, ball_x, ball_y) -> bool:
        if self.number == 1 and (ball_x - BALL_RADIUS) < PLAYER_WIDTH:
            if ball_y < (self.y + PLAYER_HEIGHT + BALL_RADIUS) and ball_y > (self.y - BALL_RADIUS):
                return True
            else:
                return False
        elif self.number == 2 and (ball_x + BALL_RADIUS) > self.x:
            if ball_y < (self.y + PLAYER_HEIGHT + BALL_RADIUS) and ball_y > (self.y - BALL_RADIUS):
                return True
            else:
                return False
        else:
            return False