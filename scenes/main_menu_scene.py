import pygame
from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT
)
from constants import (
    SCREEN_WIDTH, MAIN_MENU_OFFSET, TITLE_FONT_SIZE, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT, MAIN_MENU_BUTTON_BORDER
)
from ui.button import Button
from collections import namedtuple

class MainMenuScene:

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        title_surf = pygame.font.Font("retro_font.ttf", TITLE_FONT_SIZE).render("PONG", False, "white", "black")
        title_rect = title_surf.get_rect(center = (SCREEN_WIDTH // 2, MAIN_MENU_OFFSET + title_surf.get_height() // 2))
        self._title = namedtuple("title", ["surf", "rect"])(title_surf, title_rect)

        self._local_play_button = Button(
            SCREEN_WIDTH // 2, self._title.rect.bottom + MAIN_MENU_OFFSET + MAIN_MENU_BUTTON_HEIGHT // 2, 
            MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT, MAIN_MENU_BUTTON_BORDER, 
            "local play", lambda: scene_manager.change_scene("LocalGameScene")
        )
        
        self._multiplayer_button = Button(
            SCREEN_WIDTH // 2, self._local_play_button.rect.bottom + MAIN_MENU_OFFSET + MAIN_MENU_BUTTON_HEIGHT // 2, 
            MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT, MAIN_MENU_BUTTON_BORDER, 
            "multiplayer", lambda: scene_manager.change_scene("MultiplayerMenuScene")
        )

        self._screen = pygame.display.get_surface()
        self._drawables = [self._title, self._local_play_button, self._multiplayer_button]

    def iterate(self, tick):
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    self.scene_manager.close()
            
            if event.type == QUIT:
                self.scene_manager.close()

        self._multiplayer_button.update(events)
        self._local_play_button.update(events)

        self._screen.fill("black")
        for ent in self._drawables:
            self._screen.blit(ent.surf, ent.rect)

        pygame.display.flip()