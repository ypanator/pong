import pygame
from constants import (
    BUTTON_FONT_SIZE, BUTTON_FILL, BUTTON_ACCENT_ACTIVE, BUTTON_ACCENT_INACTIVE
)

class Button:

    def __init__(self, x, y, width, height, thickness, text, action):
        self._is_active = False
        self._action = action

        self._active_button = self._create_button(BUTTON_ACCENT_ACTIVE, x, y, width, height, thickness, text)
        self._inactive_button = self._create_button(BUTTON_ACCENT_INACTIVE, x, y, width, height, thickness, text)

        self.surf, self.rect = self._inactive_button

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

    def _set_active(self):
        if not self._is_active:
            self._is_active = True
            self.surf, _ = self._active_button
    
    def _set_inactive(self):
        if self._is_active:
            self._is_active = False
            self.surf, _ = self._inactive_button

    def update(self, events):
        for event in events:
            if getattr(event, "button", -1) != 1:
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self._set_active()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self._is_active:
                    self._action()
                self._set_inactive()