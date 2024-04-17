import pygame
import random
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, REACHEDBORDER
)

class Ball(pygame.sprite.Sprite):
    START_VEL = [5, 0]
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill("white")
        self.is_left = random.choice([True, False])
        self.pos = [[SCREEN_WIDTH - 35, SCREEN_HEIGHT / 2], [35, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.curr_vel = [0, 0]

    def push_ball(self):
        if self.is_left:
            self.curr_vel = self.START_VEL
        else:
            self.curr_vel = [-self.START_VEL[0], self.START_VEL[1]]

    def update(self, dt):
        self.pos[0] += self.curr_vel[0] * dt
        self.pos[1] += self.curr_vel[1] * dt

        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=False))

    def reset(self, is_left):
        self.is_left = is_left
        self.pos = [[SCREEN_WIDTH - 35, SCREEN_HEIGHT / 2], [35, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.curr_vel = [0, 0]