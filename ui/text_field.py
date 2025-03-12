import pygame
from constants import (
    TEXT_FIELD_FONT_SIZE, TEXT_FIELD_FILL, TEXT_FIELD_ACCENT, CURSOR_Y_OFFSET,
    CURSOR_BLINK_EVENT, CURSOR_BLINK_DELAY, CURSOR_WIDTH, CURSOR_X_OFFSET
)

class TextField:
    """
    A class to represent a text field in a Pygame application.
    """

    def __init__(self, x: int, y: int, width: int, height: int, thickness: int):
        """
        Initialize the text field.

        Args:
            x (int): The x-coordinate of the text field.
            y (int): The y-coordinate of the text field.
            width (int): The width of the text field.
            height (int): The height of the text field.
            thickness (int): The thickness of the text field border.
        """
        self.text = []
        pygame.time.set_timer(CURSOR_BLINK_EVENT, CURSOR_BLINK_DELAY)

        self.base = self._get_base(x, y, width, height, thickness)
        try:
            self.font = pygame.font.Font("retro_font.ttf", TEXT_FIELD_FONT_SIZE)
        except FileNotFoundError:
            raise RuntimeError("Font file 'retro_font.ttf' not found.")

        self.cursor = pygame.surface.Surface((CURSOR_WIDTH, height - 2 * thickness - CURSOR_Y_OFFSET))
        self.cursor.fill(TEXT_FIELD_ACCENT)
        self.is_visible = True

        self.rect = self.base[1]
        self.surf = self._draw()
    
    def _draw(self) -> pygame.Surface:
        """
        Draw the text field surface.

        Returns:
            pygame.Surface: The surface with the text field drawn on it.
        """
        surf = self.base[0].copy()
        text_surf = self.font.render("".join(self.text), False, TEXT_FIELD_ACCENT, TEXT_FIELD_FILL)
        text_rect = text_surf.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        surf.blit(text_surf, text_rect)

        if self.is_visible:
            cursor_rect = self.cursor.get_rect(center=(text_rect.right + CURSOR_X_OFFSET, self.rect.h // 2))
            surf.blit(self.cursor, cursor_rect)
        
        return surf
    
    def _get_base(self, x: int, y: int, width: int, height: int, thickness: int) -> tuple[pygame.Surface, pygame.Rect]:
        """
        Create the base surface and rectangle for the text field.

        Args:
            x (int): The x-coordinate of the text field.
            y (int): The y-coordinate of the text field.
            width (int): The width of the text field.
            height (int): The height of the text field.
            thickness (int): The thickness of the text field border.

        Returns:
            tuple: A tuple containing the base surface and rectangle.
        """
        border_surf = pygame.Surface((width, height))
        border_surf.fill(TEXT_FIELD_ACCENT)
        border_rect = border_surf.get_rect(center=(x, y))

        panel_surf = pygame.Surface((width - 2 * thickness, height - 2 * thickness))
        panel_surf.fill(TEXT_FIELD_FILL)
        panel_rect = panel_surf.get_rect(center=(border_rect.w // 2, border_rect.h // 2))

        border_surf.blit(panel_surf, panel_rect)
        return (border_surf, border_rect)

    def update(self, events: list):
        """
        Update the text field based on events.

        Args:
            events (list): A list of Pygame events.
        """
        changed = False
        for event in events:
            if event.type == CURSOR_BLINK_EVENT:
                self.is_visible = not self.is_visible
                changed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.text:
                    self.text.pop()
                    changed = True
                elif event.unicode:
                    self.text.append(event.unicode)
                    changed = True
        if changed:
            self.surf = self._draw()