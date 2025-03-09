import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT,
)

from entities.player import Player
from entities.score import Score
from entities.ball import Ball
from entities.middle_line import MiddleLine

from constants import (
    PLAYER_FIRE_EVENT, REACHED_BORDER_EVENT, SFX_VOLUME
)

class GameScene:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        self.reachedborder_sound = pygame.mixer.Sound("audio\\reachedborder.wav")
        self.reachedborder_sound.set_volume(SFX_VOLUME)

        self.ball = Ball()
        self.player_left = Player(True)
        self.player_right = Player(False)
        self.score_left = Score(True)
        self.score_right = Score(False)
        self.middle_line = MiddleLine()

        self.drawables = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.drawables.add(self.player_left, self.player_right, self.ball, self.score_left, self.score_right, self.middle_line)
        self.players.add(self.player_left, self.player_right)

        self.clock = pygame.time.Clock()

        self.is_rolling = False
        self.run = True

    def start(self, data, scene_manager):
        while self.run and scene_manager.run:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key in (K_q, K_ESCAPE):
                        self.run = False
                        scene_manager.run = False
                
                if event.type == QUIT:
                    self.run = False
                
                if (
                    not self.is_rolling and event.type == PLAYER_FIRE_EVENT and 
                    event.is_left == self.ball.is_left
                ):
                    self.ball.launch()
                    self.is_rolling = True

                if event.type == REACHED_BORDER_EVENT:
                    self.reachedborder_sound.play()
                    if event.is_left: 
                        self.player_right.score += 1
                        self.score_right.update(self.player_right.score)
                    else: 
                        self.player_left.score += 1
                        self.score_left.update(self.player_left.score)

                    self.ball.reset(event.is_left)
                    self.is_rolling = False

            dt = self.clock.tick() / 1000 * 60
            self.players.update(pygame.key.get_pressed(), dt)
            self.ball.update(dt, self.is_rolling, 
                self.player_left.pos if self.ball.is_left else self.player_right.pos, self.players
            )
                
            self.screen.fill("black")
            for ent in self.drawables:
                self.screen.blit(ent.surf, ent.rect)
                
            pygame.display.flip()