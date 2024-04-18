import pygame
import random
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, REACHEDBORDER, BALL_OFFSET
)

class Ball(pygame.sprite.Sprite):
    START_VEL = [5, 5]
    RADIUS = 6
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((self.RADIUS * 2, self.RADIUS * 2))
        self.surf.fill("black")
        pygame.draw.circle(self.surf, "white", (self.RADIUS, self.RADIUS), self.RADIUS)
        self.surf.set_colorkey("black")

        self.is_left = random.choice([True, False])
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.cur_vel = [0, 0]


    def fire(self):
        if self.is_left:
            self.cur_vel = self.START_VEL
        else:
            self.cur_vel = [-self.START_VEL[0], self.START_VEL[1]]
        

    def handle_border(self):
        if self.pos[1] == self.surf.get_height() / 2 or self.pos[1] == SCREEN_HEIGHT - self.surf.get_height() / 2:
            self.cur_vel[1] *= -1

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=False))


    def move(self, dt):
        self.pos[0] += self.cur_vel[0] * dt
        self.pos[1] += self.cur_vel[1] * dt

        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

        self.handle_border()


    def follow_player(self, player_pos):
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            player_pos[1]
        ]        
        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        

    def update(self, dt, is_rolling, player_pos):
        self.move(dt) if is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self.is_left = is_left
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.cur_vel = [0, 0]