import pygame
from constants import SCREEN_HEIGHT

class RoomCode(pygame.sprite.Sprite):
    FONT_SIZE = 10
    font = pygame.font.Font("retro_font.ttf", FONT_SIZE)

    def _render(self, text):
        return self.font.render(str(text), False, "white", "black")

    def __init__(self):
        super().__init__()
        
        self.prefix = "code: "
        self.surf = self._render("")
        self.surf.set_colorkey("black")
        self.rect = self.surf.get_rect(center = (
            20, SCREEN_HEIGHT - 20
        ))
    
    def update(self, room_code):
        self.surf = self._render(self.prefix + room_code)
