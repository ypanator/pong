import pygame
from constants import (
    SCORE_OFFSETS, SCREEN_WIDTH, SCORE_FONT_SIZE
)

class Score(pygame.sprite.Sprite):
    font = pygame.font.Font("retro_font.ttf", SCORE_FONT_SIZE)

    def render(self, score):
        return self.font.render(str(score), False, "white", "black")

    def __init__(self, is_left):
        super().__init__()
        
        self.surf = self.render(0)
        self.surf.set_colorkey("black")
        self.rect = self.surf.get_rect(center = (
            SCORE_OFFSETS[0] if is_left else SCREEN_WIDTH - SCORE_OFFSETS[0],
            SCORE_OFFSETS[1]
        ))
    
    def update(self, score):
        self.surf = self.render(score)