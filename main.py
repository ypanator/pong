import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT,

)

from player import Player
from ball import Ball
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYERFIRE, REACHEDBORDER
)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("black")

ball = Ball()
player_left = Player(True)
player_right = Player(False)

drawables = pygame.sprite.Group()
players = pygame.sprite.Group()
drawables.add(player_left, player_right, ball)
players.add(player_left, player_right)

clock = pygame.time.Clock()

is_rolling = False
run = True

while run:
     
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                run = False
        
        if event.type == QUIT:
            run = False
        
        if not is_rolling and event.type == PLAYERFIRE and event.is_left == ball.is_left:
            print("pushed")
            ball.push_ball()
            is_rolling = True
        
        if event.type == REACHEDBORDER:
            ball.reset(event.is_left)
            is_rolling = False

    dt = clock.tick() / 1000 * 60
    players.update(pygame.key.get_pressed(), dt)
    if is_rolling:
        ball.update(dt)
        
    screen.fill("black")
    for ent in drawables:
        screen.blit(ent.surf, ent.rect)
        
    pygame.display.flip()

pygame.quit()