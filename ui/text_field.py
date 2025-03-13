import pygame
from constants import (
    TEXT_FIELD_FONT_SIZE, TEXT_FIELD_FILL, TEXT_FIELD_ACCENT, CURSOR_Y_OFFSET,
    CURSOR_BLINK_EVENT, CURSOR_BLINK_DELAY, CURSOR_WIDTH, CURSOR_X_OFFSET
)

class TextField:

    def __init__(self, x, y, width, height, thickness, limit):
        self._text = []
        self._limit = limit
        pygame.time.set_timer(CURSOR_BLINK_EVENT, CURSOR_BLINK_DELAY)

        self._base = self._get_base(x, y, width, height, thickness)
        self._font = pygame.font.Font("retro_font.ttf", TEXT_FIELD_FONT_SIZE)

        self._cursor = pygame.surface.Surface((CURSOR_WIDTH, height - 2 * thickness - CURSOR_Y_OFFSET))
        self._cursor.fill(TEXT_FIELD_ACCENT)
        self._is_visible = True

        self.rect = self._base[1]
        self.surf = self._draw()
    
    def _draw(self):
        surf = self._base[0].copy()
        text_surf = self._font.render("".join(self._text), False, TEXT_FIELD_ACCENT, TEXT_FIELD_FILL)
        text_rect = text_surf.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        surf.blit(text_surf, text_rect)

        if self._is_visible:
            cursor_rect = self._cursor.get_rect(center=(text_rect.right + CURSOR_X_OFFSET, self.rect.h // 2))
            surf.blit(self._cursor, cursor_rect)
        
        return surf
    
    def _get_base(self, x, y, width, height, thickness):
        border_surf = pygame.Surface((width, height))
        border_surf.fill(TEXT_FIELD_ACCENT)
        border_rect = border_surf.get_rect(center=(x, y))

        panel_surf = pygame.Surface((width - 2 * thickness, height - 2 * thickness))
        panel_surf.fill(TEXT_FIELD_FILL)
        panel_rect = panel_surf.get_rect(center=(border_rect.w // 2, border_rect.h // 2))

        border_surf.blit(panel_surf, panel_rect)
        return (border_surf, border_rect)

    def update(self, events):
        changed = False
        for event in events:
            if event.type == CURSOR_BLINK_EVENT :
                self._is_visible = not self._is_visible
                changed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self._text:
                    self._text.pop()
                    changed = True
                elif event.unicode and len(self._text) < self._limit:
                    self._text.append(event.unicode)
                    changed = True
        if changed:
            self.surf = self._draw()
    
    def get_text(self):
        return "".join(self._text)