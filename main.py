import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT,
)

from player import Player
from score import Score
from ball import Ball
from middle_line import MiddleLine

from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_FIRE_EVENT, REACHED_BORDER_EVENT, SFX_VOLUME
)

pygame.init()
pygame.display.set_caption("pong")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("black")

reachedborder_sound = pygame.mixer.Sound("audio\\reachedborder.wav")
reachedborder_sound.set_volume(SFX_VOLUME)

ball = Ball()
player_left = Player(True)
player_right = Player(False)
score_left = Score(True)
score_right = Score(False)
middle_line = MiddleLine()

drawables = pygame.sprite.Group()
players = pygame.sprite.Group()
drawables.add(player_left, player_right, ball, score_left, score_right, middle_line)
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
        
        if not is_rolling and event.type == PLAYER_FIRE_EVENT and event.is_left == ball.is_left:
            ball.launch()
            is_rolling = True

        if event.type == REACHED_BORDER_EVENT:
            reachedborder_sound.play()
            if event.is_left: 
                player_right.score += 1
                score_right.update(player_right.score)
            else: 
                player_left.score += 1
                score_left.update(player_left.score)

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