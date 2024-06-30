import pygame
from constants import (
    SCORE_OFFSETS, SCREEN_WIDTH, FONT_SIZE
)

class Score(pygame.sprite.Sprite):
    pygame.font.init()
    font = pygame.font.Font("retro_font.ttf", FONT_SIZE)

    def _render(self, score):
        return self.font.render(str(score), False, "white", "black")

    def __init__(self, is_left):
        super().__init__()
        self.surf = self._render(0)
        self.surf.set_colorkey("black")
        self.rect = self.surf.get_rect(center = (
            SCORE_OFFSETS[0] if is_left else SCREEN_WIDTH - SCORE_OFFSETS[0],
            SCORE_OFFSETS[1]
        ))
    
    def update(self, score):
        self.surf = self._render(score)