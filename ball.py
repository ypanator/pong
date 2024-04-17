import pygame
import random
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH
)

class Ball(pygame.sprite.Sprite):
    START_VEL = [5, 0]
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill("white")
        self.is_left = random.choice([True, False])
        self.pos = [[35, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 35, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.curr_vel = [0, 0]

    def push_ball(self):
        if self.is_left:
            self.curr_vel = START_VEL
        else:
            self.curr_vel = [-START_VEL[0], START_VEL[1]]

    def update(self, dt):
        self.pos[0] += self.curr_vel[0] * dt
        self.pos[1] += self.curr_vel[1] * dt

        self.rect.move_ip(0, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def reset(self):
        self.is_left = random.choice([True, False])
        self.pos = [[35, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 35, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.curr_vel = [0, 0]