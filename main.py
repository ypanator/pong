import pygame
from pygame.locals import (
    K_w,
    K_s,
    K_UP,
    K_DOWN,
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    USEREVENT
)
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, is_left, has_ball):
        super().__init__()
        self.surf = pygame.Surface((7, SCREEN_HEIGHT/4))
        self.surf.fill("white")
        self.pos = [20, SCREEN_HEIGHT / 2] if is_left else [SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.is_left = is_left
        self.has_ball = has_ball

    def update(self, pressed_keys):
        if self.is_left:
            if pressed_keys[K_w]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_s]:
                self.pos[1] += 5 * dt
        else:
            if pressed_keys[K_UP]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_DOWN]:
                self.pos[1] += 5 * dt
        
        if int(self.pos[1] - self.rect.centery) != 0:
            pygame.event.post(pygame.event.Event(HAS_MOVED))

        self.rect.move_ip(0, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill("white")
        self.is_left = random.choice([True, False])
        self.pos = [[35, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 35, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        
    def update(self):
        if is_rolling:
            pass


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("black")

HAS_MOVED = USEREVENT + 1

ball = Ball()
player_left = Player(True, ball.is_left)
player_right = Player(False, not ball.is_left)

drawables = pygame.sprite.Group()
players = pygame.sprite.Group()
drawables.add(player_left, player_right, ball)
players.add(player_left, player_right)

clock = pygame.time.Clock()
dt = clock.tick() / 1000 * 60

is_rolling = False
run = True
while run:
     
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                run = False
        
        if event.type == QUIT:
            run = False
        
        if event.type == HAS_MOVED:
            

    dt = clock.tick() / 1000 * 60
    players.update(pygame.key.get_pressed())
    ball.update()

    screen.fill("black")
    for ent in drawables:
        screen.blit(ent.surf, ent.rect)
        
    pygame.display.flip()

pygame.quit()