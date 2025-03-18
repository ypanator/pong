import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from ui.text_field import TextField
from collections import namedtuple
from net.client import Client
import net.server_code as codes
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

        self._lpanel_offset_x = SCREEN_WIDTH / 4 - 10
        self._lpanel_offset_y = SCREEN_HEIGHT / 3

        self._rpanel_offset_x = SCREEN_WIDTH * 3 / 4 - 10
        self._rpanel_offset_y = SCREEN_HEIGHT / 4

        self._client = None

        # ---------------------- left panel ----------------------
        self._create_room_button = Button(
            self._lpanel_offset_x, self._lpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "create room", self._create_room_event
        )

        self._back_button = Button(
            self._lpanel_offset_x, self._create_room_button.rect.centery + self._lpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "back", lambda: self._scene_manager.change_scene("MainMenuScene")
        )

        # ---------------------- right panel ----------------------
        self._label_surf = pygame.font.Font("retro_font.ttf", self._font_size).render("ENTER ROOM CODE", False, "white", "black")
        self._label_rect = self._label_surf.get_rect(center = (self._rpanel_offset_x, self._rpanel_offset_y * 2 / 3))
        self._label = namedtuple("label", ["surf", "rect"])(self._label_surf, self._label_rect)

        self._room_code_field = TextField(
            self._rpanel_offset_x, self._label_rect.centery + self._rpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 6
        )

        self._join_button = Button(
            self._rpanel_offset_x, self._room_code_field.rect.bottom + self._rpanel_offset_y, 
            self._button_width, self._button_height, self._button_border, 
            "join", lambda: self._join_room_event(self._room_code_field.get_text())
        )


        self._drawables = [
            self._create_room_button, self._back_button, self._label,
            self._room_code_field, self._join_button
        ]
        self._updatable = [
            self._create_room_button, self._back_button,
            self._room_code_field, self._join_button            
        ]
    
    def iterate(self, tick):
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    self._scene_manager.close()
            
            if event.type == QUIT:
                self._scene_manager.close()

        for ent in self._updatable:
            ent.update(events)

        self._screen.fill("black")
        for ent in self._drawables:
            self._screen.blit(ent.surf, ent.rect)

        pygame.display.flip()
    
    def _start_game(self):
        self._client.write({"type": codes.GET_CODE_REQ, "data": None})
        while (response := self._client.read()) is None or response["type"] != codes.ROOM_CODE:
            pass
        self._scene_manager.context["mp_game"] = { "room": response["data"] }
        self._scene_manager.change_scene("MultiplayerGameScene")

    def _create_room_event(self):
        self._ensure_connection()
        self._client.write({ "type": codes.CREATE_REQ, "data": None })
        self._scene_manager.context["loading"] = {
            "wait": lambda: (response := self._client.read()) is None or response["type"] != codes.ROOM_CREATE,
            "on_load": lambda: self._start_game()
        }

    def _join_room_event(self, code):
        self._ensure_connection()
        self._client.write({ "type": codes.JOIN_REQ, "data": code })
        self._scene_manager.context["loading"] = {
            "wait": lambda: (response := self._client.read()) is None or response["type"] != codes.ROOM_JOIN,
            "on_load": lambda: self._start_game()
        }

    def _ensure_connection(self):
        if self._client is None:
            self._client = Client()
            self._client.connect()