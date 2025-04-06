import pygame
import random
import math
from models import enable_event

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_HEIGHT, BALL_ACCELERATION,
    BALL_OFFSET, BALL_RADIUS, BALL_ANGLE, MIN_ANGLE_FACTOR, BALL_VELOCITY, REACHED_BORDER_EVENT
)

class Ball:
    def __init__(self, event):
        self._is_left = random.choice([True, False])
        self.vel = self.xv = self.yv = 0
        self.is_rolling = False

        center = (
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        )        
        self.rect = pygame.rect.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.rect.center = center

        self._reached_border_event = event


    def launch(self):
        factor = random.choice([-1, 1]) * random.uniform(MIN_ANGLE_FACTOR, 1)
        angle = factor * BALL_ANGLE
        self.vel = BALL_VELOCITY

        self.xv = math.cos(angle) * self.vel
        self.xv *= 1 if self._is_left else -1
        self.yv = math.sin(angle) * self.vel

        self.is_rolling = True


    def handle_border(self):
        x, y = self.rect

        if y <= BALL_RADIUS:
            y = BALL_RADIUS + 1
            self.yv *= -1
            self.rect.center = (x, y)
        
        if y >= SCREEN_HEIGHT - BALL_RADIUS:
            y = SCREEN_HEIGHT - BALL_RADIUS - 1
            self.yv *= -1        
            self.rect.center = (x, y)    

        if self.rect.left <= 0:
            enable_event(self._reached_border_event, True)
        elif self.rect.right >= SCREEN_WIDTH:
            enable_event(self._reached_border_event, False)


    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player._rect):
                factor = (self._pos[1] - player._rect.centery) / (PADDLE_HEIGHT / 2)
                factor = math.copysign(max(MIN_ANGLE_FACTOR, abs(factor)), factor)
                angle = factor * BALL_ANGLE
                self.vel += BALL_ACCELERATION

                self.xv = math.cos(angle) * self.vel
                self.xv *= 1 if player._is_left else -1
                self.yv = math.sin(angle) * self.vel

                if player.is_left:
                    self._pos[0] = player._rect.right + BALL_RADIUS + 1
                else:
                    self._pos[0] = player._rect.left - BALL_RADIUS - 1
                break


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()
        
        x, y = self.rect.center
        x += self.xv * dt
        y += self.yv * dt
        self.rect.center = (x, y)


    def follow_player(self, player_y):
        x, y = self.rect.center
        x = BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET
        y = player_y
        self.rect.center = (x, y)
        

    def update(self, dt, player_pos, players):
        self.move(dt, players) if self.is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self._is_left = is_left
        self.rect.center = (
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2            
        )
        self.is_rolling = False