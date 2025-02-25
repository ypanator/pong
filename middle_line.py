import pygame
from constants import (
    LINE_WIDTH, LINE_HEIGHT, LINE_OFFSET, LINE_GAP, SCREEN_HEIGHT, SCREEN_WIDTH
)

class MiddleLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = pygame.Surface((LINE_WIDTH, SCREEN_HEIGHT))
        self.surf.fill("black")
        self.surf.set_colorkey("black")
        for i in range(-LINE_OFFSET, SCREEN_HEIGHT, LINE_HEIGHT + LINE_GAP):
            pygame.draw.line(
                self.surf, "white", (LINE_WIDTH // 2, i), (LINE_WIDTH // 2, i + LINE_HEIGHT), LINE_WIDTH
            )
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))