import pygame
import random
import math

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_HEIGHT, BALL_ACCELERATION,
    BALL_OFFSET, BALL_RADIUS, BALL_ANGLE, MIN_ANGLE_FACTOR, BALL_VELOCITY, REACHED_BORDER_EVENT
)

class Ball:
    def __init__(self):
        self._is_left = random.choice([True, False])
        self._vel = self._xv = self._yv = 0

        center = (
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        )        
        self._rect = pygame.rect.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self._rect.center = center


    def launch(self):
        factor = random.choice([-1, 1]) * random.uniform(MIN_ANGLE_FACTOR, 1)
        angle = factor * BALL_ANGLE
        self._vel = BALL_VELOCITY

        self._xv = math.cos(angle) * self._vel
        self._xv *= 1 if self._is_left else -1
        self._yv = math.sin(angle) * self._vel


    def handle_border(self):
        x, y = self._rect

        if y <= BALL_RADIUS:
            y = BALL_RADIUS + 1
            self._yv *= -1
            self._rect.center = (x, y)
        
        if y >= SCREEN_HEIGHT - BALL_RADIUS:
            y = SCREEN_HEIGHT - BALL_RADIUS - 1
            self._yv *= -1        
            self._rect.center = (x, y)    

        if self._rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=True))
        elif self._rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=False))


    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player._rect):
                factor = (self._pos[1] - player._rect.centery) / (PADDLE_HEIGHT / 2)
                factor = math.copysign(max(MIN_ANGLE_FACTOR, abs(factor)), factor)
                angle = factor * BALL_ANGLE
                self._vel += BALL_ACCELERATION

                self._xv = math.cos(angle) * self._vel
                self._xv *= 1 if player._is_left else -1
                self._yv = math.sin(angle) * self._vel

                if player.is_left:
                    self._pos[0] = player._rect.right + BALL_RADIUS + 1
                else:
                    self._pos[0] = player._rect.left - BALL_RADIUS - 1
                break


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()
        
        x, y = self._rect.center
        x += self._xv * dt
        y += self._yv * dt
        self._rect.center = (x, y)


    def follow_player(self, player_y):
        x, y = self._rect.center
        x = BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET
        y = player_y
        self._rect.center = (x, y)
        

    def update(self, dt, is_rolling, player_pos, players):
        self.move(dt, players) if is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self._is_left = is_left
        self._rect.center = (
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2            
        )