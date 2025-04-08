import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT
)

from .local_entities.paddle import Paddle
from .local_entities.score import Score
from .local_entities.ball import Ball
from .local_entities.middle_line import MiddleLine

from constants import (
    PADDLE_FIRE_EVENT, REACHED_BORDER_EVENT, SFX_VOLUME
)

class LocalGameScene:
    def __init__(self, scene_manager):
        self._scene_manager = scene_manager

        self._screen = pygame.display.get_surface()

        self._reachedborder_sound = pygame.mixer.Sound("audio\\reachedborder.wav")
        self._reachedborder_sound.set_volume(SFX_VOLUME)

        self._ball = Ball()
        self._paddle_left = Paddle(True)
        self._paddle_right = Paddle(False)
        self._score_left = Score(True)
        self._score_right = Score(False)
        self._middle_line = MiddleLine()

        self._drawables = pygame.sprite.Group()
        self._paddles = pygame.sprite.Group()
        self._drawables.add(self._paddle_left, self._paddle_right, self._ball, self._score_left, self._score_right, self._middle_line)
        self._paddles.add(self._paddle_left, self._paddle_right)

        self._is_rolling = False

    def iterate(self, tick):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    self._scene_manager.change_scene("MainMenuScene")
            
            if event.type == QUIT:
                self._scene_manager.close()
            
            if (
                not self._is_rolling and event.type == PADDLE_FIRE_EVENT and 
                event.is_left == self._ball._is_left
            ):
                self._ball.launch()
                self._is_rolling = True

            if event.type == REACHED_BORDER_EVENT:
                self._reachedborder_sound.play()
                if event.is_left: 
                    self._paddle_right._score += 1
                    self._score_right.update(self._paddle_right._score)
                else: 
                    self._paddle_left._score += 1
                    self._score_left.update(self._paddle_left._score)

                self._ball.reset(event.is_left)
                self._is_rolling = False

        dt = tick / 1000 * 60
        self._paddles.update(pygame.key.get_pressed(), dt)
        self._ball.update(dt, self._is_rolling, 
            self._paddle_left._pos if self._ball._is_left else self._paddle_right._pos, self._paddles
        )
            
        self._screen.fill("black")
        for ent in self._drawables:
            self._screen.blit(ent.surf, ent.rect)
            
        pygame.display.flip()