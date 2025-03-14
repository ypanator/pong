import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from ui.text_field import TextField
from collections import namedtuple

from pygame.locals import (
    K_q, K_ESCAPE, KEYDOWN, QUIT
)

class MultiplayerMenuScene:

    def __init__(self, scene_manager):
        self._screen = pygame.display.get_surface()
        self._scene_manager = scene_manager

        self._button_width = 400
        self._button_height = 100
        self._button_border = 10
        self._font_size = 30

        self._lpanel_offset_x = SCREEN_WIDTH / 3
        self._lpanel_offset_y = SCREEN_HEIGHT / 3

        self._rpanel_offset_x = SCREEN_WIDTH * 2 / 3
        self._rpanel_offset_y = SCREEN_HEIGHT  / 4


        #
        # TODO: 
        #       - update button for font size
        #       - update textfield to hold text from left instead of from center
        #


        # ---------------------- left panel ----------------------
        self._create_room_button = Button(
            self._lpanel_offset_x, self._lpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "create room", lambda: print("test 1")
        )

        self._back_button = Button(
            self._lpanel_offset_x, self._create_room_button.rect.centery + self._lpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "back", lambda: print("test 2")
        )
        
        # ---------------------- right panel ----------------------
        self._label_surf = pygame.font.Font("retro_font.ttf", self._font_size).render("ENTER ROOM CODE", False, "white", "black")
        self._label_rect = self._label_surf.get_rect(center = (self._rpanel_offset_x, self._rpanel_offset_y))
        # TODO:
        self.label = namedtuple("label", ["surf", "rect"])(self._label_surf, self._label_rect)

        self._room_code_field = TextField(
            self._rpanel_offset_x, self._label_rect.centery + self._rpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 6
        )

        self._join_button = Button(
            self._rpanel_offset_x, self._room_code_field.rect.centery + self._lpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "back", lambda: print("test 3")
        )

        # TODO:
        self._drawables = None
        self._updatable = None
    
    def iterate(self):
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    self.scene_manager.close()
            
            if event.type == QUIT:
                self.scene_manager.close()

        self.multiplayer_button.update(events)
        self.local_play_button.update(events)

        for ent in self.drawables:
            self.screen.blit(ent.surf, ent.rect)

        pygame.display.flip()