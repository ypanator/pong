import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT,

)

from player import Player
from score import Score
from ball import Ball
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYERFIRE, REACHEDBORDER
)


pygame.init()
pygame.display.set_caption("pong")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("black")

ball = Ball()
player_left = Player(True)
player_right = Player(False)
score_left = Score(True)
score_right = Score(False)

drawables = pygame.sprite.Group()
players = pygame.sprite.Group()
drawables.add(player_left, player_right, ball, score_left, score_right)
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
            ball.launch()
            is_rolling = True

        if event.type == REACHEDBORDER:
            if event.is_left: 
                player_right.score += 1
                score_right.update(player_right.score)
            else: 
                player_left.score += 1
                score_left.update(player_left.score)

            print(f"{player_right.score = } {player_left.score = }")
            ball.reset(event.is_left)
            is_rolling = False

    dt = clock.tick() / 1000 * 60
    players.update(pygame.key.get_pressed(), dt)
    ball.update(dt, is_rolling, player_left.pos if ball.is_left else player_right.pos, players)
        
    screen.fill("black")
    for ent in drawables:
        screen.blit(ent.surf, ent.rect)
        
    pygame.display.flip()

pygame.quit()