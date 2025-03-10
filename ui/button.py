import pygame
from constants import (
    BUTTON_FONT_SIZE, BUTTON_FILL, BUTTON_ACCENT_ACTIVE, BUTTON_ACCENT_INACTIVE
)

class Button:

    def __init__(self, x, y, width, height, thickness, text):
        self.active_button = self._create_button(BUTTON_ACCENT_ACTIVE, x, y, width, height, thickness, text)
        self.inactive_button = self._create_button(BUTTON_ACCENT_INACTIVE, x, y, width, height, thickness, text)

    def _create_button(self, accent, x, y, width, height, thickness, text):
        border_surf = pygame.Surface((width, height))
        border_surf.fill(accent)
        border_rect = border_surf.get_rect(center = (x, y))

        panel_surf = pygame.Surface((width - 2 * thickness, height - 2 * thickness))
        panel_surf.fill(BUTTON_FILL)
        panel_rect = panel_surf.get_rect(center = (border_rect.w // 2, border_rect.h // 2))

        font = pygame.font.Font("retro_font.ttf", BUTTON_FONT_SIZE)
        text_surf = font.render(text, False, accent, BUTTON_FILL)
        text_rect = text_surf.get_rect(center = (panel_rect.w // 2, panel_rect.h // 2))

        panel_surf.blit(text_surf, text_rect)
        border_surf.blit(panel_surf, panel_rect)

        return (border_surf, border_rect)

    def get_inactive_button(self):
        return self.inactive_button
    
    def get_active_button(self):
        return self.active_button