import pygame
import random
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, REACHEDBORDER, BALL_OFFSET, RADIUS, START_VEL
)

class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((RADIUS * 2, RADIUS * 2))
        self.surf.fill("black")
        pygame.draw.circle(self.surf, "white", (RADIUS, RADIUS), RADIUS)
        self.surf.set_colorkey("black")

        self.is_left = random.choice([True, False])
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.cur_vel = [0, 0]


    def launch(self):
        if self.is_left:
            self.cur_vel = START_VEL
        else:
            self.cur_vel = [-START_VEL[0], START_VEL[1]]
        

    def handle_border(self):
        if self.pos[1] == self.surf.get_height() / 2 or self.pos[1] == SCREEN_HEIGHT - self.surf.get_height() / 2:
            self.cur_vel[1] *= -1

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHEDBORDER, is_left=False))
    

    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player.rect):
                self.cur_vel = [self.cur_vel[0] * -1, self.cur_vel[1]]
                if player.is_left:
                    self.pos[0] = player.rect.right + RADIUS
                else:
                    self.pos[0] = player.rect.left - RADIUS
                print("player collision")


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()

        self.pos[0] += self.cur_vel[0] * dt
        self.pos[1] += self.cur_vel[1] * dt

        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)


    def follow_player(self, player_pos):
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            player_pos[1]
        ]        
        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        

    def update(self, dt, is_rolling, player_pos, players):
        self.move(dt, players) if is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self.is_left = is_left
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.cur_vel = [0, 0]