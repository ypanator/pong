import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_FIRE_EVENT
)
import time

class Paddle:
    def __init__(self, is_left, event):
        self._is_left = is_left
        self._fired_timestamp = 0
        self._fired_timestep = 500

        center = (
            PADDLE_OFFSET if self._is_left else SCREEN_WIDTH - PADDLE_OFFSET,
            SCREEN_HEIGHT // 2
        )        
        self.rect = pygame.rect.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rect.center = center

        self._paddle_fire_event = event


    def update(self, pressed, dt):
        x, y = self.rect.center
        if pressed.up:
            y -= 5 * dt
        if pressed.down:
            y += 5 * dt
        if pressed.fire:
            if time.time() * 1000 - self._fired_timestamp >= self._fired_timestep:
                self._fired_timestamp = time.time() * 1000
                self._paddle_fire_event.enable(self._is_left)
        
        y = max(y, PADDLE_HEIGHT / 2)
        y = min(y, SCREEN_HEIGHT - PADDLE_HEIGHT / 2)
        self.rect.center = (x, y)