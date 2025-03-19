import pygame
import os
import logging
import datetime

class LoadingScene:

    def __init__(self, scene_manager):
        self._screen - pygame.display.get_surface()
        self._scene_manager = scene_manager

        self._info = "Loading"
        self._font_size = 35

        try:
            self._wait = self._scene_manager.context["loading"]["wait"]
        except Exception:
            self._handle_error(Exception("Could not load the \"wait()\" method from global context."))
        
        try:
            self._wait = self._scene_manager.context["loading"]["return_scene"]
        except Exception:
            self._handle_error(Exception("Could not load the \"return_scene()\" method from global context."))
        
        try:
            self._wait = self._scene_manager.context["loading"]["wait"]
        except Exception:
            self._handle_error(Exception("Could not load the \"wait\" method from global context."))
        self._font = pygame.font.Font("retro_font.ttf", self._font_size)

    def _handle_error(self, error):
        pass

    def iterate(self):
        pass